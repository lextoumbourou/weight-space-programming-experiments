import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    # Orientation o has line direction theta = o*22.5 deg (x right, y down).
    thetas = np.arange(8) * np.pi / 8
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    yy, xx = np.mgrid[-2:3, -2:3]
    for o in range(8):
        nx, ny = -np.sin(thetas[o]), np.cos(thetas[o])   # unit normal
        d = xx * nx + yy * ny                            # perpendicular distance
        g = np.exp(-d ** 2 / (2 * 1.1 ** 2))
        g -= g.mean()                                    # zero-mean ridge filter
        g /= (g * (np.abs(d) <= 1.25)).sum()             # ideal stroke -> ~1
        w1[o, 0] = g
    b1 = np.full(8, -0.2, np.float32)

    # ---------------- conv2: spatial pooling per orientation ----------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    for o in range(8):
        w2[o, o, 1:4, 1:4] = 1.0     # ch 0-7: broad cells (8-px bands, stride 4)
        w2[8 + o, o, 2, 2] = 1.0     # ch 8-15: sharp cells (4-px bands)
    b2 = np.zeros(16, np.float32)

    # ---------------- stroke primitives (u right, v down, box [-1,1]^2) ----------------
    def line(a, b, n=40):
        t = np.linspace(0, 1, n)[:, None]
        return np.array(a, float)[None] * (1 - t) + np.array(b, float)[None] * t

    def arc(cx, cy, rx, ry, a0, a1, n=120):
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    # each digit: list of shape variants; each variant: list of polylines
    digits = {
        0: [[arc(0, 0, 0.85, 1.0, 0, 360)],
            [arc(0, 0, 0.55, 1.0, 0, 360)]],
        1: [[line((0.0, -1), (0.0, 1))]],
        2: [[arc(0, -0.45, 0.8, 0.55, 180, 380),
             line((0.75, -0.26), (-0.8, 0.95)),
             line((-0.8, 0.95), (0.9, 0.95))]],
        3: [[arc(0, -0.5, 0.75, 0.5, 200, 450),
             arc(0, 0.5, 0.8, 0.5, 270, 520)]],
        4: [[line((-0.25, -1), (-0.8, 0.35)),
             line((-0.8, 0.35), (0.8, 0.35)),
             line((0.45, -0.9), (0.45, 1))],
            [line((-0.7, -1), (-0.7, 0.2)),
             line((-0.7, 0.2), (0.8, 0.2)),
             line((0.4, -1), (0.4, 1))]],
        5: [[line((0.8, -1), (-0.45, -1)),
             line((-0.45, -1), (-0.55, -0.1)),
             arc(-0.05, 0.45, 0.75, 0.55, 240, 510)]],
        6: [[line((0.45, -1), (-0.65, 0.35)),
             arc(0, 0.45, 0.68, 0.55, 0, 360)],
            [arc(0.6, 0.3, 1.25, 1.3, 240, 180, 60) if False else
             arc(0.55, 0.45, 1.2, 1.45, 245, 180),
             arc(0, 0.45, 0.68, 0.55, 0, 360)]],
        7: [[line((-0.8, -1), (0.8, -1)),
             line((0.8, -1), (-0.15, 1))],
            [line((-0.8, -1), (0.7, -1)),
             line((0.7, -1), (0.2, 1))]],
        8: [[arc(0, -0.5, 0.6, 0.5, 0, 360),
             arc(0, 0.5, 0.75, 0.5, 0, 360)]],
        9: [[arc(0, -0.45, 0.7, 0.55, 0, 360),
             line((0.7, -0.45), (0.35, 1))],
            [arc(0, -0.5, 0.7, 0.5, 0, 360),
             line((0.7, -0.5), (0.6, 1))]],
    }

    def soft_band(z, lo, hi):
        # soft membership of coordinates z (N,) in band [lo,hi] -> (N,)
        out = np.maximum(0, np.maximum(lo - z, z - hi))
        return np.clip(1 - out / 2.0, 0, 1)

    def features(polys_xy):
        # expected 16x4x4 feature profile for strokes given in pixel coords
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
        return Fd

    def place(polys, slant, wfac, sx, sy):
        # shear + aspect, then MNIST-like normalisation: box side ~18, COM at (14,14)
        P = []
        for q in polys:
            u, v = q[:, 0] * wfac, q[:, 1]
            P.append(np.stack([u - slant * v / 9.0, v], 1))
        allp = np.concatenate(P)
        lo, hi = allp.min(0), allp.max(0)
        scale = 18.0 / max(hi[0] - lo[0], hi[1] - lo[1])
        # centre of mass weighted by stroke length
        num, den = np.zeros(2), 0.0
        for q in P:
            m = 0.5 * (q[1:] + q[:-1]); w = np.linalg.norm(q[1:] - q[:-1], axis=1)
            num += (m * w[:, None]).sum(0); den += w.sum()
        com = num / den
        return [(q - com) * scale + np.array([14.0 + sx, 14.0 + sy]) for q in P]

    # ---------------- averaged templates over variations ----------------
    F = np.zeros((10, 256))
    slants = [-1.0, 1.5, 4.0]
    wfacs = [0.75, 1.0]
    shifts = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for dgt, variants in digits.items():
        acc = np.zeros((16, 4, 4)); cnt = 0
        for polys in variants:
            for s in slants:
                for wf in wfacs:
                    for (sx, sy) in shifts:
                        acc += features(place(polys, s, wf, sx, sy)); cnt += 1
        F[dgt] = (acc / cnt).reshape(256)      # (channel,row,col) order

    # ---------------- fc: zero-sum, mean-centred, unit-norm templates ----------------
    Fv = F / (np.linalg.norm(F, axis=1, keepdims=True) + 1e-8)
    D = Fv - Fv.mean(axis=0, keepdims=True)   # remove what all digits share
    D = D - D.mean(axis=1, keepdims=True)     # each template sums to zero
    D /= np.linalg.norm(D, axis=1, keepdims=True) + 1e-8
    alpha = 1.0
    wfc = (alpha * D).astype(np.float32)
    bfc = np.zeros(10, np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2,
        "conv2.bias": b2,
        "fc.weight": wfc,
        "fc.bias": bfc,
    }
