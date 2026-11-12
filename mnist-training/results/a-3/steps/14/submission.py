import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors ----------------
    # channel k responds where ink increases along direction k*45 deg (x right, y down)
    alphas = [k * 45.0 for k in range(8)]
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

    # ---------------- conv2: 4 cardinal directions x 4 spatial shifts ----------------
    # direction D in {0:+x, 1:+y, 2:-x, 3:-y} uses conv1 ch 2D (weight 1) and its diagonal
    # neighbours 2D+-1 (weight 0.5). Single tap at (1+a, 1+b): shifts grid by 2a, 2b px.
    # channel index = 4*D + 2*a + b
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for D in range(4):
        kc = 2 * D
        for a in range(2):
            for b in range(2):
                ch = 4 * D + 2 * a + b
                W2[ch, kc, 1 + a, 1 + b] = 1.0
                W2[ch, (kc + 1) % 8, 1 + a, 1 + b] = 0.5
                W2[ch, (kc - 1) % 8, 1 + a, 1 + b] = 0.5

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
        0: [(1.0, ellipse(10, 10, 6.5, 9.5, tilt=0.2))],
        1: [(1.0, [(12.5, 0.5), (8.5, 19.5)]),
            (0.5, [(10, 0.5), (10, 19.5)]),
            (0.4, [(15, 0.5), (6, 19.5)])],
        2: [(1.0, [(4.5, 4.5), (6.5, 1.5), (10, 0.3), (13.5, 1), (15.5, 3.5), (15.5, 7), (13, 10.5),
                   (9, 14), (5, 18), (4, 19.5), (8, 19), (12, 19), (17, 19.5)])],
        3: [(1.0, [(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
                   (15, 18), (11, 19.8), (4, 18.5)])],
        4: [(1.0, [(6, 1), (5, 7), (4, 13)]),
            (1.0, [(4, 13), (10, 12.8), (17, 12.5)]),
            (1.0, [(14, 1), (13.5, 10), (13, 20)]),
            (0.4, [(13, 1), (8, 7), (4, 13)])],
        5: [(1.0, [(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
                   (11, 19.8), (4, 18.5)])],
        6: [(1.0, [(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
                   (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)])],
        7: [(1.0, [(3.5, 1.5), (10, 1), (16.5, 0.5)]),
            (1.0, [(16.5, 0.5), (13, 7), (10, 14), (8.5, 19.5)])],
        8: [(1.0, ellipse(10.5, 5, 4.8, 4.7, tilt=-0.2)), (1.0, ellipse(9.5, 14.7, 5.6, 5, tilt=-0.2))],
        9: [(1.0, ellipse(10, 5.5, 5.5, 5)), (1.0, [(15.5, 5.5), (15, 11), (14, 19.5)]),
            (0.5, [(15.5, 5.5), (13, 12), (10, 19.5)])],
    }

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
        sc = 0.875
        P[:, 0] = 10 + (P[:, 0] - 10) * sc
        P[:, 1] = 10 + (P[:, 1] - 10) * sc
        P[:, 3] *= sc
        wsum = P[:, 3].sum()
        cx = (P[:, 0] * P[:, 3]).sum() / wsum
        cy = (P[:, 1] * P[:, 3]).sum() / wsum
        P[:, 0] += 14 - cx
        P[:, 1] += 14 - cy
        return P

    # ---------------- templates on the interleaved 8x8 grid ----------------
    sig = 1.8
    h = 1.4
    Dang = np.radians([0.0, 90.0, 180.0, 270.0])
    # fine-grid centres: index g = 2r + a  -> centre 4r + 5.5 + 2a = 5.5 + 2g
    gcent = np.array([5.5 + 2 * g for g in range(8)])
    T = np.zeros((10, 16, 4, 4))
    for d, strokes in digits.items():
        P = sample(strokes)
        acc = np.zeros((4, 8, 8))             # direction x fine row x fine col
        for x, y, phi, w in P:
            nx, ny = -math.sin(phi), math.cos(phi)
            for sgn in (+1, -1):
                beta = math.atan2(-sgn * ny, -sgn * nx)       # gradient dir at this edge
                tune = np.maximum(0.0, np.cos(beta - Dang))
                ex, ey = x + sgn * h * nx, y + sgn * h * ny
                mr = np.exp(-(ey - gcent) ** 2 / (2 * sig ** 2))
                mc = np.exp(-(ex - gcent) ** 2 / (2 * sig ** 2))
                acc += tune[:, None, None] * np.outer(mr, mc)[None] * w
        Tf = 1.0 - np.exp(-acc / 1.0)
        for D in range(4):
            for a in range(2):
                for b in range(2):
                    ch = 4 * D + 2 * a + b
                    T[d, ch] = Tf[D, a::2, b::2]   # fine (2r+a, 2c+b) -> channel cell (r, c)

    # ---------------- fc: multinomial naive Bayes ----------------
    gamma = 0.14
    eps = 0.02
    LQ = np.zeros((10, 256))
    for d in range(10):
        q = T[d].reshape(-1) + eps
        q = q / q.sum()
        LQ[d] = np.log(q)
    LQ -= LQ.mean(axis=0, keepdims=True)
    Wfc = gamma * LQ

    bfc = 0.6 * np.array([0.229, -0.612, 0.853, 0.846, 0.146, 0.733, -0.084, 0.19, -0.214, -0.474])

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
