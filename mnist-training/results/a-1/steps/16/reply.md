## Step 16: narrower position tolerance in the templates

**Step 15 result.** 72.4% accuracy, loss 0.89. The largest remaining errors are about where strokes sit, not what orientation they have:
- 3 ↔ 5: top-left vertical versus top-right arc.
- 5 → 8 and 8 → 3: whether the left side has strokes.
- 9 → 3.

**Reasoning.** Each feature is already a max over a 6-px window, with windows 2 px apart. My templates then add a further Gaussian position spread of σ = 1.5 px on top. Together these may blur left against right too much to separate these pairs.

**Change.** I reduce the template spread to σ = 1.0. Everything else stays as in step 15, so I can see the effect of this single change.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]       # 0=horizontal, 45='/', 90=vertical, 135='\'
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

    # ---------------- conv2: tap selection -> 8x8 grid per orientation ----------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for f in range(4):
        for ai in range(2):
            for bi in range(2):
                W2[f * 4 + ai * 2 + bi, f, 1 + ai, 1 + bi] = 1.0

    # ---------------- stroke helpers: points (r, c, dr, dc, arc_weight, gain) ----------------
    def poly(pts, g=1.0, step=0.5):
        out = []
        for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
            L = math.hypot(r1 - r0, c1 - c0)
            n = max(1, int(L / step))
            for i in range(n + 1):
                a = i / n
                out.append((r0 + a * (r1 - r0), c0 + a * (c1 - c0), r1 - r0, c1 - c0, L / (n + 1), g))
        return out

    def ellipse(cr, cc, rr, rc, t0=0.0, t1=2 * math.pi, n=80, g=1.0, gleft=None):
        # t measured from top, clockwise; left half is sin(t) < 0
        out = []
        dt = (t1 - t0) / n
        for i in range(n):
            t = t0 + dt * i
            dr, dc = rr * math.sin(t), rc * math.cos(t)
            gg = g
            if gleft is not None and math.sin(t) < 0:
                gg = gleft
            out.append((cr - rr * math.cos(t), cc + rc * math.sin(t), dr, dc,
                        math.hypot(dr, dc) * dt, gg))
        return out

    # ---------------- hand-drawn upright variants (gain >1 = discriminative stroke) ----------------
    variants = {
        0: [ellipse(14, 14, 9, 6.5), ellipse(14, 14, 9, 5), ellipse(14, 14, 8.5, 7.5)],
        1: [poly([(4, 14), (23, 14)]),
            poly([(7, 11), (4, 14), (23, 14)])],
        2: [poly([(8, 8), (5, 11), (4, 14), (5, 18), (8, 19), (11, 18), (15, 14),
                  (19, 10), (23, 8)]) + poly([(23, 8), (23, 14), (23, 20)], g=1.3),
            poly([(7, 7), (4, 11), (4, 16), (7, 19), (11, 18), (16, 13), (21, 8),
                  (23, 7)]) + poly([(23, 7), (23, 13), (22, 20)], g=1.3),
            poly([(5, 8), (4, 14), (5, 19), (9, 18), (23, 8)]) + poly([(23, 8), (23, 20)], g=1.3)],
        3: [poly([(5, 8), (4, 13), (5, 18), (8, 19), (11, 17), (13, 13)], g=1.3) +
            poly([(13, 13), (14, 17), (17, 19), (20, 18), (23, 13), (22, 8)]),
            poly([(4, 8), (4, 18), (9, 14), (10, 13)], g=1.3) +
            poly([(10, 13), (13, 18), (18, 19), (22, 16), (23, 11), (21, 7)])],
        4: [poly([(4, 10), (14, 7), (15, 14), (15, 20)]) + poly([(5, 17), (23, 17)]),
            poly([(4, 9), (15, 8), (15, 20)]) + poly([(4, 18), (23, 17)]),
            poly([(4, 16), (14, 7), (15, 20)]) + poly([(4, 16), (23, 16)])],
        5: [poly([(4, 19), (4, 10), (12, 9)], g=1.5) +
            poly([(12, 9), (11, 14), (13, 18), (17, 19), (21, 17), (23, 12), (22, 8)]),
            poly([(4, 18), (4, 9), (12, 8)], g=1.5) +
            poly([(12, 8), (11, 13), (13, 17), (17, 19), (21, 18), (23, 13), (23, 9), (20, 6)])],
        6: [poly([(4, 17), (8, 12), (13, 9), (18, 9), (22, 11), (23, 15), (21, 18),
                  (17, 19), (14, 16), (14, 12), (16, 9)]),
            poly([(4, 15), (9, 11), (15, 9), (20, 9), (23, 13), (22, 17), (19, 18),
                  (17, 15), (17, 11), (19, 9)])],
        7: [poly([(5, 8), (5, 19)], g=1.6) + poly([(5, 19), (12, 16), (23, 13)]),
            poly([(5, 7), (4, 19)], g=1.6) + poly([(4, 19), (9, 18), (16, 15), (23, 14)]),
            poly([(5, 8), (5, 19)], g=1.6) + poly([(5, 19), (12, 16), (23, 13)]) +
            poly([(14, 12), (14, 19)])],
        8: [ellipse(9, 14, 4.5, 4.5, gleft=1.4) + ellipse(18.5, 14, 5, 5.5, gleft=1.4),
            poly([(6, 18), (4, 14)]) + poly([(4, 14), (6, 10), (9, 11)], g=1.4) +
            poly([(9, 11), (13, 14), (16, 18), (20, 19), (23, 14)]) +
            poly([(23, 14), (21, 9), (17, 10)], g=1.4) +
            poly([(17, 10), (13, 14), (9, 17), (6, 18)])],
        9: [ellipse(9, 14, 4.5, 5, gleft=1.3) + poly([(9, 19), (23, 18)]),
            ellipse(9, 14, 4, 4.5, gleft=1.3) + poly([(9, 18.5), (16, 18), (23, 15)]),
            ellipse(9, 13, 4.5, 5, gleft=1.3) + poly([(9, 18), (23, 17)])],
    }
    shear_sets = {k: [0.0, 0.2, 0.4] for k in range(10)}
    shear_sets[1] = [0.0, 0.2, 0.4, 0.6]
    shear_sets[7] = [-0.1, 0.1, 0.3]

    # ---------------- geometric transforms ----------------
    def shear(pts, sh):
        return [(r, c + sh * (14 - r), dr, dc - sh * dr, w, g) for (r, c, dr, dc, w, g) in pts]

    CEN = 13.7   # MNIST: centre of mass at the middle of the field

    def centre(pts):
        W = sum(p[4] for p in pts)
        mr = sum(p[0] * p[4] for p in pts) / W
        mc = sum(p[1] * p[4] for p in pts) / W
        return [(r - mr + CEN, c - mc + CEN, dr, dc, w, g) for (r, c, dr, dc, w, g) in pts]

    # ---------------- template in feature space for one stroke set ----------------
    sigma = 1.0   # narrower positional tolerance (was 1.5)

    def feat_template(pts):
        Tk = np.zeros((4, 8, 8))
        for (r, c, dr, dc, _, g) in pts:
            nrm = math.hypot(dr, dc) + 1e-9
            for f, (fr, fc) in enumerate(dirs):
                cosd = abs(dr * fr + dc * fc) / nrm
                tune = max(0.0, 2 * cosd * cosd - 1)
                if tune <= 0:
                    continue
                for Y in range(8):
                    dy = max(0.0, 2 * Y + 4 - r, r - (2 * Y + 7))
                    for X in range(8):
                        dx = max(0.0, 2 * X + 4 - c, c - (2 * X + 7))
                        v = g * tune * math.exp(-(dy * dy + dx * dx) / (2 * sigma * sigma))
                        if v > Tk[f, Y, X]:
                            Tk[f, Y, X] = v
        return Tk

    T = np.zeros((10, 4, 8, 8))
    for k, vlist in variants.items():
        n = 0
        for pts in vlist:
            for sh in shear_sets[k]:
                T[k] += feat_template(centre(shear(pts, sh)))
                n += 1
        T[k] /= n

    # ---------------- fc: partially normalised templates, zero-sum per (class, orientation) ----------------
    p = 0.5
    norms = np.sqrt((T ** 2).sum(axis=(1, 2, 3), keepdims=True))
    Tn = T / norms ** p
    Wt = Tn - Tn.mean(axis=(2, 3), keepdims=True)
    Wt = Wt / np.sqrt((Wt ** 2).sum(axis=(1, 2, 3))).mean()
    s = 4.5
    Wfc = np.zeros((10, 256), np.float32)
    for k in range(10):
        for f in range(4):
            for ai in range(2):
                for bi in range(2):
                    c = f * 4 + ai * 2 + bi
                    for sr in range(4):
                        for sc in range(4):
                            Wfc[k, c * 16 + sr * 4 + sc] = s * Wt[k, f, 2 * sr + ai, 2 * sc + bi]

    bfc = np.array([0.0, -0.4, 1.0, -1.0, 1.4, 0.3, -0.8, 0.2, 1.2, -0.7], np.float32)

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wfc, "fc.bias": bfc,
    }
```
