## Step 1: oriented-stroke features and hand-drawn digit templates

The network is set up as a nearest-template classifier over oriented-stroke features.

- **conv1:** Channels 0–3 are 5×5 line detectors at 0°, 45°, 90° and 135°. Each has a positive ridge along the line through the centre and a negative surround. A detector responds with about 1 to a 3-px-wide stroke at its own orientation. The bias is −0.3, which removes weak and cross-orientation responses. Channels 4–7 are unused for now.
- **conv2:** Each output channel copies one orientation map, using a single tap at kernel offset (a, b) with a, b ∈ {1, 2}. Combined with the two max-pools, this gives every orientation an 8×8 grid of max-pooled windows. Each window spans 6 px, and the window starts are 2 px apart. 4 orientations × 4 offsets = 16 channels.
- **fc:** I draw each digit by hand as polylines and ellipses in 28×28 coordinates.
  - From each drawing I build a template T_k over 4 orientations × 8×8 cells.
  - Each stroke point adds its orientation tuning, max(0, cos 2Δ), to nearby cells, with Gaussian position tolerance.
  - The logit is z_k = s·(⟨T_k, F⟩ − ½|T_k|²). This ranks classes by negative squared distance between the feature vector F and each template.

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
        dirs.append((-math.sin(t), math.cos(t)))   # unit direction in (row, col); row grows downward

    def profile(d):
        # ridge profile across the line: 1 at centre, 0.6 at d=1, -0.5 for d>=2
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
                d = abs(u * dc - v * dr)        # distance from the line through the kernel centre
                dist[u + 2, v + 2] = d
                w[u + 2, v + 2] = profile(d)
        # normalise: response to an ideal 3-px-wide stroke (the d<=1.5 band) = 1
        w = w / w[dist <= 1.5].sum()
        W1[f, 0] = w
        b1[f] = -0.3                            # threshold out weak / cross-orientation responses

    # ---------------- conv2: tap selection -> 8x8 grid per orientation ----------------
    # channel c = f*4 + ai*2 + bi, single weight at kernel (1+ai, 1+bi).
    # After pool2 at cell (sr, sc): grid Y = 2*sr+ai, X = 2*sc+bi.
    # Detector centres covered by grid cell Y: input rows 2Y+4 .. 2Y+7 (same for columns).
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for f in range(4):
        for ai in range(2):
            for bi in range(2):
                c = f * 4 + ai * 2 + bi
                W2[c, f, 1 + ai, 1 + bi] = 1.0

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
    sigma = 1.5   # positional tolerance in pixels
    T = np.zeros((10, 4, 8, 8))
    for k, pts in digits.items():
        for (r, c, dr, dc) in pts:
            nrm = math.hypot(dr, dc) + 1e-9
            for f, (fr, fc) in enumerate(dirs):
                cosd = abs(dr * fr + dc * fc) / nrm
                tune = max(0.0, 2 * cosd * cosd - 1)   # cos(2*delta)
                if tune <= 0:
                    continue
                for Y in range(8):
                    lo, hi = 2 * Y + 4, 2 * Y + 7
                    dy = max(0.0, lo - r, r - hi)
                    for X in range(8):
                        lo2, hi2 = 2 * X + 4, 2 * X + 7
                        dx = max(0.0, lo2 - c, c - hi2)
                        v = tune * math.exp(-(dy * dy + dx * dx) / (2 * sigma * sigma))
                        if v > T[k, f, Y, X]:
                            T[k, f, Y, X] = v

    # ---------------- fc: nearest-template logits ----------------
    s = 0.3
    Wfc = np.zeros((10, 256), np.float32)
    bfc = np.zeros(10, np.float32)
    for k in range(10):
        for f in range(4):
            for ai in range(2):
                for bi in range(2):
                    c = f * 4 + ai * 2 + bi
                    for sr in range(4):
                        for sc in range(4):
                            Y, X = 2 * sr + ai, 2 * sc + bi
                            Wfc[k, c * 16 + sr * 4 + sc] = s * T[k, f, Y, X]
        bfc[k] = -0.5 * s * float((T[k] ** 2).sum())

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wfc, "fc.bias": bfc,
    }
```
