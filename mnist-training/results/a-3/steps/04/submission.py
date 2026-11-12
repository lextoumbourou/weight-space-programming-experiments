import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors ----------------
    alphas = [k * 45.0 for k in range(8)]   # direction in which ink increases (x right, y down)
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    for k, al in enumerate(alphas):
        a = math.radians(al)
        gx, gy = math.cos(a), math.sin(a)
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                t = dx * gx + dy * gy
                s = -dx * gy + dy * gx
                w[r, c] = t * math.exp(-t * t / 2.0) * math.exp(-s * s / (2 * 1.5 ** 2))
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15

    # ---------------- conv2: pass-through with small blur ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(8):
        W2[j, j, 1:4, 1:4] = K

    # ---------------- stroke skeletons (20x20 box: u=col, v=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48, tilt=0.0):
        pts = []
        for i in range(n + 1):
            t = 2 * math.pi * i / n
            x, y = rx * math.cos(t), ry * math.sin(t)
            xr = x * math.cos(tilt) - y * math.sin(tilt)
            yr = x * math.sin(tilt) + y * math.cos(tilt)
            pts.append((cx + xr, cy + yr))
        return pts

    digits = {
        0: [(1.0, ellipse(10, 10, 6.0, 9.5))],
        1: [(1.0, [(10.5, 0.5), (9.5, 19.5)]),
            (0.5, [(13, 0.5), (7, 19.5)]),
            (0.3, [(15, 0.5), (5, 19.5)])],
        2: [(1.0, [(4, 5), (6, 1.5), (10, 0.5), (14, 1.5), (16, 5), (15, 9), (10, 14), (4, 19.5),
                   (10, 19.5), (17, 19.5)])],
        3: [(1.0, [(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
                   (15, 18), (11, 19.8), (4, 18.5)])],
        4: [(0.8, [(7, 0.5), (5, 7), (4, 12.5), (10, 12.5), (17, 12)]),
            (0.5, [(12, 0.5), (8, 6), (4, 12.5)]),
            (1.0, [(14, 2), (14, 8), (13.5, 19.5)])],
        5: [(1.0, [(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
                   (11, 19.8), (4, 18.5)])],
        6: [(1.0, [(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
                   (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)])],
        7: [(1.0, [(4, 1), (10, 0.5), (16, 0.5), (14, 6), (12, 11), (10, 19.5)]),
            (0.5, [(16, 0.5), (11, 10), (8, 19.5)])],
        8: [(1.0, ellipse(10.5, 5, 4.8, 4.7, tilt=-0.2)), (1.0, ellipse(9.5, 14.7, 5.6, 5, tilt=-0.2))],
        9: [(1.0, ellipse(10, 5.5, 5.5, 5)), (1.0, [(15.5, 5.5), (15, 11), (14, 19.5)]),
            (0.5, [(15.5, 5.5), (13, 12), (10, 19.5)])],
    }

    # sample each digit into points: (x, y, phi, weight*ds), then normalise size and COM
    def sample(strokes):
        pts = []
        for wgt, poly in strokes:
            for (u0, v0), (u1, v1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(u1 - u0, v1 - v0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.4))
                phi = math.atan2(v1 - v0, u1 - u0)
                for i in range(n):
                    s = (i + 0.5) / n
                    pts.append([u0 + s * (u1 - u0), v0 + s * (v1 - v0), phi, wgt * L / n])
        P = np.array(pts)
        # shrink skeleton so skeleton+ink width fits 20 px  (skeleton ~17.5 px tall)
        sc = 0.875
        P[:, 0] = 10 + (P[:, 0] - 10) * sc
        P[:, 1] = 10 + (P[:, 1] - 10) * sc
        P[:, 3] *= sc
        # centre of mass (weighted by ink length) -> pixel (14, 14)
        wsum = P[:, 3].sum()
        cx = (P[:, 0] * P[:, 3]).sum() / wsum
        cy = (P[:, 1] * P[:, 3]).sum() / wsum
        P[:, 0] += 14 - cx
        P[:, 1] += 14 - cy
        return P

    centers = np.array([4 * r + 7.5 for r in range(4)])
    sig = 2.5
    NF = 8
    h = 1.4                                  # half stroke width
    alr = np.radians(alphas)
    T = np.zeros((10, NF, 4, 4))
    for d, strokes in digits.items():
        P = sample(strokes)
        acc = np.zeros((NF, 4, 4))
        for x, y, phi, w in P:
            nx, ny = -math.sin(phi), math.cos(phi)
            for sgn in (+1, -1):
                beta = math.atan2(-sgn * ny, -sgn * nx)     # gradient direction at this edge
                tune = np.maximum(0.0, np.cos(beta - alr)) ** 2
                ex, ey = x + sgn * h * nx, y + sgn * h * ny
                mr = np.exp(-(ey - centers) ** 2 / (2 * sig ** 2))
                mc = np.exp(-(ex - centers) ** 2 / (2 * sig ** 2))
                acc += tune[:, None, None] * np.outer(mr, mc)[None] * w
        T[d] = 1.0 - np.exp(-acc / 1.0)

    # ---------------- fc: nearest-centroid scoring ----------------
    alpha = 0.5          # logit scale
    s = 1.5              # assumed value of a "present" feature
    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    for d in range(10):
        t = T[d].reshape(-1)
        Wfc[d, :NF * 16] = alpha * t / s
        bfc[d] = -alpha * 0.5 * (t ** 2).sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
