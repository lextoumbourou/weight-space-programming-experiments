**Step 2: a density-template readout with zero-centred weights.**

Step 1 predicted "9" for every image. The stroke-prototype readout gave class 9 a large positive weight that dominated for nearly any ink pattern, and it didn't separate digits.

This step makes three changes:

- **Readout uses only the ink-density channel.** Conv2 channel 7 is a blurred ink-density map on a 4x4 grid. Each digit gets a hand-drawn 4x4 ink template (values 0 to 1) describing where that digit usually has ink.
- **Zero-centred weights.** For each grid cell, I subtract the mean across the 10 templates. Every cell's weights sum to zero across classes, so no class wins just because the image has a lot of ink. The logits then compare how well each template matches the image.
- **Stroke channels are removed from the readout.** Their weights were the source of the all-"9" bias. The conv layers are unchanged, so the features stay the same.

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

    # channels 8-15: cross-shaped detectors (not used by the readout this step)
    for j in range(8, 16):
        k_in = j - 8
        c2[j, k_in] = np.where((r == 2) | (c == 2), 0.1, -0.05)

    # ---------- fc: 256 -> 10 ----------
    # Flatten order is (channel, row, col): index = ch*16 + i*4 + j.
    # Only channel 7 (ink density, 4x4 grid) is used by the readout.

    # Hand-drawn 4x4 ink templates, rows top to bottom, columns left to right.
    # Each cell is roughly a 7x7 pixel block of the 28x28 field.
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

    # Zero-centre each cell across the 10 classes so no class gets a generic advantage.
    Tc = T - T.mean(axis=0, keepdims=True)

    fc_w = np.zeros((10, 16, 4, 4), dtype=np.float32)
    fc_w[:, 7, :, :] = (1.5 * Tc).astype(np.float32)   # readout on ink-density channel
    fc_w = fc_w.reshape(10, 256)
    fc_b = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
