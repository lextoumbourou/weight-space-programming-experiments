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
    # channel 4: ink blob
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125

    # ---------------- conv2: route features to 4x4 grids ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    sm = np.outer([0.5, 1, 0.5], [0.5, 1, 0.5]) / 4.0
    for k in range(4):
        W2[k, k, 1:4, 1:4] = sm
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3)]
    for i, (ky, kx) in enumerate(ink_taps):
        W2[4 + i, 4, ky, kx] = 1.0

    chan_tap = {0: (2, 2), 1: (2, 2), 2: (2, 2), 3: (2, 2)}
    for i, t in enumerate(ink_taps):
        chan_tap[4 + i] = t

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
        pts, angs, steps = [], [], []
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
                    steps.append(L / n)
        return np.array(pts), np.array(angs), np.array(steps)

    def box(t, h, soft=0.7):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- templates in feature space ----------------
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        P, A, S = sample(strokes)
        for ch, (ky, kx) in chan_tap.items():
            if ch < 4:
                o = np.maximum(0.0, np.cos(2 * (A - thetas[ch])))
                h, scale = 3.5, 0.7
            else:
                o = np.ones_like(A)
                h, scale = 3.0, 1.0
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    acc = np.sum(S * o * box(P[:, 0] - cx, h) * box(P[:, 1] - cy, h))
                    T[dgt, ch, r, c] = scale * (1.0 - math.exp(-0.4 * acc))

    # ---------------- fc: centred cosine template matching ----------------
    # logit_d = s * (f - mu) . (T_d - mu) / ||T_d - mu||
    s = 2.0
    Tf = T.reshape(10, -1)
    mu = Tf.mean(axis=0)
    Wfc = np.zeros((10, 256))
    bfc = np.zeros(10)
    for dgt in range(10):
        dvec = Tf[dgt] - mu
        dvec = dvec / (np.linalg.norm(dvec) + 1e-8)
        Wfc[dgt] = s * dvec
        bfc[dgt] = -s * np.dot(mu, dvec)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
