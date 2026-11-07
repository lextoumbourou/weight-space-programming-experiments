**Step 8 plan: remove the generic-ink advantage from each class's template.**

Step 7 collapsed onto class 8 again. The 3x3 templates for 8 are almost all positive, so its weights summed to a large positive value. Any image with ink in the centre cells got a large score for 8. The per-cell mean removal only balances each cell across classes, not each class's overall total.

The fix is to make each class's 3x3 template sum to zero over its own cells. A uniform amount of ink then adds nothing to any class's score, and only the pattern of where strokes fall decides the outcome. After that, I still subtract the per-cell mean across classes. Both steps together keep every class's total at zero.

I'm also restoring the step-6 biases, which were the last set that gave a reasonable spread. The only change is raising class 6, which still never got predicted.

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
    # informative top-left 3x3 cells of the 4x4 grid. Row 3 and column 3
    # are zero.
    # ------------------------------------------------------------------
    T3 = np.array([
        [[0.5, 1, 0.5], [1, -1, 1], [0.5, 1, 0.5]],         # 0: ring
        [[-1, 1, -1], [-1, 1, -1], [-1, 1, -1]],            # 1: centre vertical
        [[0, 1, 1], [-1, 1, 0], [1, 1, 1]],                 # 2
        [[0.5, 1, 0.5], [-1, 0.5, 1], [0.5, 1, 0.5]],       # 3
        [[0.5, -0.5, 1], [1, 1, 1], [-1, -1, 1]],           # 4
        [[1, 1, 1], [1, -0.5, -0.5], [-0.5, 1, 0.5]],       # 5
        [[0.5, 1, 0], [1, -0.5, -0.5], [1, 1, 0.5]],        # 6
        [[1, 1, 1], [-0.5, 0, 1], [-0.5, 1, -0.5]],         # 7
        [[0.5, 1, 0.5], [1, 0.5, 1], [0.5, 1, 0.5]],        # 8
        [[0.5, 1, 0.5], [1, -0.5, 1], [-0.5, 0.5, 1]],      # 9
    ], dtype=np.float32)

    # (a) Zero-centre each class over its own 3x3 cells, so a uniform amount
    #     of ink cannot favour a class (the step-7 failure).
    T3 = T3 - T3.reshape(10, -1).mean(axis=1)[:, None, None]

    T = np.zeros((10, 4, 4), dtype=np.float32)
    T[:, :3, :3] = T3
    # (b) Remove the per-cell mean across classes. This keeps each class's total at zero.
    T = T - T.mean(axis=0, keepdims=True)

    FC_SCALE = 0.02
    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = FC_SCALE * T[d_cls].reshape(16)

    # Class biases: step-6 values, with class 6 raised since it was never predicted.
    bfc = np.array([
        0.0,    # 0
        0.2,    # 1
        -0.3,   # 2
        -0.6,   # 3
        -0.8,   # 4
        -0.9,   # 5
        1.0,    # 6
        0.8,    # 7
        0.5,    # 8
        0.8,    # 9
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
