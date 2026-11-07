## Step 30: probe the gap detectors that are still unmeasured

**Lesson from step 29.** Removing the templates entirely made things worse: loss 0.588 against 0.517 with β = 1.5. They still add some information, so the next build restores β = 1.5.

**Next measurements.** The main remaining confusions are 7→9 (98–154), 3→5 (112), 0→2 (64), 3→2 (72) and 6→0 (59). Several gap detectors have never been measured and should help with these:

| Feature | Definition | Expected to separate |
|---|---|---|
| F1 | wide left-right gap (HB_l) in the middle rows 1–2 | the open interior of a 0 from 2, 3 and 7 |
| F2 | narrow left-right gap (HB_s) in the bottom half | the lower loops of 6 and 8 |
| F3 | narrow up-down gap (VB_s) in the top half | the upper loop of 9 vs 7; 3's upper cavity |

These are topology detectors, which output about 0.3–0.6 when they fire, so the presence threshold is 0.05 rather than 0.8.

The readout is the same binary-subset design: output = F1 + 2·F2 + 4·F3. conv1 and conv2 are unchanged.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 10 (binary-subset readout), topology features:
    #   F1 = HB_l (ch9) rows1-2, all cols > 0.05
    #   F2 = HB_s (ch7) rows2-3, all cols > 0.05
    #   F3 = VB_s (ch8) rows0-1, all cols > 0.05
    #   output index = F1 + 2*F2 + 4*F3
    # conv1/conv2 identical to step 28.
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

    beta, thr = 50.0, 0.05
    idx = lambda c, i, j: c * 16 + i * 4 + j

    def region(ch, rows, cols):
        v = np.zeros(256)
        for i in rows:
            for j in cols:
                v[idx(ch, i, j)] = 1.0
        return v

    fvec = [region(9, [1, 2], range(4)),
            region(7, [2, 3], range(4)),
            region(8, [0, 1], range(4))]
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
