**Step 10 plan: keep the step-9 fc design and apply another round of prior-matching bias correction.**

Step 9 gained a little, to 36.5%, but the counts still show imbalance. Class 6 is still barely predicted (22 times, with 4 correct), 5 is over-predicted (about 1,860), and 7 is being sent to 9 (449 of 1,000 sevens). I'm applying the same log-ratio correction as before: each bias moves by -ln(predicted / 1000). Class 6 gets a larger upward move, and class 7 is raised but capped so it doesn't flood class 9. The templates and conv layers are unchanged, so this step isolates the effect of the bias correction.

Six steps are left. Unless the bias changes produce something new, this design is near its ceiling, and I may need to try different templates in later steps.

```python
import numpy as np


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters, each 1x5x5. Shape (out=8, in=1, 5, 5).
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)

    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing='ij')

    v = np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.5))
    W1[0, 0] = v                                   # vertical stroke
    W1[1, 0] = v.T                                 # horizontal stroke
    d = r + c - 4
    W1[2, 0] = np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.5))  # '/'
    d2 = r - c
    W1[3, 0] = np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.5))  # '\'
    inner = (np.abs(r - 2) <= 1) & (np.abs(c - 2) <= 1)
    W1[4, 0] = np.where(inner, 0.2, -0.1)          # centre-surround blob
    W1[5, 0] = np.where(r <= 1, 0.5, np.where(r == 2, 0.0, -0.5))  # top vs bottom
    W1[6, 0] = np.where((r == 2) & (c == 2), 1.0, 0.0)            # identity
    W1[7, 0] = 0.2                                 # local ink mass
    b1[7] = -0.3

    # ------------------------------------------------------------------
    # conv2: 16 filters, each 8x5x5. Output o uses conv1 channel o%8 with
    # spatial pattern P[o%8], plus a weaker input from channel (o+3)%8.
    # ------------------------------------------------------------------
    P = []
    P.append(np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.3)))
    P.append(np.where(r == 2, 1.0, np.where((r == 1) | (r == 3), 0.3, -0.3)))
    P.append(np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.3)))
    P.append(np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.3)))
    P.append(np.where(inner, 0.2, 0.0))
    P.append(np.where((r == 2) & (c == 2), 1.0, 0.0))
    P.append(np.where(r <= 1, 0.5, np.where(r >= 3, -0.5, 0.0)))
    P.append(np.where(r >= 3, 0.5, np.where(r <= 1, -0.5, 0.0)))
    P = [p.astype(np.float32) for p in P]

    W2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.1, dtype=np.float32)
    for o in range(16):
        W2[o, o % 8] += P[o % 8]
        W2[o, (o + 3) % 8] += 0.5 * P[(o + 4) % 8]

    # ------------------------------------------------------------------
    # fc: 10 x 256. One 4x4 "expected ink" template per digit, applied to
    # every conv2 channel with the same weight.
    # ------------------------------------------------------------------
    T = np.array([
        [[0, 1, 1, 0], [1, -1, -1, 1], [1, -1, -1, 1], [0, 1, 1, 0]],     # 0
        [[-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1]],  # 1
        [[0, 1, 1, 0], [-1, -1, 1, 0], [-1, 1, 0, -1], [1, 1, 1, 1]],     # 2
        [[0, 1, 1, 0], [-1, -1, 1, 1], [-1, -1, 1, 1], [0, 1, 1, 0]],     # 3
        [[-1, 0, 1, -1], [0, 1, 1, 0], [1, 1, 1, 1], [-1, -1, 1, -1]],    # 4
        [[1, 1, 1, 1], [1, -1, -1, -1], [0, 1, 1, 0], [-1, 1, 1, 0]],     # 5
        [[-1, 1, 1, 0], [1, 0, -1, -1], [1, -1, -1, 1], [0, 1, 1, 0]],    # 6
        [[1, 1, 1, 1], [-1, -1, 1, 0], [-1, 1, 0, -1], [-1, 1, 0, -1]],   # 7
        [[0, 1, 1, 0], [1, -1, -1, 1], [0, 1, 1, 0], [1, -1, -1, 1]],     # 8
        [[0, 1, 1, 0], [1, -1, -1, 1], [-1, -1, 1, 1], [-1, 1, 1, 0]],    # 9
    ], dtype=np.float32)

    # Remove the per-cell mean across classes so no class is favoured by generic ink.
    T = T - T.mean(axis=0, keepdims=True)

    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * T[d_cls].reshape(16)

    # Class biases: another prior-matching correction from the step-9 counts.
    # Predicted counts were ~1140 (0), 1020 (1), 1510 (2), 1455 (3), 1630 (4),
    # 1860 (5), 22 (6), 143 (7), 676 (8), 537 (9).
    bfc = np.array([
        -0.2,   # 0  (~1140, slightly high)
        0.3,    # 1  (~1020)
        -1.2,   # 2  (~1510)
        -1.6,   # 3  (~1455)
        -1.7,   # 4  (~1630)
        -2.2,   # 5  (~1860, most over-predicted)
        3.0,    # 6  (22 predicted, capped upward move)
        2.5,    # 7  (143 predicted, capped to avoid flooding class 9)
        1.6,    # 8  (~676)
        1.6,    # 9  (~537, held because 7 is already sent to 9)
    ], dtype=np.float32)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
```
