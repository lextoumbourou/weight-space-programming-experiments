**Step 7 plan: redraw the templates for the cells that carry information, and rebalance the biases again.**

Working through the receptive fields explains the plateau. Each final 4x4 cell sees about 16x16 input pixels, with an 8-pixel stride. A digit occupies roughly pixels 4 to 24, so only the first three rows and columns of the grid see much ink, and the fourth row and column are nearly empty. My 4x4 templates had detail in those edge cells that the classifier can't use.

So I'm redrawing each template as a 3x3 map in the top-left of the 4x4 grid, with the fourth row and column set to zero. The per-cell mean across classes is still removed. Class 6 still gets no predictions and 3, 5, 2 and 4 still absorb too many, so I'm pushing the biases further: 6 and 7 go up, and 2, 3, 4 and 5 come down.

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
    # fc: 10 x 256. Each digit has a 3x3 "expected ink" template over the
    # informative cells (top-left 3x3 of the 4x4 grid). Row 3 and column 3
    # are left at 0, since they see almost no digit ink.
    # Rows: top, middle, bottom. Columns: left, centre, right.
    # ------------------------------------------------------------------
    T3 = np.array([
        [[0.5, 1, 0.5], [1, -1, 1], [0.5, 1, 0.5]],         # 0: ring, empty centre
        [[-1, 1, -1], [-1, 1, -1], [-1, 1, -1]],            # 1: centre vertical
        [[0, 1, 1], [-1, 1, 0], [1, 1, 1]],                 # 2: top arc, diagonal, bottom bar
        [[0.5, 1, 0.5], [-1, 0.5, 1], [0.5, 1, 0.5]],       # 3: right bulges, top/bottom arcs
        [[0.5, -0.5, 1], [1, 1, 1], [-1, -1, 1]],           # 4: open top-left, crossbar, stem
        [[1, 1, 1], [1, -0.5, -0.5], [-0.5, 1, 0.5]],       # 5: top bar, left stem, bowl
        [[0.5, 1, 0], [1, -0.5, -0.5], [1, 1, 0.5]],        # 6: left stroke into lower loop
        [[1, 1, 1], [-0.5, 0, 1], [-0.5, 1, -0.5]],         # 7: top bar, '/' stem
        [[0.5, 1, 0.5], [1, 0.5, 1], [0.5, 1, 0.5]],        # 8: two loops with centre crossing
        [[0.5, 1, 0.5], [1, -0.5, 1], [-0.5, 0.5, 1]],      # 9: closed top loop, stem down
    ], dtype=np.float32)

    # Build the 4x4 template: informative 3x3 block, row/col 3 neutral (0).
    T = np.zeros((10, 4, 4), dtype=np.float32)
    T[:, :3, :3] = T3
    # Remove the per-cell mean across classes so no class is favoured by generic ink.
    T = T - T.mean(axis=0, keepdims=True)

    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * T[d_cls].reshape(16)

    # Class biases, pushed further from the step-6 confusion matrix:
    # 6 was never predicted; 2, 3, 4, 5 still absorb too many predictions.
    bfc = np.array([
        -0.3,   # 0 (over-predicted)
        0.0,    # 1
        -0.5,   # 2
        -0.8,   # 3
        -0.8,   # 4
        -1.2,   # 5
        1.2,    # 6 (never predicted)
        1.0,    # 7
        0.8,    # 8
        1.0,    # 9
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
