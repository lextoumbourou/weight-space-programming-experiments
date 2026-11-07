## Step 16: probe, horizontal strokes in cells 6, 7, 8

**Step 15 results.** These are P(horizontal stroke present) for cells (0,3), (1,0) and (1,1):

| digit | cell (0,3) | cell (1,0) | cell (1,1) |
|---|---|---|---|
| 0 | .39 | .02 | .05 |
| 1 | .02 | .00 | .01 |
| 2 | .12 | .05 | .07 |
| 3 | .21 | .15 | .58 |
| 4 | .03 | .03 | .07 |
| 5 | .77 | .17 | .57 |
| 6 | .02 | .00 | .05 |
| 7 | .51 | .30 | .35 |
| 8 | .47 | .05 | .13 |
| 9 | .31 | .05 | .22 |

I also recounted step 14 including the all-three-present column. The corrected P for cell (0,0) is 0.27 for "2", 0.43 for "3" and 0.53 for "7".

**This step.** Same probe network. I test horizontal presence in cells (1,2), (1,3) and (2,0). Bit i of the output class is test i.

```python
import numpy as np
import math

def build_weights():
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)

    # ---------------- conv1 ----------------
    G = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            G[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / 2.0)
    W1[0, 0] = G / G.sum()
    b1[0] = -0.05
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]   # ch1..4: H, V, "\", "/"
    for k, th in enumerate(thetas):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                r, c = i - 2, j - 2
                d = r * math.cos(th) - c * math.sin(th)
                l = r * math.sin(th) + c * math.cos(th)
                K[i, j] = (1 - d * d / 2.0) * math.exp(-d * d / 4.0) * math.exp(-l * l / 12.0)
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[1 + k, 0] = K
        b1[1 + k] = -0.1

    # ---------------- conv2: pass-through (centre tap) ----------------
    for k in range(5):
        W2[k, k, 2, 2] = 1.0

    # ---------------- fc: PROBE (3-bit code of feature > thr) ----------------
    tests = [(1, 6), (1, 7), (1, 8)]   # horizontal presence in cells 6, 7, 8
    thr = 0.35
    Kbig = 100.0
    for c in range(8):
        for i, (ch, cell) in enumerate(tests):
            s = 1.0 if (c >> i) & 1 else -1.0
            Wf[c, ch * 16 + cell] += Kbig * s
            bf[c] += -Kbig * s * thr
    bf[8] = -1e4
    bf[9] = -1e4

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
