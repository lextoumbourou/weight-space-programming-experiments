## Step 4: discriminative templates

**Where things stand.** Step 3's distance scoring was worse; step 2's cosine scoring is still the best.
- Since only one template per class feeds a linear layer, every variant reduces to a per-class scale and bias, so cosine (normalising by |T_k|) is the right starting point.
- The remaining problem is that "8" absorbs 4s, 2s, 9s and 0s. Its template overlaps every other template.
- "7" and "4" are almost never predicted.

**Changes.**
- **Discriminative directions.** I subtract the mean template M across classes before normalising, so each class weight is W_k = s·(T_k − M)/|T_k − M|. This keeps only what is distinctive about each digit. Shared ink, which every digit has around the centre, no longer pushes towards the broadest template.
- **Sharper templates.** I reduce the position tolerance from σ = 1.5 to 1.2, so the templates overlap less.
- **Scale.** I keep s = 4.

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

    # ---------------- hand-drawn digit strokes ----------------
    def poly(pts, step=0.5):
        out = []
        for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
            L = math.hypot(r1 - r0, c1 - c0)
            n = max(1, int(L / step))
            for i in range(n + 1):
                a = i / n
                out.append((r0 + a * (r1 - r0), c0 + a * (c1 - c0), r1 - r0, c1 - c0))
        return out

    def ellipse(cr, cc, rr, rc, t0=0.0, t1=2 * math.pi, n=80):
        out = []
        for i in range(n):
            t = t0 + (t1 - t0) * i / n
            out.append((cr - rr * math.cos(t), cc + rc * math.sin(t),
                        rr * math.sin(t), rc * math.cos(t)))
        return out

    digits = {
        0: ellipse(14, 14, 9, 6.5),
        1: poly([(4, 16), (23, 12)]),
        2: poly([(8, 8), (5, 11), (4, 14), (5, 18), (8, 19), (11, 18), (15, 14),
                 (19, 10), (23, 8), (23, 14), (23, 20)]),
        3: poly([(5, 8), (4, 13), (5, 18), (8, 19), (11, 17), (13, 13)]) +
           poly([(13, 13), (14, 17), (17, 19), (20, 18), (23, 13), (22, 8)]),
        4: poly([(4, 10), (14, 7), (15, 14), (15, 20)]) + poly([(5, 17), (23, 17)]),
        5: poly([(4, 19), (4, 10), (12, 9), (11, 14), (13, 18), (17, 19), (21, 17),
                 (23, 12), (22, 8)]),
        6: poly([(4, 17), (8, 12), (13, 9), (18, 9), (22, 11), (23, 15), (21, 18),
                 (17, 19), (14, 16), (14, 12), (16, 9)]),
        7: poly([(5, 8), (5, 19), (10, 17), (15, 14), (23, 12)]),
        8: ellipse(9, 14, 4.5, 4.5) + ellipse(18.5, 14, 5, 5.5),
        9: ellipse(9, 14, 4.5, 5) + poly([(9, 19), (23, 16)]),
    }

    # ---------------- templates in feature space: T[k, f, Y, X] ----------------
    sigma = 1.2
    T = np.zeros((10, 4, 8, 8))
    for k, pts in digits.items():
        for (r, c, dr, dc) in pts:
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
                        v = tune * math.exp(-(dy * dy + dx * dx) / (2 * sigma * sigma))
                        if v > T[k, f, Y, X]:
                            T[k, f, Y, X] = v

    # ---------------- fc: centred + normalised template directions ----------------
    D = T - T.mean(axis=0, keepdims=True)                    # distinctive part of each class
    D = D / np.sqrt((D ** 2).sum(axis=(1, 2, 3), keepdims=True))
    s = 4.0
    Wfc = np.zeros((10, 256), np.float32)
    bfc = np.zeros(10, np.float32)
    for k in range(10):
        for f in range(4):
            for ai in range(2):
                for bi in range(2):
                    c = f * 4 + ai * 2 + bi
                    for sr in range(4):
                        for sc in range(4):
                            Wfc[k, c * 16 + sr * 4 + sc] = s * D[k, f, 2 * sr + ai, 2 * sc + bi]

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wfc, "fc.bias": bfc,
    }
```
