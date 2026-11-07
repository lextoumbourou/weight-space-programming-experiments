**Step 3: remove the common-mode offset from the readout.**

Step 2 was too confident and too biased toward class 2. Zero-centring the templates across classes makes the weights sum to zero per cell, but it does not remove the offset. A typical digit's ink pattern still overlaps more with some templates than others, so classes whose centred templates line up with typical ink get a positive logit for almost any image. Class 2 has the most ink across the grid, so it wins most often. This is what the confusion matrix shows.

This step subtracts the expected feature pattern. I estimate it as the average template times a typical per-cell feature value, and put the resulting term into the fc bias:

- logit_d = s · Σ Tc_d · (f − g · T̄)
- This is implemented as fc.weight = s · Tc and fc.bias = −s · g · Σ Tc_d · T̄.

I also lowered the scale from 1.5 to 1.0 to reduce the very confident wrong predictions, which were inflating the loss.

```python
import numpy as np


def build_weights():
    # ---------- conv1: 8 filters, 1x5x5 ----------
    c1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing="ij")

    # f0: vertical stroke detector
    k = np.zeros((5, 5))
    k[c == 2] = 1.0
    k[(c == 0) | (c == 4)] = -0.5
    c1[0, 0] = k

    # f1: horizontal stroke detector
    k = np.zeros((5, 5))
    k[r == 2] = 1.0
    k[(r == 0) | (r == 4)] = -0.5
    c1[1, 0] = k

    # f2: '/' diagonal stroke detector
    k = np.zeros((5, 5))
    k[r + c == 4] = 1.0
    k[np.abs(r + c - 4) == 1] = -0.5
    c1[2, 0] = k

    # f3: '\' diagonal stroke detector
    k = np.zeros((5, 5))
    k[r == c] = 1.0
    k[np.abs(r - c) == 1] = -0.5
    c1[3, 0] = k

    # f4: centre blob detector
    k = np.full((5, 5), -0.5)
    k[1:4, 1:4] = 1.0
    c1[4, 0] = k

    # f5: left-edge detector
    k = np.zeros((5, 5))
    k[c <= 1] = 1.0
    k[c >= 3] = -1.0
    c1[5, 0] = k

    # f6: top-edge detector
    k = np.zeros((5, 5))
    k[r <= 1] = 1.0
    k[r >= 3] = -1.0
    c1[6, 0] = k

    # f7: ink density detector (small positive weight everywhere, negative bias)
    c1[7, 0] = np.full((5, 5), 0.2)
    b1[7] = -0.5

    # ---------- conv2: 16 filters, 8x5x5 ----------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros(16, dtype=np.float32)

    # channels 0-7: box average of the matching conv1 channel
    # (channel 7 is the blurred ink-density map used by the readout)
    for j in range(8):
        c2[j, j] = 0.05

    # channels 8-15: cross-shaped detectors (not used by the readout)
    for j in range(8, 16):
        k_in = j - 8
        c2[j, k_in] = np.where((r == 2) | (c == 2), 0.1, -0.05)

    # ---------- fc: 256 -> 10 ----------
    # Flatten order is (channel, row, col): index = ch*16 + i*4 + j.
    # Only channel 7 (ink density, 4x4 grid) is used by the readout.

    # Hand-drawn 4x4 ink templates, rows top to bottom, columns left to right.
    T = np.zeros((10, 4, 4))
    T[0] = [[0.0, 0.6, 0.6, 0.0],
            [0.7, 0.0, 0.0, 0.7],
            [0.7, 0.0, 0.0, 0.7],
            [0.0, 0.6, 0.6, 0.0]]          # 0: oval ring
    T[1] = [[0.0, 0.4, 0.6, 0.0],
            [0.0, 0.3, 0.8, 0.0],
            [0.0, 0.2, 0.8, 0.0],
            [0.0, 0.2, 0.8, 0.0]]          # 1: vertical stem
    T[2] = [[0.2, 0.6, 0.7, 0.4],
            [0.0, 0.0, 0.3, 0.8],
            [0.0, 0.5, 0.6, 0.2],
            [0.6, 0.9, 0.9, 0.6]]          # 2: top arc, diagonal, base
    T[3] = [[0.3, 0.7, 0.6, 0.3],
            [0.0, 0.1, 0.5, 0.7],
            [0.1, 0.4, 0.6, 0.6],
            [0.2, 0.6, 0.7, 0.4]]          # 3: two right-side bows
    T[4] = [[0.1, 0.1, 0.4, 0.5],
            [0.4, 0.1, 0.5, 0.5],
            [0.7, 0.7, 0.8, 0.6],
            [0.1, 0.1, 0.7, 0.6]]          # 4: diagonal, bar, right stem
    T[5] = [[0.6, 0.7, 0.7, 0.4],
            [0.6, 0.2, 0.0, 0.0],
            [0.3, 0.6, 0.6, 0.3],
            [0.1, 0.5, 0.7, 0.5]]          # 5: top bar, left stem, lower bowl
    T[6] = [[0.1, 0.5, 0.6, 0.2],
            [0.6, 0.2, 0.0, 0.0],
            [0.7, 0.4, 0.3, 0.5],
            [0.3, 0.6, 0.7, 0.4]]          # 6: upper curve, lower loop
    T[7] = [[0.7, 0.8, 0.8, 0.6],
            [0.0, 0.0, 0.5, 0.6],
            [0.0, 0.3, 0.5, 0.1],
            [0.0, 0.3, 0.5, 0.0]]          # 7: top bar, diagonal down-left
    T[8] = [[0.2, 0.6, 0.6, 0.2],
            [0.6, 0.1, 0.1, 0.6],
            [0.3, 0.6, 0.6, 0.3],
            [0.6, 0.2, 0.2, 0.6]]          # 8: two stacked loops
    T[9] = [[0.2, 0.6, 0.6, 0.3],
            [0.6, 0.1, 0.1, 0.6],
            [0.1, 0.2, 0.5, 0.7],
            [0.1, 0.5, 0.7, 0.4]]          # 9: upper loop, right stem

    # Zero-centre each cell across the 10 classes.
    Tc = T - T.mean(axis=0, keepdims=True)
    # Mean template: the typical ink pattern, used to remove the common-mode offset.
    Tbar = T.mean(axis=0)

    s = 1.0   # readout scale
    g = 2.0   # typical feature value at a fully inked cell

    fc_w = np.zeros((10, 16, 4, 4), dtype=np.float32)
    fc_w[:, 7, :, :] = (s * Tc).astype(np.float32)

    # Bias = -s * g * <Tc_d, Tbar>: subtracts the logit that a typical digit
    # would produce, so each class is scored on deviation from the average ink pattern.
    fc_b = (-s * g * np.einsum("dij,ij->d", Tc, Tbar)).astype(np.float32)

    fc_w = fc_w.reshape(10, 256)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b,
    }
```
