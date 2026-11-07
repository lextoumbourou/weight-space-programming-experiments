## Step 22: probe stroke features for naive Bayes

**Where things stand.** The naive-Bayes topology scoring was a big jump: loss 0.720 and accuracy 76.7%. Features with measured per-digit statistics clearly beat hand-guessed templates. The next step is to measure the most discriminative stroke features too, so they can join the naive-Bayes part.

**Which features.** I chose three aimed at the biggest remaining confusions: 7 (49% recall, lost to 9, 2, 5 and 3) and 3→5.

| Feature | Definition | Expected to separate |
|---|---|---|
| F1 | horizontal stroke in grid row 0 (top bar) | 7, 5 from 9, 3 |
| F2 | horizontal stroke in grid row 3 (bottom bar) | 2 from 7 |
| F3 | vertical stroke in the upper-left 2×2 block | 5 from 3; 4 and 6 |

Each feature is the sum of its conv2 channel over the region, with "present" meaning a sum above 0.8.

**Readout.** As in step 20, output k = F1 + 2·F2 + 4·F3, where each F is 1 if present. Outputs 8–9 are unused. Each digit's row gives the joint presence of the three features. conv1 and conv2 are unchanged.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 6 (binary-subset readout), stroke features:
    #   F1 = horizontal (ch0) summed over row 0          > 0.8
    #   F2 = horizontal (ch0) summed over row 3          > 0.8
    #   F3 = vertical   (ch2) summed over rows0-1,cols0-1 > 0.8
    #   output index = F1 + 2*F2 + 4*F3
    # conv1/conv2 identical to step 21.
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
    beta, thr = 50.0, 0.8
    idx = lambda c, i, j: c * 16 + i * 4 + j

    def region(ch, rows, cols):
        v = np.zeros(256)
        for i in rows:
            for j in cols:
                v[idx(ch, i, j)] = 1.0
        return v

    fvec = [region(0, [0], range(4)),
            region(0, [3], range(4)),
            region(2, [0, 1], [0, 1])]
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
