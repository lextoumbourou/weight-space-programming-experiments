# Step 12: a diagnostic step to measure how the hole detector behaves

Accuracy is 70% and loss 0.93. Further blind template tweaks are giving little, and I cannot see the feature values directly. Instead of guessing, I use this step to measure one thing: how the hole detector (conv2 channel 4) responds on each digit class.

**How the measurement works.** The fc layer reads two numbers from the 4×4 hole map:
- h1: the sum of the hole map over the top two rows of cells (loops in the upper half, as in 9, 8 and closed 4s);
- h2: the sum over the bottom two rows (loops in the lower half, as in 6, 8 and 0).

Each number is sorted into one of three bins using thresholds 0.02 and 0.5:

| Bin | Range | Meaning |
|---|---|---|
| 0 | below 0.02 | no hole |
| 1 | 0.02 to 0.5 | weak hole |
| 2 | above 0.5 | strong hole |

**The logits are built so the argmax reports the bins.**
- The logit for class 3·i + j is (sum of step functions of h1 up to bin i) + (the same for h2 up to bin j), with very steep slopes.
- The argmax is therefore the output class 3·bin(h1) + bin(h2), covering classes 0–8. Class 9 is never chosen.
- Row d of the confusion matrix is then the joint 3×3 histogram of (top hole, bottom hole) for true digit d.

This step's loss and accuracy will be very poor. That is expected and does not matter, because the step with the lowest loss is the one finally scored. With these per-class firing rates I can weight the structural features properly in later steps. The conv layers are identical to step 11, so the measurement applies directly to the current best network.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1 (identical to step 11) =================
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    def edge_kernel(theta):
        K = np.zeros((5, 5))
        ct, st = math.cos(theta), math.sin(theta)
        for r in range(5):
            for c in range(5):
                u = c - 2
                v = -(r - 2)
                a = u * ct + v * st
                n = -u * st + v * ct
                K[r, c] = n * math.exp(-a * a / (2 * 1.5 ** 2) - n * n / (2 * 1.0 ** 2))
        K /= K[K > 0].sum()
        return K

    for k, th in enumerate(thetas):
        K = edge_kernel(th)
        conv1_w[2 * k, 0] = K
        conv1_w[2 * k + 1, 0] = -K
        conv1_b[2 * k] = -0.25
        conv1_b[2 * k + 1] = -0.25

    INK_ABOVE, INK_BELOW, INK_LEFT, INK_RIGHT = 0, 1, 4, 5

    # ================= conv2 (identical to step 11) =================
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15

    w = 0.2
    def wall(c, side, wt):
        if side == 'L':
            conv2_w[c, INK_LEFT, 1:4, 0:2] += wt
        elif side == 'R':
            conv2_w[c, INK_RIGHT, 1:4, 3:5] += wt
        elif side == 'T':
            conv2_w[c, INK_ABOVE, 0:2, 1:4] += wt
        elif side == 'B':
            conv2_w[c, INK_BELOW, 3:5, 1:4] += wt

    def empty_centre(c, pen=0.4):
        conv2_w[c, :, 2, 2] -= pen

    for s in 'LRTB':
        wall(4, s, w)
    empty_centre(4)
    conv2_b[4] = -0.8
    bays = {5: ('LRB', 'T'), 6: ('LRT', 'B'), 7: ('TRB', 'L'), 8: ('TLB', 'R')}
    for c, (walls_on, open_side) in bays.items():
        for s in walls_on:
            wall(c, s, w)
        wall(c, open_side, -2 * w)
        empty_centre(c)
        conv2_b[c] = -0.5
    conv2_w[9, INK_LEFT, 0:5, 0:2] += 0.15
    conv2_w[9, INK_RIGHT, 0:5, 3:5] += 0.15
    empty_centre(9)
    conv2_b[9] = -0.7

    # ================= fc: DIAGNOSTIC 3x3 histogram =================
    # h1 = sum of hole map (channel 4) over cell rows 0-1; h2 = over cell rows 2-3.
    def idx(ch, r, c):
        return ch * 16 + r * 4 + c
    v1 = np.zeros(256)
    v2 = np.zeros(256)
    for r in range(4):
        for c in range(4):
            if r < 2:
                v1[idx(4, r, c)] = 1.0
            else:
                v2[idx(4, r, c)] = 1.0

    t1, t2 = 0.02, 0.5
    s = 200.0
    # step-function pieces: g_0 = 0, g_1 = s(h - t1), g_2 = s(2h - t1 - t2)
    gw = [0.0, s, 2 * s]
    gb = [0.0, -s * t1, -s * (t1 + t2)]

    fc_w = np.zeros((10, 256))
    fc_b = np.zeros(10)
    for i in range(3):
        for j in range(3):
            k = 3 * i + j
            fc_w[k] = gw[i] * v1 + gw[j] * v2
            fc_b[k] = gb[i] + gb[j]
    fc_b[9] = -1e4   # class 9 never chosen

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
