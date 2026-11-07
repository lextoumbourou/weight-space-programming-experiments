## Step 38: probe features for the 7 vs 9 confusion

**Where things stand.** The three new stroke features gave a new best: loss 0.473 and accuracy 84.9%.
- 0→2 fell from 64 to 46.
- 9 recall rose from 690 to 726.
- 7→9 is still the largest error at 155.
- 7 is also under-predicted: 885 predictions for 1,028 true 7s. I will raise its bias in the next build.

**Next probe, aimed at 7 vs 9.** A 7's top bar is long and straight from the far left to the far right. A 9's top is a rounded loop that is narrower at the corners. A 9's stem is also on the right, while a 7's runs through the centre.

| Feature | Definition | Threshold |
|---|---|---|
| F1 | horizontal stroke in the top-left cell (0, 0) | 0.4 |
| F2 | horizontal stroke in the top-right cell (0, 3) | 0.4 |
| F3 | ink in the lower part of the right column (rows 2–3, col 3) | 0.8 |

F1 and F2 are single cells, so their threshold is lower than for the multi-cell regions. The readout is the same binary-subset design: output = F1 + 2·F2 + 4·F3. conv1 and conv2 are unchanged.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 12 (binary-subset readout):
    #   F1 = horizontal (ch0) cell (0,0)         > 0.4
    #   F2 = horizontal (ch0) cell (0,3)         > 0.4
    #   F3 = ink (ch4) rows2-3, col3             > 0.8
    #   output index = F1 + 2*F2 + 4*F3
    # conv1/conv2 identical to step 37.
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

    beta = 50.0
    idx = lambda c, i, j: c * 16 + i * 4 + j

    def region(ch, rows, cols):
        v = np.zeros(256)
        for i in rows:
            for j in cols:
                v[idx(ch, i, j)] = 1.0
        return v

    fvec = [region(0, [0], [0]),
            region(0, [0], [3]),
            region(4, [2, 3], [3])]
    thrs = [0.4, 0.4, 0.8]
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for S in range(8):
        for n in range(3):
            if (S >> n) & 1:
                Wf[S] += beta * fvec[n]
                bf[S] -= beta * thrs[n]
    bf[8] = -1000.0
    bf[9] = -1000.0

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
