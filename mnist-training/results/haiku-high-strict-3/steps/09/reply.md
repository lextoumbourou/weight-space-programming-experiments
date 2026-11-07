**Step 9 plan: go back to the step-6 fc layer and balance the classes with a prior-matching bias correction.**

Step 8 confirmed the ungrouped 3x3 zero-sum templates don't work. Class 1 absorbed about 2,900 predictions, because its centre-column weight matches the central ink of most digits. The step-6 design (4x4 templates, per-cell mean removal) is still the best at 36.2%, so I'm reverting to it.

Its remaining problem is class balance. Predicted counts were roughly 2,300 for 5, 1,800 for 3, 1,650 for 4 and 1,600 for 2, while 6 got 0, 7 got about 30, and 9 and 8 got a few hundred each. I'm applying a log-ratio correction: each bias moves by -ln(predicted count / 1000), with the upward moves for 6, 7, 8 and 9 capped so one class doesn't flood the others. Templates and conv layers are unchanged.

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
    # every conv2 channel with the same weight (the step-6 design).
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

    # Class biases: prior-matching correction from the step-6 confusion counts.
    # bias_d = previous_bias - ln(predicted_count_d / 1000), with upward
    # moves capped for the classes that were almost never predicted.
    bfc = np.array([
        -0.1,   # 0  (~1150 predicted, slightly high)
        0.3,    # 1  (~935 predicted)
        -0.8,   # 2  (~1580 predicted)
        -1.2,   # 3  (~1800 predicted)
        -1.2,   # 4  (~1650 predicted)
        -1.6,   # 5  (~2300 predicted)
        1.6,    # 6  (0 predicted, capped)
        1.6,    # 7  (~30 predicted, capped)
        1.2,    # 8  (~350 predicted)
        1.6,    # 9  (~230 predicted, capped)
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
