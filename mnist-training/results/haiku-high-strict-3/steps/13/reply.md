**Step 13 plan: another small prior-matching correction from the step-12 counts.**

Step 12 is the best so far at 36.68%, so it's the baseline. Its counts are still uneven: 5 got about 1,720 predictions (320 correct), 4 got 1,590, 2 got 1,540 and 3 got 1,500. Class 6 got only 25, and 9 got 561, mostly from 7s. Class 7 is under-predicted and its images are being taken by 9 (458 of 1,000), so I'm raising 7 a little. Class 9 has very low recall (44), so taking some 7s from it is a good trade.

Changes from step 12:
- Lower 5, 4, 3 and 2 by about -ln(predicted / 1000).
- Raise 8 and 6 modestly.
- Raise 7 to 2.3 so it competes better with 9.

Templates and conv layers are unchanged. With two steps left, I'll return to whichever bias set scores best for the final step.

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

    # Class biases: step-12 set, with prior-matching moves from the step-12 counts.
    # Predicted counts: ~1160 (0), ~1040 (1), ~1540 (2), ~1500 (3), ~1590 (4),
    # ~1720 (5), 25 (6), 146 (7), 730 (8), 560 (9).
    bfc = np.array([
        -0.25,  # 0
        0.3,    # 1
        -1.2,   # 2  (was -0.8)
        -1.6,   # 3  (was -1.2)
        -1.8,   # 4  (was -1.4)
        -2.4,   # 5  (was -1.9)
        2.0,    # 6  (was 1.6; still under-predicted)
        2.3,    # 7  (was 1.6; should take some 7-vs-9 cases back from 9)
        1.5,    # 8  (was 1.2)
        1.6,    # 9
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
