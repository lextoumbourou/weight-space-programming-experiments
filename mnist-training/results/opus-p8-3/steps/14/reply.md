## Step 14: diagnostic probe of the loop features

**What steps 12–13 showed.** Strengthening the loop expectations for 6 and 9 made them worse: 6→0 rose to 285 and 9→0 to 164. My mental model of where the loop detectors fire must be wrong, and I have no direct view of the features. So this step spends one evaluation on measuring them.

**How the probe works.** I keep conv1 and conv2 exactly as in step 13 and turn the fc layer into a readout. The output "class" index then shows which feature region fired most, not a digit.

| Output | Meaning |
|---|---|
| 0–3 | LOOP detector (ch9), average of the two central columns, in grid rows 0, 1, 2, 3 |
| 4–7 | wide gap detector HB2 (ch5), same layout, rows 0–3 |
| 8 | "nothing fired": a constant threshold logit |
| 9 | unused |

LOOP values are divided by 0.1 and HB2 values by 0.2, so each is measured relative to its threshold. A large β makes the output close to a hard argmax.

**How to read it.** Each row of the confusion matrix (true digit) becomes a histogram. It shows whether loops are detected in that digit at all, and in which grid row. This step's loss will be poor on purpose; the best earlier step is still kept for scoring.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE: conv1/conv2 identical to step 13; fc reads out
    # where the LOOP (ch9) and HB2 (ch5) detectors fire.
    # ==================================================================
    # conv1: ch0-3 oriented lines, ch4 ink, ch5 background
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
    W1[4, 0] = g
    b1[4] = -0.1
    W1[5, 0] = -1.5 * g
    b1[5] = 1.0

    # conv2: same as step 13
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def pair_detector(ch, taps):
        W2[ch, 5, 2, 2] = 1.0
        for (r, c) in taps:
            W2[ch, 4, r, c] = 1.0
        b2[ch] = -1.8

    pair_detector(5, [(2, 0), (2, 4)])   # HB2
    pair_detector(6, [(0, 2), (4, 2)])   # VB2
    pair_detector(7, [(2, 1), (2, 3)])   # HB1
    pair_detector(8, [(1, 2), (3, 2)])   # VB1
    W2[9, 5, 2, 2] = 1.0                 # LOOP
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        W2[9, 4, r, c] = 0.6
    b2[9] = -2.2

    # fc probe
    beta = 10.0
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    idx = lambda c, i, j: c * 16 + i * 4 + j
    for r in range(4):
        for j in (1, 2):
            Wf[r, idx(9, r, j)] = beta * 0.5 / 0.1        # LOOP row r (avg of 2 cols)/0.1
            Wf[4 + r, idx(5, r, j)] = beta * 0.5 / 0.2    # HB2 row r (avg of 2 cols)/0.2
    bf[8] = beta * 1.0        # "nothing over threshold"
    bf[9] = -100.0            # unused

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
