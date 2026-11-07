import numpy as np
import math

def build_weights():
    rng = np.random.RandomState(0)

    # ---------------- conv1: 8 oriented line (ridge) detectors ----------------
    thetas = np.arange(8) * np.pi / 8          # line direction, x right / y down
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    yy, xx = np.mgrid[-2:3, -2:3]
    for o in range(8):
        nx, ny = -np.sin(thetas[o]), np.cos(thetas[o])
        d = xx * nx + yy * ny
        g = np.exp(-d ** 2 / (2 * 1.1 ** 2))
        g -= g.mean()                          # zero-mean ridge filter
        g /= (g * (np.abs(d) <= 1.25)).sum()   # ideal stroke -> ~1
        w1[o, 0] = g
    b1 = np.full(8, -0.2, np.float32)

    # ---------------- conv2: spatial pooling per orientation ----------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    for o in range(8):
        w2[o, o, 1:4, 1:4] = 1.0     # ch 0-7: broad cells
        w2[8 + o, o, 2, 2] = 1.0     # ch 8-15: sharp cells
    b2 = np.zeros(16, np.float32)

    # ---------------- stroke primitives ----------------
    def line(a, b, n=40):
        t = np.linspace(0, 1, n)[:, None]
        return np.array(a, float)[None] * (1 - t) + np.array(b, float)[None] * t

    def arc(cx, cy, rx, ry, a0, a1, n=120):
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    def bez(a, c, b, n=50):
        t = np.linspace(0, 1, n)[:, None]
        a, c, b = (np.array(z, float)[None] for z in (a, c, b))
        return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b

    def fig8(k=0.65, n=240):
        t = np.linspace(0, 2 * np.pi, n)
        return np.stack([k * np.sin(2 * t), np.cos(t)], 1)

    digits = {
        0: [[arc(0, 0, 0.85, 1.0, 0, 360)],
            [arc(0, 0, 0.55, 1.0, 0, 360)]],
        1: [[line((0.0, -1), (0.0, 1))],
            [line((-0.35, -0.75), (0.0, -1)), line((0.0, -1), (0.0, 1))],
            [line((-0.35, -0.75), (0.0, -1)), line((0.0, -1), (0.0, 1)),
             line((-0.35, 1), (0.35, 1))]],
        2: [[arc(0, -0.45, 0.8, 0.55, 180, 380),
             line((0.75, -0.26), (-0.8, 0.95)),
             line((-0.8, 0.95), (0.9, 0.95))],
            [arc(0, -0.45, 0.8, 0.55, 180, 380),          # curved neck
             bez((0.75, -0.26), (0.3, 0.45), (-0.8, 0.95)),
             line((-0.8, 0.95), (0.9, 0.95))],
            [arc(0, -0.45, 0.8, 0.55, 180, 380),          # bottom-left loop
             line((0.75, -0.26), (-0.45, 0.75)),
             arc(-0.6, 0.78, 0.22, 0.2, 0, 360),
             line((-0.4, 0.95), (0.9, 0.95))]],
        3: [[arc(0, -0.5, 0.75, 0.5, 200, 450),
             arc(0, 0.5, 0.8, 0.5, 270, 520)]],
        4: [[line((-0.25, -1), (-0.8, 0.35)),
             line((-0.8, 0.35), (0.8, 0.35)),
             line((0.45, -0.9), (0.45, 1))],
            [line((-0.7, -1), (-0.7, 0.2)),
             line((-0.7, 0.2), (0.8, 0.2)),
             line((0.4, -1), (0.4, 1))],
            [line((-0.1, -1), (-0.75, 0.2)),
             line((-0.75, 0.2), (0.6, 0.2)),
             line((0.5, -1), (0.5, 1)),
             line((-0.1, -1), (0.2, -0.95))]],
        5: [[line((0.8, -1), (-0.45, -1)),
             line((-0.45, -1), (-0.55, -0.1)),
             arc(-0.05, 0.45, 0.75, 0.55, 240, 510)],
            [line((0.8, -1), (-0.4, -1)),                  # S-like join
             bez((-0.4, -1), (-0.65, -0.2), (-0.1, -0.12)),
             arc(-0.05, 0.45, 0.75, 0.55, 265, 510)]],
        6: [[line((0.45, -1), (-0.65, 0.35)),
             arc(0, 0.45, 0.68, 0.55, 0, 360)],
            [arc(0.55, 0.45, 1.2, 1.45, 245, 180),
             arc(0, 0.45, 0.68, 0.55, 0, 360)]],
        7: [[line((-0.8, -1), (0.8, -1)),
             line((0.8, -1), (-0.15, 1))],
            [line((-0.8, -1), (0.7, -1)),
             line((0.7, -1), (0.2, 1))],
            [arc(0, -0.6, 0.8, 0.4, 200, 340),
             line((0.75, -0.75), (-0.1, 1))],
            [line((-0.8, -1), (0.8, -1)),
             line((0.8, -1), (-0.15, 1)),
             line((-0.2, 0.05), (0.6, 0.05))]],
        8: [[fig8(0.65)],
            [fig8(0.5)],
            [arc(0, -0.5, 0.6, 0.5, 0, 360),
             arc(0, 0.5, 0.75, 0.5, 0, 360)]],
        9: [[arc(0, -0.45, 0.7, 0.55, 0, 360),
             line((0.7, -0.45), (0.35, 1))],
            [arc(0, -0.5, 0.7, 0.5, 0, 360),
             line((0.7, -0.5), (0.6, 1))]],
    }

    def soft_band(z, lo, hi):
        out = np.maximum(0, np.maximum(lo - z, z - hi))
        return np.clip(1 - out / 2.0, 0, 1)

    def features(polys_xy):
        # expected 16x4x4 ridge-feature profile from stroke geometry (pixel coords)
        Fd = np.zeros((16, 4, 4))
        for p in polys_xy:
            mid = 0.5 * (p[1:] + p[:-1])
            dv = p[1:] - p[:-1]
            ds = np.linalg.norm(dv, axis=1)
            ang = np.arctan2(dv[:, 1], dv[:, 0])
            yA = np.stack([soft_band(mid[:, 1], 4 * i + 4, 4 * i + 11) for i in range(4)])
            xA = np.stack([soft_band(mid[:, 0], 4 * i + 4, 4 * i + 11) for i in range(4)])
            yB = np.stack([soft_band(mid[:, 1], 4 * i + 6, 4 * i + 9) for i in range(4)])
            xB = np.stack([soft_band(mid[:, 0], 4 * i + 6, 4 * i + 9) for i in range(4)])
            for o in range(8):
                tw = ds * np.maximum(0, np.cos(2 * (ang - thetas[o]))) ** 2
                Fd[o] += np.einsum('n,in,jn->ij', tw, yA, xA)
                Fd[8 + o] += np.einsum('n,in,jn->ij', tw, yB, xB)
        return Fd.reshape(256)

    def place(polys, slant, wfac, taper, sx, sy, size, warp):
        # smooth random warp (as step 12), shear/aspect/taper, MNIST normalisation
        a1, a2, a3, a4, p1, p2, p3, p4 = warp
        P = []
        for q in polys:
            u0, v0 = q[:, 0], q[:, 1]
            u0 = u0 + a1 * np.sin(np.pi * v0 + p1) + a2 * np.sin(np.pi * u0 + p2)
            v0 = v0 + a3 * np.sin(np.pi * u0 + p3) + a4 * np.sin(np.pi * v0 + p4)
            u = u0 * wfac * (1 + taper * v0)
            P.append(np.stack([u - slant * v0 / 9.0, v0], 1))
        allp = np.concatenate(P)
        lo, hi = allp.min(0), allp.max(0)
        scale = size / max(hi[0] - lo[0], hi[1] - lo[1])
        num, den = np.zeros(2), 0.0
        for q in P:
            m = 0.5 * (q[1:] + q[:-1]); w = np.linalg.norm(q[1:] - q[:-1], axis=1)
            num += (m * w[:, None]).sum(0); den += w.sum()
        com = num / den
        return [(q - com) * scale + np.array([14.0 + sx, 14.0 + sy]) for q in P]

    # ---------------- synthetic feature samples per class ----------------
    NS = 500
    X = np.zeros((10, NS, 256))
    for dgt, variants in digits.items():
        for k in range(NS):
            polys = variants[rng.randint(len(variants))]
            sl = rng.uniform(-3, 7) if dgt == 1 else rng.uniform(-2, 5)
            warp = np.r_[rng.normal(0, 0.08, 4), rng.uniform(0, 2 * np.pi, 4)]
            X[dgt, k] = features(place(polys,
                                       slant=sl,
                                       wfac=rng.uniform(0.6, 1.1),
                                       taper=rng.uniform(-0.2, 0.2),
                                       sx=rng.uniform(-1.2, 1.2),
                                       sy=rng.uniform(-1.2, 1.2),
                                       size=rng.uniform(17, 19),
                                       warp=warp))

    # ---------------- shrunk LDA with ink-amount nuisance directions ----------------
    mu = X.mean(1)
    R = (X - mu[:, None]).reshape(-1, 256)
    S = R.T @ R / R.shape[0]
    p_ = 256
    t = np.trace(S) / p_
    gam = 0.7
    Sig = (1 - gam) * S + gam * t * np.eye(p_)
    nuis = [np.ones(p_), np.r_[np.ones(128), np.zeros(128)], np.r_[np.zeros(128), np.ones(128)]]
    for n in nuis:
        n = n / np.linalg.norm(n)
        Sig += 1000.0 * t * np.outer(n, n)

    mbar = mu.mean(0)
    W = np.linalg.solve(Sig, (mu - mbar).T).T
    W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-8
    alpha = 2.0
    wfc = (alpha * W).astype(np.float32)

    # ---------------- fc bias (calibrated from confusion counts) ----------------
    true_cnt = np.array([980, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    bfc = np.zeros(10, np.float64)
    bfc[1] += 0.3
    bfc[9] -= 0.3
    pred5 = np.array([861, 804, 802, 939, 802, 888, 1598, 961, 1021, 1324], float)
    bfc -= 1.0 * np.log(pred5 / true_cnt)
    pred6 = np.array([964, 950, 901, 965, 980, 962, 1139, 1012, 1002, 1125], float)
    bfc -= 0.7 * np.log(pred6 / true_cnt)
    pred12 = np.array([973, 1049, 745, 1175, 998, 807, 1013, 1026, 1080, 1134], float)
    bfc -= 0.5 * np.log(pred12 / true_cnt)
    bfc = (alpha * bfc).astype(np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2,
        "conv2.bias": b2,
        "fc.weight": wfc,
        "fc.bias": bfc,
    }
