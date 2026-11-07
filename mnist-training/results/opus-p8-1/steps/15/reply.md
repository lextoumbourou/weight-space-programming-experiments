## Step 15: probe, horizontal strokes in cells 3, 4, 5

**Step 14 results.** These are P(horizontal stroke present) for top-row cells 0, 1 and 2, decoded from the 3-bit codes:

| digit | cell (0,0) | cell (0,1) | cell (0,2) |
|---|---|---|---|
| 0 | .04 | .33 | .61 |
| 1 | ~0 | ~0 | ~0 |
| 2 | .11 | .49 | .41 |
| 3 | .11 | .76 | .66 |
| 4 | ~0 | .03 | .03 |
| 5 | ~0 | .51 | .86 |
| 6 | ~0 | .01 | .03 |
| 7 | .04 | .84 | .87 |
| 8 | .04 | .55 | .78 |
| 9 | .03 | .79 | .93 |

These are very informative. A top bar separates {7, 9, 5, 3, 8} from {1, 4, 6}, and real digits sit slightly right of centre at the top.

**This step.** Same probe network. I test horizontal presence in cell (0,3), the top-right corner, and in cells (1,0) and (1,1), the left half of the second row. Bit i of the output class is test i.

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
    tests = [(1, 3), (1, 4), (1, 5)]   # horizontal presence in cells 3, 4, 5
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
