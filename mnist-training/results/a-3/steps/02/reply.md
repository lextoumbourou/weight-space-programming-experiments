## Step 2: score each digit as a likelihood instead of a cosine match

**What went wrong in step 1:** I normalised every template to unit length. That gave sparse templates, especially digit 1, very large weights. Any image with a vertical stroke near the middle scored high for "1". Many 8s, 4s and 9s were therefore predicted as 1.

**What changes in this step:**
- **Likelihood scoring.** The fc layer now treats each pooled feature as roughly a present/absent signal, like a Bernoulli naive-Bayes classifier. For digit d, each feature has a probability p = 0.05 + 0.9·T of being present, where T is the stroke template from before.
  - The weight on each feature is γ·log(p/(1−p))/s.
  - The class bias is γ·Σ log(1−p).
  - s is the typical value of a "present" feature: about 2 for orientation channels and 3 for ink.
  - The bias makes classes that expect many features pay a cost when those features are missing. This replaces the bad norm effect.
  - γ is a temperature that tempers overconfidence, because the features are far from independent.
- **Alternative strokes.** I add a few weighted alternative strokes: a slanted 1, a closed-top 4, and more 7 and 9 variants.

conv1 and conv2 are unchanged.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    thetas = [0.0, 45.0, 90.0, 135.0]   # 0=horizontal, 45="\", 90=vertical, 135="/" (y down)
    for k, th in enumerate(thetas):
        t = math.radians(th)
        ux, uy = math.cos(t), math.sin(t)
        nx, ny = -math.sin(t), math.cos(t)
        raw = np.zeros((5, 5)); taper = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                d = dx * nx + dy * ny
                a = dx * ux + dy * uy
                raw[r, c] = math.exp(-d * d / (2 * 0.9 ** 2))
                taper[r, c] = math.exp(-a * a / (2 * 2.0 ** 2))
        m = (taper * raw).sum() / taper.sum()
        w = taper * (raw - m)                  # zero-sum ridge detector
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.1
    W1[4, 0, 1:4, 1:4] = 1.0 / 9.0             # ink detector
    # channels 5-7 unused

    # ---------------- conv2: pass-through with small blur ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(5):
        W2[j, j, 1:4, 1:4] = K

    # ---------------- fc: stroke templates -> naive-Bayes style scores ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    # each digit: list of (weight, polyline) in 20x20 box coords (u=col, v=row)
    digits = {
        0: [(1.0, ellipse(10, 10, 6.5, 9.5))],
        1: [(1.0, [(11, 0.5), (9, 19.5)]),
            (0.6, [(14, 0.5), (6, 19.5)])],                     # slanted 1
        2: [(1.0, [(4, 5), (6, 1.5), (10, 0.5), (14, 1.5), (16, 5), (15, 9), (10, 14), (4, 19.5),
                   (10, 19.5), (17, 19.5)])],
        3: [(1.0, [(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
                   (15, 18), (11, 19.8), (4, 18.5)])],
        4: [(0.8, [(7, 0.5), (5, 7), (4, 12.5), (10, 12.5), (17, 12)]),   # open-top 4
            (0.6, [(12, 0.5), (8, 6), (4, 12.5)]),                       # closed-top diagonal
            (1.0, [(14, 2), (14, 8), (13.5, 19.5)])],
        5: [(1.0, [(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
                   (11, 19.8), (4, 18.5)])],
        6: [(1.0, [(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
                   (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)])],
        7: [(1.0, [(4, 1), (10, 0.5), (16, 0.5), (14, 6), (12, 11), (10, 19.5)]),
            (0.5, [(16, 0.5), (11, 10), (8, 19.5)])],             # more slanted stem
        8: [(1.0, ellipse(10, 5, 5, 4.7)), (1.0, ellipse(10, 14.7, 6, 5))],
        9: [(1.0, ellipse(10, 5.5, 5.5, 5)), (1.0, [(15.5, 5.5), (15, 11), (14, 19.5)]),
            (0.5, [(15.5, 5.5), (13, 12), (10, 19.5)])],          # slanted stem
    }

    centers = [4 * r + 7.5 for r in range(4)]
    sig = 2.5
    NF = 5
    T = np.zeros((10, NF, 4, 4))
    for d, strokes in digits.items():
        acc = np.zeros((NF, 4, 4))
        for wgt, poly in strokes:
            for (u0, v0), (u1, v1) in zip(poly[:-1], poly[1:]):
                x0, y0, x1, y1 = u0 + 4, v0 + 4, u1 + 4, v1 + 4
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.5))
                ds = L / n
                phi = math.atan2(y1 - y0, x1 - x0)
                orient = [max(0.0, math.cos(2 * (phi - math.radians(th)))) ** 2 for th in thetas]
                for i in range(n):
                    s = (i + 0.5) / n
                    x = x0 + s * (x1 - x0); y = y0 + s * (y1 - y0)
                    mr = np.array([math.exp(-(y - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                    mc = np.array([math.exp(-(x - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                    m = np.outer(mr, mc) * ds * wgt
                    for k in range(4):
                        acc[k] += orient[k] * m
                    acc[4] += 0.5 * m
        T[d] = 1.0 - np.exp(-acc / 1.5)

    # Bernoulli naive-Bayes style: p = prob. feature present for class d
    gamma = 0.3                                   # temperature (features are correlated)
    scale = np.array([2.0, 2.0, 2.0, 2.0, 3.0])   # typical value of a "present" feature
    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    for d in range(10):
        p = 0.05 + 0.9 * T[d]
        L1 = np.log(p / (1 - p))
        L0 = np.log(1 - p)
        for k in range(NF):
            Wfc[d, k * 16:(k + 1) * 16] = gamma * L1[k].reshape(-1) / scale[k]
        bfc[d] = gamma * L0.sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
