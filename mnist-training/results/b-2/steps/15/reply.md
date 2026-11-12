# Step 15: measure the U-bay detector (channel 5)

**The measured weighting worked.** Replacing the hand-guessed weights of channels 4 and 7 with terms built from their measured class statistics gave the best step so far:
- accuracy rose from 70.3% to 72.7%, and loss fell from 0.928 to 0.897;
- 2 jumped from 619 to 803 correct, and 3 → 2, 5 → 2, 7 → 2 mostly disappeared.

The remaining structural channels (5, 6, 8, 9) still use hand-guessed templates, which may be just as wrong as those of channels 4 and 7 were.

**This step: another diagnostic.** I measure channel 5, the U-shaped bay open at the top, in the same way as before:
- h1 = its sum over the top two rows of cells; h2 = its sum over the bottom two rows.
- Each goes into bins split at 0.02 and 0.5, and the predicted class is 3·bin(h1) + bin(h2).
- Row d of the confusion matrix is then the joint histogram for digit d.

The conv layers are exactly those of the current best network. Next I will measure channels 6, 8 and 9, then weight them all from data.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1 (unchanged) =================
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

    # ================= conv2 (unchanged) =================
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

    # ================= fc: DIAGNOSTIC 3x3 histogram of channel 5 (U bay, open top) =================
    MEAS = 5
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
