## Step 17: probe, horizontal strokes in cells 9, 10, 11

**Step 16 results.** These are P(horizontal stroke present) for cells (1,2), (1,3) and (2,0):

| digit | cell (1,2) | cell (1,3) | cell (2,0) |
|---|---|---|---|
| 0 | .04 | .02 | .00 |
| 1 | .00 | .00 | .00 |
| 2 | .05 | .01 | .32 |
| 3 | .55 | .09 | .16 |
| 4 | .06 | .02 | .58 |
| 5 | .54 | .16 | .14 |
| 6 | .37 | .38 | .00 |
| 7 | .22 | .10 | .05 |
| 8 | .23 | .20 | .03 |
| 9 | .18 | .03 | .34 |

The patterns match intuition. The crossbar of 4 shows up on the left at row 2, the middle bars of 3 and 5 at cell (1,2), and the top of the loop of 6 at row 1 on the right.

**This step.** Same probe network. I test horizontal presence in cells (2,1), (2,2) and (2,3). Bit i of the output class is test i.

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
    tests = [(1, 9), (1, 10), (1, 11)]   # horizontal presence in cells 9, 10, 11
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
