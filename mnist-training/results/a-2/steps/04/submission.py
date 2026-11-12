import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + intensity ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')   # V = row offset (down), U = col offset (right)
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)
        perp = -U * math.sin(th) + V * math.cos(th)
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = K
        b1[k] = -0.05
    G = np.exp(-(U**2 + V**2) / 2.0)
    G /= G.sum()
    W1[4, 0] = G                      # channel 4: local ink density

    # ---------------- conv2: blur-and-pass-through of channels 0..4 ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    G2 = np.exp(-(U**2 + V**2) / (2 * 1.0**2))
    G2 /= G2.sum()
    for c in range(5):
        W2[c, c] = G2

    # ---------------- stroke descriptions (x=col, y=row) ----------------
    def seg(p0, p1, w=1.0):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(L / 0.5))
        t = (np.arange(n) + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        ang = np.full(n, math.atan2(y1 - y0, x1 - x0))
        ds = np.full(n, w * L / n)
        return x, y, ang, ds

    def arc(cx, cy, rx, ry, t0, t1, w=1.0):
        t0r, t1r = math.radians(t0), math.radians(t1)
        n = max(8, int(abs(t1 - t0) / 3))
        t = t0r + (t1r - t0r) * (np.arange(n) + 0.5) / n
        dt = abs(t1r - t0r) / n
        x = cx + rx * np.cos(t)
        y = cy + ry * np.sin(t)
        dx = -rx * np.sin(t)
        dy = ry * np.cos(t)
        ang = np.arctan2(dy, dx)
        ds = w * np.hypot(dx, dy) * dt
        return x, y, ang, ds

    digits = {
        0: [arc(14, 14, 5.5, 8.5, 0, 360)],
        1: [seg((15, 4.5), (13, 23.5), 0.6), seg((17.5, 5), (10.5, 23), 0.6)],
        2: [arc(14, 10, 5, 5, 180, 390), seg((18.3, 12.5), (9, 22.5)), seg((9, 22.5), (20, 22.5))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [seg((10, 4.5), (8, 16)), seg((8, 16), (20, 16)), seg((17, 5), (17, 23.5))],
        5: [seg((10, 5), (19, 5)), seg((10, 5), (9.5, 13)), arc(13.5, 17.5, 5.5, 5, 228, 510)],
        6: [seg((17, 4.5), (10.5, 12)), seg((10.5, 12), (8.5, 18)), arc(13.5, 18, 5, 4.5, 0, 360)],
        7: [seg((8, 5), (20, 5)), seg((20, 5), (12, 23.5))],
        8: [arc(14, 9, 4, 4.5, 0, 360), arc(14, 18.5, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 4.5, 0, 360), seg((19, 10), (16, 23.5))],
    }

    # ---------------- templates in feature space (expected feature pattern per digit) ----------------
    centers = [4 * i + 7.5 for i in range(4)]
    sigma = 3.0
    T = np.zeros((10, 16, 4, 4))
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes])
        y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes])
        ds = np.concatenate([s[3] for s in strokes])
        for r in range(4):
            for c in range(4):
                prox = np.exp(-((x - centers[c])**2 + (y - centers[r])**2) / (2 * sigma**2)) * ds
                for k, th in enumerate(thetas):
                    tune = np.cos(a - th)**4
                    T[d, k, r, c] = 1 - math.exp(-np.sum(prox * tune) / 3.0)
                T[d, 4, r, c] = 0.5 * (1 - math.exp(-np.sum(prox) / 3.0))
    Tf = T.reshape(10, 256)

    # ---------------- nearest-centroid classifier ----------------
    alpha = 0.4      # estimated feature scale relative to template scale
    s = 12.0         # logit scale
    Wfc = s * alpha * Tf
    bfc = -0.5 * s * alpha**2 * np.sum(Tf**2, axis=1)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
