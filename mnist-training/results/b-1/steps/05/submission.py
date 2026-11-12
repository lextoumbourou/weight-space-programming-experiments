import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    Y, X = np.meshgrid(off, off, indexing='ij')
    # 0: horizontal, 1: vertical, 2: "\" (down-right), 3: "/" (up-right)
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        d = np.abs(-math.sin(th) * X + math.cos(th) * Y)
        g = np.exp(-d ** 2 / (2 * 0.8 ** 2))
        w = g - g.mean()
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.1
    # channel 4: ink blob (plus-shaped average)
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125

    # ---------------- conv2: single-tap routing ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    chan_src = {}   # conv2 channel -> (conv1 channel, ky, kx, gain)
    for k in range(4):                      # orientation maps, centre tap, boosted
        chan_src[k] = (k, 2, 2, 1.3)
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3), (2, 1), (2, 3), (1, 2), (3, 2)]
    for i, (ky, kx) in enumerate(ink_taps): # ink at 9 shifts -> channels 4..12
        chan_src[4 + i] = (4, ky, kx, 1.0)
    for ch, (src, ky, kx, gain) in chan_src.items():
        W2[ch, src, ky, kx] = gain
    # channels 13-15 unused

    # ---------------- digit strokes (x=col, y=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        t = np.linspace(0, 2 * math.pi, n + 1)
        return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in t]

    digits = {
        0: [ellipse(14, 14, 6.0, 9.5)],
        1: [[(16, 4.5), (12, 23.5)]],
        2: [[(8, 9), (10, 6), (14, 4.5), (18, 5.5), (20, 9), (18, 13), (13, 18), (8, 23), (14, 23), (21, 23)]],
        3: [[(8, 6), (12, 4.5), (17, 5), (19, 8), (17, 12), (12, 13.5), (17, 15), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        4: [[(11, 4.5), (8, 16), (21, 16)], [(18, 8), (18, 23.5)]],
        5: [[(20, 4.5), (10, 4.5), (9, 13), (14, 12), (19, 14), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        6: [[(17, 4.5), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23.5), (18, 21), (19, 17), (16, 14), (12, 14), (9, 17)]],
        7: [[(8, 5), (20, 5), (17, 11), (14, 17), (12, 23.5)]],
        8: [ellipse(14, 9, 4.0, 4.3), ellipse(14, 18.5, 4.8, 5.0)],
        9: [ellipse(14, 9.5, 5.5, 5.0), [(19, 10), (18, 17), (16, 23.5)]],
    }

    def sample(strokes):
        pts, angs = [], []
        for poly in strokes:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.25))
                phi = math.atan2(y1 - y0, x1 - x0)
                for j in range(n):
                    t = (j + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
                    angs.append(phi)
        return np.array(pts), np.array(angs)

    def box(t, h, soft):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- probability templates p_d(feature on) ----------------
    eps = 0.03
    Pt = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        P, A = sample(strokes)
        for ch, (src, ky, kx, gain) in chan_src.items():
            if src < 4:
                o = np.cos(A - thetas[src]) ** 4    # orientation agreement
                q = 0.85                            # detection reliability
            else:
                o = np.ones_like(A)
                q = 0.95
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    v = o * box(P[:, 0] - cx, 2.5, 1.2) * box(P[:, 1] - cy, 2.5, 1.2)
                    Pt[dgt, ch, r, c] = q * v.max()
    Pt = np.clip(Pt, eps, 1 - eps)

    # ---------------- fc: Bernoulli naive Bayes ----------------
    s = 0.25
    used = np.zeros((16, 4, 4), dtype=bool)
    for ch in chan_src:
        used[ch] = True
    used = used.reshape(-1)
    Wfc = np.zeros((10, 256))
    bfc = np.zeros(10)
    for dgt in range(10):
        p = Pt[dgt].reshape(-1)
        w = np.log(p / (1 - p))
        b = np.log(1 - p)
        w[~used] = 0.0
        b[~used] = 0.0
        Wfc[dgt] = s * w
        bfc[dgt] = s * b.sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
