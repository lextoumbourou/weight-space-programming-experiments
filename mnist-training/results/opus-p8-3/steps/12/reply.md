## Step 12: make the loop detectors actually fire

**Step 11 result.** Correlation scoring gave a small gain: loss 1.036 and accuracy 67.4%. The biggest confusions are now 7→9 (272), 2→8 (186), 8→2, 5→6 (163), 3→5 (159), 9→8 (142) and 7→2 (135). Nearly all of these hinge on whether a digit has a closed loop, and where.

**Why the loop features were dead.** I re-checked the "between strokes" detectors and they almost never fire inside small loops (6, 8, 9).
- The background channel ReLU(1 − 3.3·blur) is already close to 0 a couple of pixels from a stroke.
- The bias of −1.6 then requires an unrealistically strong match.
- This explains why adding HB and VB in step 7 changed nothing.

**What changes.**
- **conv1, background channel.** It becomes ReLU(1 − 1.5·blur), which is about 1 inside a 3–5 px hole and 0 on a stroke.
- **conv2, five topology channels.** Each has the form ReLU(bg_centre + Σ ink taps − θ). The thresholds are set so that one side alone, or a solid stroke, stays below θ.
  - ch5 **HB2**: ink 4 px left and 4 px right of a background point, for wide gaps (0, open 4).
  - ch6 **VB2**: ink 4 px above and 4 px below, for wide pockets (3, 5, 2).
  - ch7 **HB1**: ink 2 px left and 2 px right, for small loops (6, 8, 9).
  - ch8 **VB1**: ink 2 px above and 2 px below, for small loops.
  - ch9 **LOOP**: background with ink 2 px away on all four sides, a true hole detector.
- **fc.** I add hand-written expected-presence tables for each new channel. These channels get 1.5× weight in the templates because they target exactly the current confusions. The correlation classifier is kept.

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
    W1[4, 0] = g                 # ink presence (~0.6-0.8 on a stroke)
    b1[4] = -0.1
    W1[5, 0] = -1.5 * g          # background: ReLU(1 - 1.5*blur): ~1 in holes, 0 on strokes
    b1[5] = 1.0

    # ------------------------------------------------------------------
    # conv2:
    #   ch0-4 : 3x3-blurred pass-through of orientation / ink
    #   ch5 HB2 : bg centre & ink at pool1 offsets (2,0),(2,4)  (gap ~8 px wide)
    #   ch6 VB2 : bg centre & ink at (0,2),(4,2)
    #   ch7 HB1 : bg centre & ink at (2,1),(2,3)                (gap ~4-6 px)
    #   ch8 VB1 : bg centre & ink at (1,2),(3,2)
    #   ch9 LOOP: bg centre & ink at all four of (1,2),(3,2),(2,1),(2,3)
    # pool1 channel 4 = ink, 5 = background
    # ------------------------------------------------------------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def pair_detector(ch, taps):
        W2[ch, 5, 2, 2] = 1.0
        for (r, c) in taps:
            W2[ch, 4, r, c] = 1.0
        b2[ch] = -1.8            # bg(~0.8) + two inked taps (~1.4) - 1.8 ~ 0.4

    pair_detector(5, [(2, 0), (2, 4)])
    pair_detector(6, [(0, 2), (4, 2)])
    pair_detector(7, [(2, 1), (2, 3)])
    pair_detector(8, [(1, 2), (3, 2)])
    W2[9, 5, 2, 2] = 1.0
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        W2[9, 4, r, c] = 0.6
    b2[9] = -2.2                 # needs background + ink on ~all four sides

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

    # ------------------------------------------------------------------
    # Hand-written expected presence of topology features per 4x4 cell
    # (rows: input rows 6-9,10-13,14-17,18-21; cols same)
    # ------------------------------------------------------------------
    Z = lambda: np.zeros((4, 4))
    HB2 = {d: Z() for d in range(10)}
    VB2 = {d: Z() for d in range(10)}
    HB1 = {d: Z() for d in range(10)}
    VB1 = {d: Z() for d in range(10)}
    LP = {d: Z() for d in range(10)}
    # wide horizontal gaps
    HB2[0][:, 1:3] = np.array([[0.4], [0.8], [0.8], [0.4]])
    HB2[4][0:2, 1:3] = 0.7
    # wide vertical pockets
    VB2[0][1:3, 1:3] = 0.2
    VB2[2][3, 2:4] = 0.5; VB2[2][2, 3] = 0.3
    VB2[3][0:2, 0:2] = np.array([[0.3, 0.6], [0.3, 0.4]])
    VB2[3][2:4, 0:2] = np.array([[0.3, 0.4], [0.3, 0.6]])
    VB2[5][0:2, 2:4] = np.array([[0.6, 0.5], [0.3, 0.3]])
    VB2[5][2:4, 0:2] = np.array([[0.3, 0.4], [0.2, 0.3]])
    # small loops / narrow gaps
    for d, cells, v in [(6, [(2, 1), (2, 2), (3, 1), (3, 2)], 0.5),
                        (8, [(0, 1), (0, 2), (1, 1), (1, 2)], 0.45),
                        (8, [(2, 1), (2, 2), (3, 1), (3, 2)], 0.45),
                        (9, [(0, 1), (0, 2), (1, 1), (1, 2)], 0.6),
                        (0, [(1, 1), (1, 2), (2, 1), (2, 2)], 0.3),
                        (4, [(0, 1), (0, 2), (1, 1), (1, 2)], 0.25),
                        (2, [(3, 0), (3, 1)], 0.15)]:
        for (i, j) in cells:
            HB1[d][i, j] = max(HB1[d][i, j], v)
            VB1[d][i, j] = max(VB1[d][i, j], v * (0.6 if d in (0, 4) else 1.0))
            LP[d][i, j] = max(LP[d][i, j], v * (0.3 if d in (0, 4, 2) else 0.8))
    VB1[3][0, 1] = 0.3; VB1[3][3, 1] = 0.3
    VB1[5][0, 2] = 0.2

    emph = [
        (7, 0, slice(0, 1), slice(0, 4), 1.6),
        (2, 0, slice(3, 4), slice(0, 4), 1.6),
        (5, 2, slice(0, 2), slice(0, 2), 1.5),
        (5, 0, slice(0, 1), slice(0, 4), 1.3),
        (1, 2, slice(0, 4), slice(1, 3), 1.3),
    ]

    def smooth_spatial(M):
        P = np.pad(M, 1, mode='edge')
        return 0.6 * M + 0.1 * (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:])

    topo_w = 1.5       # extra importance of topology channels
    temps = []
    for d in range(10):
        T = np.mean([render(v) for v in digits[d]], axis=0)
        for (dd, c, rs, cs, fac) in emph:
            if dd == d:
                T[c, rs, cs] *= fac
        full = np.zeros((16, 4, 4))
        full[:5] = T
        full[5] = topo_w * HB2[d]
        full[6] = topo_w * VB2[d]
        full[7] = topo_w * HB1[d]
        full[8] = topo_w * VB1[d]
        full[9] = topo_w * LP[d]
        O = full[:4].copy()
        for k in range(4):
            full[k] = 0.7 * O[k] + 0.15 * (O[(k - 1) % 4] + O[(k + 1) % 4])
        for c in range(10):
            full[c] = smooth_spatial(full[c])
        temps.append(full.reshape(-1))
    temps = np.array(temps)

    # ------------------------------------------------------------------
    # fc: correlation classifier
    #   U_d = (T_d - Tbar)/||T_d - Tbar||;  logit_d = beta*(f.U_d - kappa*Tbar.U_d)
    # ------------------------------------------------------------------
    beta, kappa = 4.0, 0.47
    Tbar = temps.mean(axis=0)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        U = temps[d] - Tbar
        U = U / np.linalg.norm(U)
        Wf[d] = beta * U
        bf[d] = -beta * kappa * float(Tbar @ U)

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
