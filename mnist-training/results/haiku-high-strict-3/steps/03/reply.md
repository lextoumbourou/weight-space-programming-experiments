**Step 3 plan: make the fc layer orientation-aware.**

Loss fell from 17.3 to 3.98, but accuracy stayed at about 36%. Calibration is no longer the main problem. The fc layer treats all 16 conv2 channels identically, so it can only use where ink is, not what kind of stroke it is. A 1 and a 7 with ink in the same cells look the same to it.

The conv2 channels are grouped by their spatial pattern: channels o and o+8 share pattern o%8. So I'm splitting the fc weights into five groups: vertical, horizontal, '/' diagonal, '\' diagonal, and blob/other. Each digit gets a separate 4x4 template for each group, describing where that stroke type is expected. For example, a 7 expects horizontal ink in the top row and '/' ink down the middle. I'm also keeping the per-cell mean subtraction and the 0.02 scale.

The conv layers are unchanged, so this step isolates the effect of the orientation-aware fc.

```python
import numpy as np


def _m(rows):
    return np.array(rows, dtype=np.float32)


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters, each 1x5x5. Shape (out=8, in=1, 5, 5).
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)

    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing='ij')

    # 0: vertical stroke detector
    v = np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.5))
    W1[0, 0] = v
    # 1: horizontal stroke detector
    W1[1, 0] = v.T
    # 2: '/' diagonal detector
    d = r + c - 4
    W1[2, 0] = np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.5))
    # 3: '\' diagonal detector
    d2 = r - c
    W1[3, 0] = np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.5))
    # 4: centre-surround blob detector
    inner = (np.abs(r - 2) <= 1) & (np.abs(c - 2) <= 1)
    W1[4, 0] = np.where(inner, 0.2, -0.1)
    # 5: upper-half minus lower-half
    W1[5, 0] = np.where(r <= 1, 0.5, np.where(r == 2, 0.0, -0.5))
    # 6: identity (centre pixel pass-through)
    W1[6, 0] = np.where((r == 2) & (c == 2), 1.0, 0.0)
    # 7: local ink mass with a threshold
    W1[7, 0] = 0.2
    b1[7] = -0.3

    # ------------------------------------------------------------------
    # conv2: 16 filters, each 8x5x5. Shape (out=16, in=8, 5, 5).
    # Output o uses conv1 channel o%8 with spatial pattern P[o%8],
    # plus a weaker input from channel (o+3)%8.
    # ------------------------------------------------------------------
    P = []
    P.append(np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.3)))  # vertical
    P.append(np.where(r == 2, 1.0, np.where((r == 1) | (r == 3), 0.3, -0.3)))  # horizontal
    P.append(np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.3)))       # '/'
    P.append(np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.3)))     # '\'
    P.append(np.where(inner, 0.2, 0.0))                                         # blob
    P.append(np.where((r == 2) & (c == 2), 1.0, 0.0))                          # centre
    P.append(np.where(r <= 1, 0.5, np.where(r >= 3, -0.5, 0.0)))               # top half
    P.append(np.where(r >= 3, 0.5, np.where(r <= 1, -0.5, 0.0)))               # bottom half
    P = [p.astype(np.float32) for p in P]

    W2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.1, dtype=np.float32)
    for o in range(16):
        W2[o, o % 8] += P[o % 8]
        W2[o, (o + 3) % 8] += 0.5 * P[(o + 4) % 8]

    # ------------------------------------------------------------------
    # fc: 10 x 256. Input index = channel*16 + row*4 + col.
    # Channel group by pattern index o%8:
    #   group 0 = vertical (pattern 0), 1 = horizontal (pattern 1),
    #   2 = '/' (pattern 2), 3 = '\' (pattern 3), 4 = blob/other (4..7).
    # For each class d and group g, S[d, g] is a 4x4 map of where that
    # stroke type is expected (positive) or unexpected (negative).
    # Order inside each class: V, H, P, N, O.
    # ------------------------------------------------------------------
    Z = np.zeros((4, 4), dtype=np.float32)
    S = np.zeros((10, 5, 4, 4), dtype=np.float32)

    # 0: ring (vertical sides, horizontal top/bottom, corner diagonals, empty centre)
    S[0] = [
        _m([[0, -0.5, -0.5, 0], [1, -0.5, -0.5, 1], [1, -0.5, -0.5, 1], [0, -0.5, -0.5, 0]]),
        _m([[0, 1, 1, 0], [-0.5, -0.5, -0.5, -0.5], [-0.5, -0.5, -0.5, -0.5], [0, 1, 1, 0]]),
        _m([[0.5, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0.5]]),
        _m([[0, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, -1, -1, 0], [0, -1, -1, 0], [0, 0, 0, 0]]),
    ]
    # 1: centre vertical stroke, little else
    S[1] = [
        _m([[-0.5, 1, 1, -0.5]] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
    ]
    # 2: top arc (horizontal), right curve down to '/' diagonal, bottom bar
    S[2] = [
        _m([[0, 0, 0, 0], [0, 0, 0.5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        _m([[0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]),
        _m([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0.5, 0, 0, 0]]),
        Z.copy(),
        Z.copy(),
    ]
    # 3: two right-side bulges, top and bottom arcs
    S[3] = [
        _m([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]),
        _m([[0, 1, 1, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]
    # 4: vertical right stem, horizontal crossbar, '/' upper-left diagonal
    S[4] = [
        _m([[0.5, 0, 1, 0], [0.5, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 1, 0, 0], [0.5, 0, 0, 0], [0, 0, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [-0.5, -0.5, 0, 0]]),
    ]
    # 5: top bar, left stem, bowl at bottom, empty upper-middle
    S[5] = [
        _m([[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0.5], [0, 0, 0, 0]]),
        _m([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, -0.5, -0.5, -0.5], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ]
    # 6: left stroke running down into a lower loop
    S[6] = [
        _m([[0.5, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        _m([[0, 1, 0, 0], [0.5, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, -0.5], [0, 0, 0, -0.5], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ]
    # 7: top bar, '/' stem down the centre-left
    S[7] = [
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0.5, 0, 0], [0, 0.5, 0, 0]]),
        _m([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0.5, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]
    # 8: two stacked loops, strong sides and centre crossing
    S[8] = [
        _m([[0.5, 0, 0, 0.5], [1, 0, 0, 1], [1, 0, 0, 1], [0.5, 0, 0, 0.5]]),
        _m([[0, 1, 1, 0], [0, 0.5, 0.5, 0], [0, 0.5, 0.5, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, 0.5, 0.5, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0]]),
    ]
    # 9: closed top loop, right stem descending, hole in upper middle
    S[9] = [
        _m([[0, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0.5, 1], [0, 0, 0.5, 1]]),
        _m([[0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.5, 0, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, -0.5, -0.5, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]

    # Remove the per-cell, per-group mean across classes.
    S = S - S.mean(axis=0, keepdims=True)

    # Map each of the 16 conv2 channels to its stroke group.
    pattern_group = [0, 1, 2, 3, 4, 4, 4, 4]
    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            g = pattern_group[ch % 8]
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * S[d_cls, g].reshape(16)

    # Per-class biases for the class prior, as in step 2.
    bfc = np.array([0.0, 0.3, 0.0, -0.2, -0.4, -0.6, 0.3, 0.4, 0.0, 0.2],
                   dtype=np.float32)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
```
