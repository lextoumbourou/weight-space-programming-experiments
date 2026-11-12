## Step 18: rebalance the biases for the new features

**Step 17 result.** Adding endpoint detectors improved several classes a lot: 4 went from 724 to 931 correct, 7 to 905 and 1 to 927. Overall accuracy was 72.7%, but loss rose slightly to 0.92, because the per-class biases were tuned for the old features. Prediction counts are now off in new ways:

| Predicted class | Times predicted |
|---|---|
| 7 | 1240 |
| 4 | 1234 |
| 1 | 1125 |
| 8 | 1107 |
| 2 | 1051 |
| 9 | 665 |
| 3 | 757 |

**Change.** Templates and features stay exactly as in step 17; only the biases move:
- **Raised:** 9 by 0.5, 3 by 0.4.
- **Lowered:** 4 by 0.4, 7 by 0.3, 8 by 0.2, and 1 and 2 by 0.1 each.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1 =================
    # ch 0..3: oriented line detectors (0=horiz, 45='/', 90=vert, 135='\')
    # ch 4..7: endpoint detectors, tip pointing up / down / left / right
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]
    dirs = []
    for th in thetas:
        t = math.radians(th)
        dirs.append((-math.sin(t), math.cos(t)))   # unit direction (row, col), row grows downward

    def profile(d):
        if d <= 0.5:
            return 1.0
        if d <= 1.0:
            return 1.0 - 0.8 * (d - 0.5)
        if d <= 2.0:
            return 0.6 - 1.1 * (d - 1.0)
        return -0.5

    for f, (dr, dc) in enumerate(dirs):
        w = np.zeros((5, 5))
        dist = np.zeros((5, 5))
        for u in range(-2, 3):
            for v in range(-2, 3):
                d = abs(u * dc - v * dr)
                dist[u + 2, v + 2] = d
                w[u + 2, v + 2] = profile(d)
        w = w / w[dist <= 1.5].sum()   # ideal 3-px stroke -> response 1
        W1[f, 0] = w
        b1[f] = -0.2

    tips = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right
    for e, (pr, pc) in enumerate(tips):
        w = np.zeros((5, 5))
        for u in range(-2, 3):
            for v in range(-2, 3):
                a = u * pr + v * pc          # >0 : beyond the tip (must be empty)
                q = abs(u * pc - v * pr)     # distance across the stroke
                if q == 2:
                    w[u + 2, v + 2] = -0.5
                else:
                    base = 1.0 if q == 0 else 0.5
                    w[u + 2, v + 2] = base * (1.0 if a <= 0 else -1.5)
        W1[4 + e, 0] = w / 6.0               # ideal tip -> ~1, continuing stroke -> 0
        b1[4 + e] = -0.25

    # ================= conv2: checkerboard tap selection =================
    # map m (0..7) uses taps (1+q,1+q), q in {0,1}; channel c = 2*m + q.
    # pool2 cell (sr,sc) -> grid Y=2*sr+q, X=2*sc+q ; covers detector centres rows 2Y+4..2Y+7
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for m in range(8):
        for q in range(2):
            W2[2 * m + q, m, 1 + q, 1 + q] = 1.0

    # ================= stroke drawing =================
    # piece = (points, closed); point = (r, c, dr, dc, arc_weight, gain)
    def poly(pts, g=1.0, step=0.5):
        out = []
        for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
            L = math.hypot(r1 - r0, c1 - c0)
            n = max(1, int(L / step))
            for i in range(n + 1):
                a = i / n
                out.append((r0 + a * (r1 - r0), c0 + a * (c1 - c0), r1 - r0, c1 - c0, L / (n + 1), g))
        return (out, False)

    def ellipse(cr, cc, rr, rc, n=80, g=1.0, gleft=None):
        out = []
        dt = 2 * math.pi / n
        for i in range(n):
            t = dt * i
            dr, dc = rr * math.sin(t), rc * math.cos(t)
            gg = gleft if (gleft is not None and math.sin(t) < 0) else g
            out.append((cr - rr * math.cos(t), cc + rc * math.sin(t), dr, dc,
                        math.hypot(dr, dc) * dt, gg))
        return (out, True)

    variants = {
        0: [[ellipse(14, 14, 9, 6.5)], [ellipse(14, 14, 9, 5)], [ellipse(14, 14, 8.5, 7.5)]],
        1: [[poly([(4, 14), (23, 14)])],
            [poly([(7, 11), (4, 14), (23, 14)])]],
        2: [[poly([(8, 8), (5, 11), (4, 14), (5, 18), (8, 19), (11, 18), (15, 14), (19, 10), (23, 8)]),
             poly([(23, 8), (23, 14), (23, 20)], g=1.3)],
            [poly([(7, 7), (4, 11), (4, 16), (7, 19), (11, 18), (16, 13), (21, 8), (23, 7)]),
             poly([(23, 7), (23, 13), (22, 20)], g=1.3)],
            [poly([(5, 8), (4, 14), (5, 19), (9, 18), (23, 8)]),
             poly([(23, 8), (23, 20)], g=1.3)]],
        3: [[poly([(5, 8), (4, 13), (5, 18), (8, 19), (11, 17), (13, 13)], g=1.3),
             poly([(13, 13), (14, 17), (17, 19), (20, 18), (23, 13), (22, 8)])],
            [poly([(4, 8), (4, 18), (9, 14), (10, 13)], g=1.3),
             poly([(10, 13), (13, 18), (18, 19), (22, 16), (23, 11), (21, 7)])]],
        4: [[poly([(4, 10), (14, 7), (15, 14), (15, 20)]), poly([(5, 17), (23, 17)])],
            [poly([(4, 9), (15, 8), (15, 20)]), poly([(4, 18), (23, 17)])],
            [poly([(4, 16), (14, 7), (15, 20)]), poly([(4, 16), (23, 16)])]],
        5: [[poly([(4, 19), (4, 10), (12, 9)], g=1.5),
             poly([(12, 9), (11, 14), (13, 18), (17, 19), (21, 17), (23, 12), (22, 8)])],
            [poly([(4, 18), (4, 9), (12, 8)], g=1.5),
             poly([(12, 8), (11, 13), (13, 17), (17, 19), (21, 18), (23, 13), (23, 9), (20, 6)])]],
        6: [[poly([(4, 17), (8, 12), (13, 9), (18, 9), (22, 11), (23, 15), (21, 18),
                   (17, 19), (14, 16), (14, 12), (16, 9)])],
            [poly([(4, 15), (9, 11), (15, 9), (20, 9), (23, 13), (22, 17), (19, 18),
                   (17, 15), (17, 11), (19, 9)])]],
        7: [[poly([(5, 8), (5, 19)], g=1.6), poly([(5, 19), (12, 16), (23, 13)])],
            [poly([(5, 7), (4, 19)], g=1.6), poly([(4, 19), (9, 18), (16, 15), (23, 14)])],
            [poly([(5, 8), (5, 19)], g=1.6), poly([(5, 19), (12, 16), (23, 13)]),
             poly([(14, 12), (14, 19)])]],
        8: [[ellipse(9, 14, 4.5, 4.5, gleft=1.4), ellipse(18.5, 14, 5, 5.5, gleft=1.4)],
            [poly([(6, 18), (4, 14)]), poly([(4, 14), (6, 10), (9, 11)], g=1.4),
             poly([(9, 11), (13, 14), (16, 18), (20, 19), (23, 14)]),
             poly([(23, 14), (21, 9), (17, 10)], g=1.4),
             poly([(17, 10), (13, 14), (9, 17), (6, 18)])]],
        9: [[ellipse(9, 14, 4.5, 5, gleft=1.3), poly([(9, 19), (23, 18)])],
            [ellipse(9, 14, 4, 4.5, gleft=1.3), poly([(9, 18.5), (16, 18), (23, 15)])],
            [ellipse(9, 13, 4.5, 5, gleft=1.3), poly([(9, 18), (23, 17)])]],
    }
    shear_sets = {k: [0.0, 0.2, 0.4] for k in range(10)}
    shear_sets[1] = [0.0, 0.2, 0.4, 0.6]
    shear_sets[7] = [-0.1, 0.1, 0.3]

    # ================= transforms =================
    def shear_var(var, sh):
        return [([(r, c + sh * (14 - r), dr, dc - sh * dr, w, g) for (r, c, dr, dc, w, g) in pts], cl)
                for (pts, cl) in var]

    CEN = 13.7

    def centre_var(var):
        allp = [p for (pts, _) in var for p in pts]
        W = sum(p[4] for p in allp)
        mr = sum(p[0] * p[4] for p in allp) / W
        mc = sum(p[1] * p[4] for p in allp) / W
        return [([(r - mr + CEN, c - mc + CEN, dr, dc, w, g) for (r, c, dr, dc, w, g) in pts], cl)
                for (pts, cl) in var]

    def endpoints(var):
        out = []
        for i, (pts, cl) in enumerate(var):
            if cl:
                continue
            for (p, sgn) in [(pts[0], -1.0), (pts[-1], 1.0)]:
                r, c, dr, dc = p[0], p[1], p[2], p[3]
                joined = False
                for j, (pts2, _) in enumerate(var):
                    if j == i:
                        continue
                    for p2 in pts2:
                        if (p2[0] - r) ** 2 + (p2[1] - c) ** 2 < 1.0:
                            joined = True
                            break
                    if joined:
                        break
                if not joined:
                    nn = math.hypot(dr, dc) + 1e-9
                    out.append((r, c, sgn * dr / nn, sgn * dc / nn))
        return out

    # ================= feature-space templates =================
    sigma = 1.5
    sigma_e = 2.0
    lam_e = 1.0

    def win_d(r, Y):
        return max(0.0, 2 * Y + 4 - r, r - (2 * Y + 7))

    def var_template(var):
        Tk = np.zeros((8, 8, 8))
        for (pts, _) in var:
            for (r, c, dr, dc, _, g) in pts:
                nrm = math.hypot(dr, dc) + 1e-9
                for f, (fr, fc) in enumerate(dirs):
                    cosd = abs(dr * fr + dc * fc) / nrm
                    tune = max(0.0, 2 * cosd * cosd - 1)
                    if tune <= 0:
                        continue
                    for Y in range(8):
                        dy = win_d(r, Y)
                        for X in range(8):
                            dx = win_d(c, X)
                            v = g * tune * math.exp(-(dy * dy + dx * dx) / (2 * sigma * sigma))
                            if v > Tk[f, Y, X]:
                                Tk[f, Y, X] = v
        for (r, c, tr, tc) in endpoints(var):
            for e, (pr, pc) in enumerate(tips):
                tune = max(0.0, tr * pr + tc * pc) ** 2
                if tune < 0.05:
                    continue
                for Y in range(8):
                    dy = win_d(r, Y)
                    for X in range(8):
                        dx = win_d(c, X)
                        v = lam_e * tune * math.exp(-(dy * dy + dx * dx) / (2 * sigma_e * sigma_e))
                        if v > Tk[4 + e, Y, X]:
                            Tk[4 + e, Y, X] = v
        return Tk

    T = np.zeros((10, 8, 8, 8))
    for k, vlist in variants.items():
        n = 0
        for var in vlist:
            for sh in shear_sets[k]:
                T[k] += var_template(centre_var(shear_var(var, sh)))
                n += 1
        T[k] /= n

    # ================= fc =================
    mask = np.zeros((8, 8))
    for Y in range(8):
        for X in range(8):
            if Y % 2 == X % 2:
                mask[Y, X] = 1.0
    Tm = T * mask
    p = 0.5
    norms = np.sqrt((Tm ** 2).sum(axis=(1, 2, 3), keepdims=True))
    Tn = Tm / norms ** p
    means = Tn.sum(axis=(2, 3), keepdims=True) / mask.sum()
    Wt = (Tn - means) * mask
    Wt = Wt / np.sqrt((Wt ** 2).sum(axis=(1, 2, 3))).mean()
    s = 4.5

    Wfc = np.zeros((10, 256), np.float32)
    for k in range(10):
        for m in range(8):
            for q in range(2):
                c = 2 * m + q
                for sr in range(4):
                    for sc in range(4):
                        Wfc[k, c * 16 + sr * 4 + sc] = s * Wt[k, m, 2 * sr + q, 2 * sc + q]

    # biases rebalanced for the new features (from step-17 prediction counts)
    bfc = np.array([0.0, -0.5, 0.9, -0.6, 1.0, 0.3, -0.8, -0.1, 1.0, -0.2], np.float32)

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wfc, "fc.bias": bfc,
    }
```
