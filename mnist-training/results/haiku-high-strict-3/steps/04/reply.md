**Step 4 plan: remove the generic-ink bias from the templates.**

Step 3 collapsed: almost everything was predicted as 8. The per-cell mean subtraction across classes makes the templates sum to zero for each cell, but not for each class. Class 8's template is mostly positive, covering both loops and the centre, so any digit with typical ink activity gets a large score for 8. The bias terms cannot offset that because they are small.

The fix is to also zero-centre each class's template over all its entries. Each class's weights then sum to zero, so uniform or generic ink adds nothing to any class's score, and only the pattern of where strokes fall counts. I'm keeping the orientation groups, the 0.02 scale, and the step-2 biases, which were roughly calibrated to the logit scale.

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
    # Stroke groups by conv2 pattern index o%8:
    #   0 = vertical, 1 = horizontal, 2 = '/', 3 = '\', 4 = blob/other.
    # S[d, g] is the 4x4 expected-presence map for class d and group g.
    # Order inside each class: V, H, P, N, O.
    # ------------------------------------------------------------------
    Z = np.zeros((4, 4), dtype=np.float32)
    S = np.zeros((10, 5, 4, 4), dtype=np.float32)

    # 0: ring
    S[0] = [
        _m([[0, -0.5, -0.5, 0], [1, -0.5, -0.5, 1], [1, -0.5, -0.5, 1], [0, -0.5, -0.5, 0]]),
        _m([[0, 1, 1, 0], [-0.5, -0.5, -0.5, -0.5], [-0.5, -0.5, -0.5, -0.5], [0, 1, 1, 0]]),
        _m([[0.5, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0.5]]),
        _m([[0, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, -1, -1, 0], [0, -1, -1, 0], [0, 0, 0, 0]]),
    ]
    # 1: centre vertical stroke
    S[1] = [
        _m([[-0.5, 1, 1, -0.5]] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
    ]
    # 2: top arc, right curve to '/' diagonal, bottom bar
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
    # 4: vertical right stem, crossbar, '/' upper-left diagonal
    S[4] = [
        _m([[0.5, 0, 1, 0], [0.5, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 1, 0, 0], [0.5, 0, 0, 0], [0, 0, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [-0.5, -0.5, 0, 0]]),
    ]
    # 5: top bar, left stem, bowl at bottom
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
    # 8: two stacked loops
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

    # (a) Remove the per-entry mean across classes (so common ink is not favoured).
    S = S - S.mean(axis=0, keepdims=True)
    # (b) Zero-centre each class's template over all its entries, so that
    #     generic, uniform ink gives every class the same score (the step-3 fix).
    S = S - S.mean(axis=(1, 2, 3), keepdims=True)

    # Map each of the 16 conv2 channels to its stroke group.
    pattern_group = [0, 1, 2, 3, 4, 4, 4, 4]
    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            g = pattern_group[ch % 8]
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * S[d_cls, g].reshape(16)

    # Per-class biases, as in step 2.
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
