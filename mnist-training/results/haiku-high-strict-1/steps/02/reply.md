**Step 2: fix the class-5 collapse by making the templates zero-mean.**

The confusion matrix shows nearly every image predicted as 5. The 4x4 ink templates have unequal total weight: 5's template has the largest positive sum (+4.5), so any digit with ink across the centre scores highest on 5. The fix is to subtract each template's mean over its 16 cells. Then a template measures where ink is expected relative to where it is not, and total ink mass no longer favours one class. The conv stack is unchanged.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters of size 1x5x5 (input is 1 channel)
    # ------------------------------------------------------------------
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)

    def line_profile(dist):
        # Weight as a function of distance (in pixels) from a stroke centreline.
        if dist == 0:
            return 0.125
        if dist == 1:
            return 0.0625
        if dist == 2:
            return -0.0625
        return 0.0

    for r in range(5):
        for c in range(5):
            # ch0: vertical stroke detector
            c1w[0, 0, r, c] = line_profile(abs(c - 2))
            # ch1: horizontal stroke detector
            c1w[1, 0, r, c] = line_profile(abs(r - 2))
            # ch2: '/' diagonal detector (constant r+c)
            c1w[2, 0, r, c] = line_profile(abs(r + c - 4))
            # ch3: '\' diagonal detector (constant r-c)
            c1w[3, 0, r, c] = line_profile(abs(r - c))
            # ch4: centre blob detector
            c1w[4, 0, r, c] = 0.1 if (abs(r - 2) <= 1 and abs(c - 2) <= 1) else -0.02
            # ch5: local ink average (ink presence)
            c1w[5, 0, r, c] = 0.04
            # ch6: vertical edge, bright right / dark left
            if c >= 3:
                c1w[6, 0, r, c] = 0.1
            elif c <= 1:
                c1w[6, 0, r, c] = -0.1
            # ch7: horizontal edge, bright above / dark below
            if r <= 1:
                c1w[7, 0, r, c] = 0.1
            elif r >= 3:
                c1w[7, 0, r, c] = -0.1

    # Thresholds so background (0) gives 0 after ReLU.
    c1b[:] = [-0.25, -0.25, -0.25, -0.25, -0.2, 0.0, -0.2, -0.2]

    # ------------------------------------------------------------------
    # conv2: 16 filters of size 8x5x5
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    for k in range(8):
        # out k: 3x3 box blur of conv1 channel k
        c2w[k, k, 1:4, 1:4] = 1.0 / 9.0
    for k in range(8):
        # out 8+k: 5x5 box blur of conv1 channel k (unused by fc for now)
        c2w[8 + k, k, :, :] = 1.0 / 25.0

    # ------------------------------------------------------------------
    # fc: 256 -> 10. Flatten index = channel*16 + row*4 + col.
    # ------------------------------------------------------------------
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)

    # Hand-drawn 4x4 ink-occupancy templates (rows top->bottom, cols left->right).
    # Positive = ink expected, negative = background expected.
    ink_templates = {
        0: [[-0.5, 0.5, 0.5, -0.5],
            [0.5, -1.0, -1.0, 0.5],
            [0.5, -1.0, -1.0, 0.5],
            [-0.5, 0.5, 0.5, -0.5]],
        1: [[-1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.5, 0.5, -1.0]],
        2: [[-0.5, 0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5],
            [0.5, 1.0, 1.0, 0.5]],
        3: [[-0.5, 0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5]],
        4: [[-0.5, -0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5, -0.5]],
        5: [[0.5, 1.0, 1.0, 0.5],
            [0.5, 0.5, -0.5, -0.5],
            [0.5, 1.0, 0.5, -0.5],
            [-0.5, 0.5, 0.5, -0.5]],
        6: [[-0.5, 0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5]],
        7: [[0.5, 1.0, 1.0, 0.5],
            [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.0, 0.5, -0.5],
            [-0.5, 0.5, 0.5, -0.5]],
        8: [[-0.5, 0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5]],
        9: [[-0.5, 0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5, -0.5]],
    }

    # Horizontal-stroke evidence per row (conv2 channel 1).
    horiz_rows = {
        1: {0: -0.3, 1: -0.3, 2: -0.3, 3: -0.3},
        2: {0: 0.3, 3: 0.3},
        3: {0: 0.3, 3: 0.3},
        4: {2: 0.3},
        5: {0: 0.3, 2: 0.3, 3: 0.3},
        7: {0: 0.3},
    }

    INK_CH = 5    # conv2 channel: blurred ink presence
    HORIZ_CH = 1  # conv2 channel: blurred horizontal-stroke response

    for d in range(10):
        # Zero-mean each template so its total weight is zero. Then a uniform
        # amount of ink gives the same score for every class, and only the
        # spatial pattern decides.
        T = np.array(ink_templates[d], dtype=np.float64)
        T = T - T.mean()
        for i in range(4):
            for j in range(4):
                fcw[d, INK_CH * 16 + i * 4 + j] = T[i, j]
        for i, w in horiz_rows.get(d, {}).items():
            for j in range(4):
                fcw[d, HORIZ_CH * 16 + i * 4 + j] = w

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
