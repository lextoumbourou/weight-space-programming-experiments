This is the final step, so I'm resubmitting the best network seen so far, from step 11 (54.8% validation accuracy), rather than risking another untested change. The later edits (an open-top 4, the extra bias corrections and a straighter 1) all scored lower. The network is exactly the step-11 version:
- stroke and ink features in conv1;
- local 3x3-window features plus an "empty window" feature in conv2;
- fc weights from hand-drawn stroke templates;
- matched-filter energy biases with the step-11 class corrections.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: oriented strokes + ink blob ----------------
    w1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    rr, cc = np.meshgrid(np.arange(-2, 3), np.arange(-2, 3), indexing="ij")

    def bar(dr, dc):
        # oriented line detector: zero-sum gaussian ridge through the centre
        n = math.hypot(dr, dc)
        dr, dc = dr / n, dc / n
        perp = rr * dc - cc * dr
        g = np.exp(-perp ** 2 / (2 * 0.9 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    w1[0, 0] = bar(1, 0)    # 0: vertical
    w1[1, 0] = bar(0, 1)    # 1: horizontal
    w1[2, 0] = bar(-1, 1)   # 2: "/"
    w1[3, 0] = bar(1, 1)    # 3: "\"
    g = np.exp(-(rr ** 2 + cc ** 2) / (2 * 1.3 ** 2))
    w1[4, 0] = g / g.sum()  # 4: ink blob (channels 5..7 unused)

    # ---------------- conv2: local (3x3 window) pooled features ----------------
    w2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros(16, dtype=np.float32)
    m = np.zeros((5, 5), dtype=np.float32)
    m[1:4, 1:4] = 1.0
    m = 2.0 * m / m.sum()
    for k in range(5):      # channels 0..4 = V, H, "/", "\", ink in a central window
        w2[k, k] = m
    b2[0:4] = -0.05
    # channel 5: "empty window" = relu(0.4 - local ink)
    w2[5, 4] = -m
    b2[5] = 0.4

    # ---------------- stroke templates (x = column, y = row, pixel coords) ----------------
    def ellipse(cx, cy, rx, ry, a0=0.0, a1=2 * math.pi, n=40):
        return [(cx + rx * math.cos(a0 + (a1 - a0) * t / n),
                 cy + ry * math.sin(a0 + (a1 - a0) * t / n)) for t in range(n + 1)]

    T = {}
    T[0] = [ellipse(14, 14, 6.5, 9.5)]
    T[1] = [[(15.5, 4), (13, 24)], [(11.5, 7.5), (15.5, 4)]]
    T[2] = [[(8.5, 8), (10, 5), (14, 4), (18, 5.5), (19.5, 9), (17, 13),
             (8.5, 23), (20.5, 23)]]
    T[3] = [[(8.5, 6), (12, 4), (16, 4.5), (18.5, 8), (16, 12), (12.5, 13.5),
             (16.5, 15), (19, 18.5), (17, 22.5), (13, 24), (8.5, 22)]]
    T[4] = [[(16, 4), (7, 17), (21, 17)], [(16, 4), (16, 24)]]
    T[5] = [[(19, 4), (9.5, 4), (9, 13), (13, 12), (17, 13.5), (19.5, 17),
             (18, 21.5), (14, 24), (8.5, 22)]]
    T[6] = [[(17.5, 4), (12, 8), (9, 14), (8.5, 18.5)], ellipse(14, 18.5, 5.5, 5.5)]
    T[7] = [[(8, 4.5), (20.5, 4.5), (11.5, 24)]]
    T[8] = [ellipse(14, 9, 4.5, 5.0), ellipse(14, 19, 5.5, 5.5)]
    T[9] = [ellipse(14, 9.5, 5.0, 5.5), [(19, 10), (18.5, 16), (15, 24)]]

    s2 = math.sqrt(0.5)
    orient = [(0.0, 1.0), (1.0, 0.0), (s2, -s2), (s2, s2)]   # V, H, "/", "\"

    centers = [7.5 + 4 * k for k in range(4)]   # cell centres in pixels
    sigma = 3.5
    norm = math.sqrt(2 * math.pi) * sigma

    # fc template weights: each stroke sample votes (gaussian in space, cos^2 in angle)
    W = np.zeros((10, 16, 4, 4), dtype=np.float64)
    for cls in range(10):
        for poly in T[cls]:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(math.ceil(L / 0.5)))
                dx, dy = (x1 - x0) / L, (y1 - y0) / L
                step = L / n
                cos2 = [(dx * ux + dy * uy) ** 2 for ux, uy in orient]
                for t in range(n):
                    px = x0 + (t + 0.5) * step * dx
                    py = y0 + (t + 0.5) * step * dy
                    for i in range(4):
                        for j in range(4):
                            d2 = (px - centers[j]) ** 2 + (py - centers[i]) ** 2
                            wgt = math.exp(-d2 / (2 * sigma ** 2)) * step / norm
                            for o in range(4):
                                W[cls, o, i, j] += wgt * cos2[o]
                            W[cls, 4, i, j] += wgt

    # matched-filter energy bias
    alpha = 0.9
    gamma = 0.5
    Wf = W.reshape(10, 256).copy()
    energy = (Wf ** 2).sum(axis=1)
    bf = (-0.5 * alpha * energy) * gamma
    Wf = Wf * gamma

    # emptiness weights: reward "empty window" where the class template has little ink
    eps = 1.0
    E = np.clip(1.0 - W[:, 4, :, :] / 0.5, 0.0, 1.0)
    Wf3 = Wf.reshape(10, 16, 4, 4)
    Wf3[:, 5, :, :] = eps * E
    Wf = Wf3.reshape(10, 256)

    # per-class bias corrections (from earlier confusion matrices; step-11 values)
    corr = np.array([-0.14, -0.10, -0.30, -0.07, 0.80, -0.31, 0.31, 0.18, 0.55, 0.46])
    corr = corr + np.array([-0.05, 0.0, 0.10, -0.05, 0.0, 0.0, 0.15, -0.15, 0.20, 0.0])
    bf = bf + corr

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2,
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
