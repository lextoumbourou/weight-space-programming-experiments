# Step 13: measure the open-left bay detector (channel 7)

**What step 12 showed about the hole detector.** Its per-class histograms contradict my assumptions:

| Assumption | Measured |
|---|---|
| Fires inside the small loops of 9, 6 and 8 | Rarely fires there: most 8s show no hole, 6s show only a weak top response, 9s mostly a weak bottom one |
| Specific to closed loops | Fires strongly inside 0 (top and bottom), above the tail of 2, in 3's lower bay, in the open top of 4, and in both parts of 5 |

So in practice it is a "large enclosed region" detector. The template I gave it for "9 = hole in the top" pointed the wrong way, which partly explains the 4 → 9 and 2 → 9 errors.

**Plan.** The bay detectors (channels 5–8) were designed with the same untested assumptions. Before re-weighting all the structural features from measured statistics, I measure each of them the same way. This step measures channel 7, the bay open to the left (meant for 3's bays and 5's lower bowl):
- h1 = its sum over the top two rows of cells; h2 = its sum over the bottom two rows.
- Each goes into bins split at 0.02 and 0.5, and the predicted class is 3·bin(h1) + bin(h2).
- Row d of the confusion matrix is then the joint histogram for digit d.

The conv layers stay exactly as in the step-11 network. This step's loss will be meaningless, as before.

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

    # ================= fc: DIAGNOSTIC 3x3 histogram of channel 7 (open-left bay) =================
    MEAS = 7
    def idx(ch, r, c):
        return ch * 16 + r * 4 + c
    v1 = np.zeros(256)
    v2 = np.zeros(256)
    for r in range(4):
        for c in range(4):
            if r < 2:
                v1[idx(MEAS, r, c)] = 1.0
            else:
                v2[idx(MEAS, r, c)] = 1.0

    t1, t2 = 0.02, 0.5
    s = 200.0
    gw = [0.0, s, 2 * s]
    gb = [0.0, -s * t1, -s * (t1 + t2)]

    fc_w = np.zeros((10, 256))
    fc_b = np.zeros(10)
    for i in range(3):
        for j in range(3):
            k = 3 * i + j
            fc_w[k] = gw[i] * v1 + gw[j] * v2
            fc_b[k] = gb[i] + gb[j]
    fc_b[9] = -1e4

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
