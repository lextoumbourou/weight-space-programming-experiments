## Step 20: probe the small-hole and narrow-gap detectors

**Where things stand.** Measured topology templates gave the best result yet: loss 0.942 and accuracy 71.1%. The largest remaining errors are 7→9 (300), 3→5 (190), 2→8 (153), 9→8 (149) and 6→0 (132).

**Why these probes.**
- To separate 7 from 9, I most need to know whether the small, strict hole detector LOOP_s fires in 9s and not in 7s.
- Both digits also trigger the large-hole detector in row 1, so that detector cannot decide between them.
- LOOP_s and the narrow-gap detectors are still unmeasured and unused.

**A better probe design.** Earlier probes only showed which feature was largest. This one gives the full yes/no pattern for three features at once.
- Each output k corresponds to a subset S of the three features. Its logit is β·Σ_{i∈S}(F_i − t).
- The argmax is then exactly the set of features that are above threshold.

The three features, each summed over a half of the grid with threshold t = 0.05:

| Feature | Detector | Region |
|---|---|---|
| F1 | LOOP_s | top half (rows 0–1) |
| F2 | LOOP_s | bottom half (rows 2–3) |
| F3 | HB_s (narrow left-right gap) | top half |

Output k = F1 + 2·F2 + 4·F3, where each F is 1 if it is above threshold. Outputs 8–9 are unused. Each digit's row in the confusion matrix then gives the joint presence distribution of the three features. conv1 and conv2 are unchanged from step 19.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 5 (binary-subset readout):
    #   F1 = LOOP_s (ch5) summed over rows 0-1
    #   F2 = LOOP_s (ch5) summed over rows 2-3
    #   F3 = HB_s   (ch7) summed over rows 0-1
    #   output index = [F1>t] + 2*[F2>t] + 4*[F3>t]
    # conv1/conv2 identical to step 19.
    # ==================================================================
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))
        w = w - w.mean()
        w = w / w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()
    W1[4, 0] = g;        b1[4] = -0.1
    W1[5, 0] = -2.5 * g; b1[5] = 1.0
    W1[6, 0] = 3.0 * g;  b1[6] = -0.3
    W1[7, 0] = 3.0 * g;  b1[7] = -1.3

    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def sat(ch, r, c, w):
        W2[ch, 6, r, c] += w
        W2[ch, 7, r, c] -= w

    near = {'U': (1, 2), 'D': (3, 2), 'L': (2, 1), 'R': (2, 3)}
    far = {'U': (0, 2), 'D': (4, 2), 'L': (2, 0), 'R': (2, 4)}

    def detector(ch, taps, sides_req, sides_forbid=()):
        W2[ch, 5, 2, 2] = 1.0
        for sd in sides_req:
            sat(ch, *taps[sd], 1.0)
        for sd in sides_forbid:
            sat(ch, *taps[sd], -1.0)
        b2[ch] = -(len(sides_req) + 1 - 0.6)

    detector(5, near, 'UDLR')
    detector(6, far, 'UDLR')
    detector(7, near, 'LR')
    detector(8, near, 'UD')
    detector(9, far, 'LR')
    detector(10, far, 'UD')
    detector(11, far, 'UDR', 'L')
    detector(12, far, 'UDL', 'R')
    detector(13, far, 'LRD', 'U')
    detector(14, far, 'LRU', 'D')

    # binary-subset probe readout
    beta, thr = 50.0, 0.05
    idx = lambda c, i, j: c * 16 + i * 4 + j
    feats = [(5, (0, 1)), (5, (2, 3)), (7, (0, 1))]     # (channel, rows)
    fvec = []
    for (ch, rows) in feats:
        v = np.zeros(256)
        for i in rows:
            for j in range(4):
                v[idx(ch, i, j)] = 1.0
        fvec.append(v)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for S in range(8):
        for n in range(3):
            if (S >> n) & 1:
                Wf[S] += beta * fvec[n]
                bf[S] -= beta * thr
    bf[8] = -1000.0
    bf[9] = -1000.0

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
