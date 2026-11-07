**Step 2 plan: fix calibration and class bias, then tweak templates.**

The loss of 17.3 means the logits are far too large. Wrong classes are scored with huge confidence, so the fc scale needs to drop. I'm reducing it from 0.1 to 0.02.

The confusion matrix also shows class-prior problems. Predictions pile into 4 and 5, while 6, 7 and 9 are almost never predicted. I'm adding small per-class biases: negative for 3, 4 and 5, positive for 1, 6, 7 and 9. Finally, I'm redrawing the templates for 6, 7 and 9 to better match their stroke layouts.

The conv layers are unchanged, since the feedback doesn't yet point to a problem there.

```python
import numpy as np


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters, each 1x5x5. Shape (out=8, in=1, 5, 5).
    # Coordinates: r = row offset inside the 5x5 window, c = column offset.
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)

    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing='ij')

    # Filter 0: vertical stroke detector.
    v = np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.5))
    W1[0, 0] = v

    # Filter 1: horizontal stroke detector.
    W1[1, 0] = v.T

    # Filter 2: '/' diagonal detector.
    d = r + c - 4
    W1[2, 0] = np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.5))

    # Filter 3: '\' diagonal detector.
    d2 = r - c
    W1[3, 0] = np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.5))

    # Filter 4: centre-surround blob detector.
    inner = (np.abs(r - 2) <= 1) & (np.abs(c - 2) <= 1)
    W1[4, 0] = np.where(inner, 0.2, -0.1)

    # Filter 5: upper-half minus lower-half.
    W1[5, 0] = np.where(r <= 1, 0.5, np.where(r == 2, 0.0, -0.5))

    # Filter 6: identity (centre pixel pass-through).
    W1[6, 0] = np.where((r == 2) & (c == 2), 1.0, 0.0)

    # Filter 7: local ink mass with a threshold.
    W1[7, 0] = 0.2
    b1[7] = -0.3

    # ------------------------------------------------------------------
    # conv2: 16 filters, each 8x5x5. Shape (out=16, in=8, 5, 5).
    # ------------------------------------------------------------------
    P = []
    # 0: vertical bar
    P.append(np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.3)))
    # 1: horizontal bar
    P.append(np.where(r == 2, 1.0, np.where((r == 1) | (r == 3), 0.3, -0.3)))
    # 2: '/' diagonal
    P.append(np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.3)))
    # 3: '\' diagonal
    P.append(np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.3)))
    # 4: 3x3 blob
    P.append(np.where(inner, 0.2, 0.0))
    # 5: centre point
    P.append(np.where((r == 2) & (c == 2), 1.0, 0.0))
    # 6: top half positive, bottom half negative
    P.append(np.where(r <= 1, 0.5, np.where(r >= 3, -0.5, 0.0)))
    # 7: bottom half positive, top half negative
    P.append(np.where(r >= 3, 0.5, np.where(r <= 1, -0.5, 0.0)))
    P = [p.astype(np.float32) for p in P]

    W2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.1, dtype=np.float32)
    for o in range(16):
        # Main input: channel o%8 with pattern o%8.
        W2[o, o % 8] += P[o % 8]
        # Weaker secondary input: channel (o+3)%8 with another pattern.
        W2[o, (o + 3) % 8] += 0.5 * P[(o + 4) % 8]

    # ------------------------------------------------------------------
    # fc: 10 x 256. Input index = channel*16 + row*4 + col (4x4 pooled grid).
    # Each class has a 4x4 "expected ink" template applied to every channel.
    # ------------------------------------------------------------------
    T = np.array([
        # 0: ring
        [[0, 1, 1, 0], [1, -1, -1, 1], [1, -1, -1, 1], [0, 1, 1, 0]],
        # 1: centre vertical stroke
        [[-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1]],
        # 2: top arc, diagonal, bottom bar
        [[0, 1, 1, 0], [-1, -1, 1, 0], [-1, 1, 0, -1], [1, 1, 1, 1]],
        # 3: right-side bulges, top and bottom arcs
        [[0, 1, 1, 0], [-1, -1, 1, 1], [-1, -1, 1, 1], [0, 1, 1, 0]],
        # 4: open top-left, cross bar, right stem
        [[-1, 0, 1, -1], [0, 1, 1, 0], [1, 1, 1, 1], [-1, -1, 1, -1]],
        # 5: top bar, left stem, bottom bowl
        [[1, 1, 1, 1], [1, -1, -1, -1], [0, 1, 1, 0], [-1, 1, 1, 0]],
        # 6: left stroke running down into a lower loop (redrawn)
        [[-1, 1, 1, 0], [1, 0, -1, -1], [1, -1, -1, 1], [0, 1, 1, 0]],
        # 7: top bar, then diagonal stem down the left-centre (redrawn)
        [[1, 1, 1, 1], [-1, -1, 1, 0], [-1, 1, 0, -1], [-1, 1, 0, -1]],
        # 8: two stacked loops
        [[0, 1, 1, 0], [1, -1, -1, 1], [0, 1, 1, 0], [1, -1, -1, 1]],
        # 9: closed top loop with right stem descending (redrawn)
        [[0, 1, 1, 0], [1, -1, -1, 1], [-1, -1, 1, 1], [-1, 1, 1, 0]],
    ], dtype=np.float32)

    # Remove the per-cell mean across classes so no class is favoured
    # by generic activity.
    T = T - T.mean(axis=0, keepdims=True)

    # Smaller scale than step 1 (0.1 -> 0.02) to stop overconfident wrong logits.
    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * T[d_cls].reshape(16)

    # Per-class biases to correct the class prior seen in the confusion matrix.
    # Over-predicted classes (3, 4, 5) get negative bias; under-predicted
    # classes (1, 6, 7, 9) get positive bias.
    bfc = np.array([
        0.0,   # 0
        0.3,   # 1
        0.0,   # 2
        -0.2,  # 3
        -0.4,  # 4
        -0.5,  # 5
        0.3,   # 6
        0.4,   # 7
        0.0,   # 8
        0.2,   # 9
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
