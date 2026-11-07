## Step 10: settle κ between the last two runs

**What the κ runs show.** κ = 0.35 sent almost everything to 8, and κ = 0.6 makes 8 rare (268 correct, about 450 predictions in total). The right value lies in between, so I try 0.47. The per-class bias corrections carried over from step 5 stay, scaled to the new β.

**Confidence.** The loss rose from 1.11 to 1.30 at the same accuracy. The blurred features are larger, so the logits grew and wrong predictions became over-confident. I lower β from 2.5 to 2.0.

Everything else (features, templates, loop and concavity channels) is unchanged. That isolates the effect of recalibration before I go back to template work.

```python
import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1: ch0-3 oriented line detectors, ch4 ink (blur), ch5 background
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]          # 0=horizontal, 45='\', 90=vertical, 135='/'
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))   # Mexican hat across line
        w = w - w.mean()
        w = w / w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()
    W1[4, 0] = g                 # ink presence
    b1[4] = -0.1
    W1[5, 0] = -3.3 * g          # background: ReLU(1 - 3.3*blur)
    b1[5] = 1.0

    # ------------------------------------------------------------------
    # conv2: ch0-4 3x3-blurred pass-through; ch5 HB, ch6 VB
    # ------------------------------------------------------------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3
    W2[5, 5, 2, 2] = 1.0
    for cc in (0, 1, 3, 4):
        W2[5, 4, 2, cc] = 0.5
    b2[5] = -1.6
    W2[6, 5, 2, 2] = 1.0
    for rr in (0, 1, 3, 4):
        W2[6, 4, rr, 2] = 0.5
    b2[6] = -1.6

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (x=col, y=row); variants per digit
    # ------------------------------------------------------------------
    def ell(cx, cy, rx, ry, a0=0.0, a1=360.0, n=28):
        a = np.radians(np.linspace(a0, a1, n))
        return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in a]

    digits = {
        0: [[ell(14, 14, 5.5, 8.5)],
            [ell(14, 14, 6.5, 8.5)],
            [[(15 - 1.5 * math.sin(t) + 6 * math.cos(t), 14 + 8.5 * math.sin(t))
              for t in np.radians(np.linspace(0, 360, 28))]]],
        1: [[[(15.5, 5), (12.5, 23)]],
            [[(14, 5), (14, 23)]],
            [[(17, 5), (11, 23)]]],
        2: [[[(9, 9), (10.5, 6), (14, 5), (17.5, 6), (19, 9), (18, 12), (15, 15.5),
              (11, 19.5), (9, 22), (14, 22), (20, 22)]],
            [[(9, 8), (12, 5), (16, 5), (18.5, 7.5), (17.5, 11), (9, 22), (20, 22)]]],
        3: [[[(9, 6), (13, 5), (17, 5.5), (19, 8), (18, 11), (14, 13.5), (18, 15.5),
              (19.5, 18.5), (18, 21.5), (14, 23), (9, 22)]],
            [[(10, 5), (18, 5), (13, 12.5), (18, 14.5), (19.5, 18), (17, 22), (13, 23), (9, 21)]]],
        4: [[[(10, 5), (9.5, 15), (20, 15)], [(18, 5), (17, 23)]],
            [[(16, 5), (9, 16), (20, 16)], [(17, 8), (17, 23)]]],
        5: [[[(19, 5), (11, 5), (10, 13), (14, 12), (18, 13.5), (19.5, 17), (18, 21),
              (14, 23), (9, 21.5)]],
            [[(19, 5), (12, 5.5), (11, 12), (15, 11.5), (18.5, 14), (18.5, 19), (15, 22.5),
              (10, 22)]]],
        6: [[[(17, 5), (13, 8), (10.5, 12), (9.5, 16), (10, 20), (13, 23), (16.5, 22.5),
              (18.5, 19), (17.5, 15.5), (14, 14), (10.5, 16)]],
            [[(16, 5), (12, 11), (10, 17), (11, 21.5), (14.5, 23), (18, 21), (18, 17),
              (15, 15), (11, 17)]]],
        7: [[[(9, 5), (19.5, 5), (17, 11), (14.5, 17), (13, 23)]],
            [[(9, 6), (19, 5), (15, 14), (12, 23)]]],
        8: [[ell(14, 9.5, 4.0, 4.2), ell(14, 18.5, 5.0, 4.5)],
            [ell(15, 9.5, 4.0, 4.2), ell(13, 18.5, 5.0, 4.5)]],
        9: [[ell(14, 9.5, 4.5, 4.3), [(18.5, 10), (17.5, 16), (16, 23)]],
            [ell(14.5, 9.5, 4.5, 4.3), [(19, 10), (15, 23)]]],
    }

    def cov(v, i):
        lo, hi = 4 * i + 5.0, 4 * i + 10.0
        dist = max(lo - v, 0.0, v - hi)
        return max(0.0, 1.0 - dist / 3.0)

    def render(polys):
        T = np.zeros((5, 4, 4))
        for P in polys:
            P = np.array(P, float)
            for a, b in zip(P[:-1], P[1:]):
                dx, dy = b - a
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(dy, dx)
                o = [max(0.0, math.cos(2 * (phi - math.radians(th)))) for th in thetas]
                n = max(2, int(L / 0.5) + 1)
                for t in np.linspace(0, 1, n):
                    x, y = a + t * (b - a)
                    hy = [cov(y, i) for i in range(4)]
                    hx = [cov(x, j) for j in range(4)]
                    for i in range(4):
                        for j in range(4):
                            sp = hy[i] * hx[j]
                            if sp <= 0:
                                continue
                            for k in range(4):
                                T[k, i, j] = max(T[k, i, j], o[k] * sp)
                            T[4, i, j] = max(T[4, i, j], sp)
        return T

    # Hand-written expected presence of HB / VB per 4x4 cell
    Z = lambda: np.zeros((4, 4))
    HB = {d: Z() for d in range(10)}
    VB = {d: Z() for d in range(10)}
    HB[0][:, 1:3] = np.array([[0.5], [0.9], [0.9], [0.5]])
    VB[0][1:3, 1:3] = 0.2
    VB[2][3, 2:4] = 0.6; VB[2][2, 3] = 0.3
    VB[2][3, 0:2] = 0.2; HB[2][3, 0:2] = 0.2
    VB[3][0, 1] = 0.7; VB[3][1, 1] = 0.5; VB[3][0, 0] = 0.3; VB[3][1, 0] = 0.3
    VB[3][2, 1] = 0.5; VB[3][3, 1] = 0.6; VB[3][2, 0] = 0.3; VB[3][3, 0] = 0.3
    HB[4][0:2, 1:3] = 0.8
    VB[4][1, 2] = 0.3
    VB[5][0, 2] = 0.6; VB[5][0, 3] = 0.5; VB[5][1, 2] = 0.3; VB[5][1, 3] = 0.3
    VB[5][2, 0] = 0.3; VB[5][2, 1] = 0.4; VB[5][3, 1] = 0.3
    HB[6][2, 1:3] = 0.6; HB[6][3, 1:3] = 0.5
    VB[6][2, 1:3] = 0.5; VB[6][3, 1:3] = 0.5
    HB[8][0:2, 1:3] = 0.5; HB[8][2:4, 1:3] = 0.5
    VB[8][0:2, 1:3] = 0.5; VB[8][2:4, 1:3] = 0.5
    VB[8][1:3, 0] = 0.3; VB[8][1:3, 3] = 0.3
    HB[9][0:2, 1:3] = 0.6
    VB[9][0:2, 1:3] = 0.6

    emph = [
        (7, 0, slice(0, 1), slice(0, 4), 1.6),
        (2, 0, slice(3, 4), slice(0, 4), 1.6),
        (5, 2, slice(0, 2), slice(0, 2), 1.5),
        (5, 0, slice(0, 1), slice(0, 4), 1.3),
        (1, 2, slice(0, 4), slice(1, 3), 1.3),
    ]

    # ------------------------------------------------------------------
    # fc: logit_d = beta*(f.T_d - kappa/2 ||T_d||^2) + bias correction
    # kappa between the two previous runs; beta lowered (overconfident)
    # ------------------------------------------------------------------
    beta, kappa = 2.0, 0.47
    bias_adj = np.array([-0.25, 0.0, 0.0, 0.0, 0.5, 0.25, -0.375, 0.0, 0.5, -0.125]) * (2.0 / 1.5)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        T = np.mean([render(v) for v in digits[d]], axis=0)
        for (dd, c, rs, cs, fac) in emph:
            if dd == d:
                T[c, rs, cs] *= fac
        full = np.zeros((16, 4, 4))
        full[:5] = T
        full[5] = HB[d]
        full[6] = VB[d]
        Wf[d] = beta * full.reshape(-1)
        bf[d] = -beta * kappa * 0.5 * np.sum(full ** 2) + bias_adj[d]

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
