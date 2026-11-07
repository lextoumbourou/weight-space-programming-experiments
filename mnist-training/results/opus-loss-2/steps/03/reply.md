## Step 3: zero-sum class weights, a better 0, and extra weight on confused pairs

Step 2 improved the loss to 1.006 and accuracy to 67.2%. The largest confusions are 4→9 (393), 2→8 (292), 5→6 (262), 0→2 (182), 1→7 (155) and 3→8 (151).

1. **Zero-sum class weights.**
   - All features are non-negative, so a thick or heavy image raises every logit in proportion to how much positive weight that class has.
   - Classes with spread-out templates (8, 6, 9) gain from this, and they are over-predicted.
   - I now make each class's weight vector sum to zero over all 256 features. Generic extra ink then no longer favours any class.

2. **Better 0 template.**
   - The 0 is now wider (x-radius 7 instead of 6) and its centre is empty.
   - I add a tilted variant whose top leans right.

3. **Extra weight on confused pairs.**
   - For each heavily confused pair (a, b), I add λ·(T_a − T_b) to class a's weights and the negative to class b's, where T is the normalised template.
   - This pushes the decision towards the features that actually separate the two drawings.
   - The pairs are 4/9, 5/6, 2/8, 0/2, 1/7, 3/8, 7/9, 8/9, 3/5 and 4/8.

conv1 and conv2 are unchanged.

```python
import numpy as np
import math

def build_weights():
    PI = math.pi
    # ---------------- conv1: oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    # line directions (x right, y down): 0=horizontal, pi/4="\", pi/2=vertical, 3pi/4="/"
    phis = [0.0, PI / 4, PI / 2, 3 * PI / 4]
    for k, phi in enumerate(phis):
        vals = {}
        for r in range(5):
            for c in range(5):
                x, y = c - 2, r - 2
                if x * x + y * y <= 5:
                    d = abs(-math.sin(phi) * x + math.cos(phi) * y)
                    vals[(r, c)] = math.exp(-d * d / 2.0)
        m = np.mean(list(vals.values()))
        for (r, c), v in vals.items():
            W1[k, 0, r, c] = v - m             # zero-sum: flat ink gives nothing
        W1[k] /= W1[k][W1[k] > 0].sum()        # ideal stroke -> ~1
        b1[k] = -0.15
    # channels 4-7 unused

    # ---------------- conv2: 4 orientations x 4 spatial shifts ----------------
    # channel = k*4 + sy*2 + sx ; 2x2 block sum of pooled orientation map k.
    # Final cell (i,j) centred at input y = 6.5+2*sy+4*i, x = 6.5+2*sx+4*j
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for k in range(4):
        for sy in range(2):
            for sx in range(2):
                ch = k * 4 + sy * 2 + sx
                W2[ch, k, 1 + sy:3 + sy, 1 + sx:3 + sx] = 0.5

    # ---------------- digit stroke drawings (x=col, y=row, pixels) ----------------
    def seg(p0, p1):
        p0 = np.array(p0, float); p1 = np.array(p1, float)
        L = np.linalg.norm(p1 - p0)
        n = max(2, int(L / 0.25) + 1)
        t = np.linspace(0, 1, n)[:, None]
        return p0 + (p1 - p0) * t

    def arc(cx, cy, rx, ry, t0, t1, rot=0.0):
        # ellipse arc; rot>0 tilts the top of the shape to the right
        n = int(abs(t1 - t0) * max(rx, ry) / 0.25) + 2
        t = np.linspace(t0, t1, n)
        x0 = rx * np.cos(t); y0 = ry * np.sin(t)
        x = cx + x0 * math.cos(rot) - y0 * math.sin(rot)
        y = cy + x0 * math.sin(rot) + y0 * math.cos(rot)
        return np.stack([x, y], axis=1)

    digits = {
        0: [[arc(14, 14, 7, 9.5, 0, 2 * PI)],
            [arc(14, 14, 6.5, 9.5, 0, 2 * PI, rot=0.3)]],
        1: [[seg((14, 4.5), (14, 23.5))],
            [seg((16.5, 4.5), (11.5, 23.5))]],
        2: [[arc(14, 10, 5.5, 5, -PI, 0.5),
             seg((18.8, 12.4), (8, 23)),
             seg((8, 23), (21, 22.5))]],
        3: [[arc(13.5, 8.8, 5, 4.3, -2.6, PI / 2),
             seg((10.5, 13.2), (13.5, 13.1)),
             arc(13.5, 18.5, 6, 5.4, -PI / 2, 2.6)]],
        4: [[seg((15, 4.5), (7.5, 17)),          # closed/slanted 4
             seg((7.5, 17), (21, 17)),
             seg((17.5, 9), (17, 23.5))],
            [seg((9, 4.5), (8, 16.5)),           # open-top 4
             seg((8, 16.5), (21, 16.5)),
             seg((17.5, 4.5), (17, 23.5))]],
        5: [[seg((20, 4.5), (10.5, 4.5)),
             seg((10.5, 4.5), (9.5, 12.5)),
             arc(13.5, 17.2, 6, 5.8, -2.2, 2.6)]],
        6: [[arc(19, 16, 9.5, 11.5, -1.75, -PI),
             arc(14, 18.3, 5, 5, 0, 2 * PI)]],
        7: [[seg((8, 5), (20.5, 5)),
             seg((20.5, 5), (12.5, 23.5))]],
        8: [[arc(14, 9, 4.5, 4.5, 0, 2 * PI),
             arc(14, 18.5, 5.5, 5, 0, 2 * PI)]],
        9: [[arc(13.5, 9.5, 5, 5, 0, 2 * PI),
             seg((18.5, 10), (18, 23.5))],
            [arc(14, 9.5, 5, 5, 0, 2 * PI),
             seg((19, 10), (15, 23.5))]],
    }

    sig = 2.5
    def centres(s):
        return 6.5 + 2.0 * s + 4.0 * np.arange(4)

    def presence(strokes):
        # T[k, sy, sx, i, j]: amount of orientation-k stroke near that cell
        T = np.zeros((4, 2, 2, 4, 4))
        for pts in strokes:
            d = pts[1:] - pts[:-1]
            mid = 0.5 * (pts[1:] + pts[:-1])
            ds = np.linalg.norm(d, axis=1)
            ang = np.arctan2(d[:, 1], d[:, 0])
            for sy in range(2):
                gy = np.exp(-(mid[:, 1][:, None] - centres(sy)[None, :]) ** 2 / (2 * sig ** 2))
                for sx in range(2):
                    gx = np.exp(-(mid[:, 0][:, None] - centres(sx)[None, :]) ** 2 / (2 * sig ** 2))
                    g = gy[:, :, None] * gx[:, None, :]
                    for k, phi in enumerate(phis):
                        ow = np.maximum(0.0, np.cos(2 * (ang - phi))) ** 2
                        T[k, sy, sx] += np.tensordot(ds * ow, g, axes=(0, 0))
        return 1.0 - np.exp(-T / 2.5)

    # normalised templates (10, 256) in fc flatten order
    # flatten: channel = k*4+sy*2+sx, then (i,j) -> index ch*16 + i*4 + j
    Tn = np.zeros((10, 256))
    for dgt in range(10):
        P = np.mean([presence(v) for v in digits[dgt]], axis=0)  # (4,2,2,4,4)
        P = P.reshape(16, 16)          # (k,sy,sx) -> channel ; (i,j) -> 16
        v = P.reshape(256)
        Tn[dgt] = v / np.linalg.norm(v)

    # base weights: template minus class-mean template
    W = Tn - Tn.mean(axis=0, keepdims=True)

    # pairwise emphasis for confused pairs (from step-2 confusion matrix)
    pairs = [(4, 9, 0.6), (5, 6, 0.6), (2, 8, 0.5), (0, 2, 0.5), (1, 7, 0.4),
             (3, 8, 0.4), (7, 9, 0.3), (8, 9, 0.3), (3, 5, 0.3), (4, 8, 0.3)]
    for a, b, lam in pairs:
        diff = Tn[a] - Tn[b]
        W[a] += lam * diff
        W[b] -= lam * diff

    # zero-sum per class: generic extra ink favours no class
    W -= W.mean(axis=1, keepdims=True)

    scale = 4.0
    Wf = scale * W
    bf = np.zeros(10, dtype=np.float64)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
