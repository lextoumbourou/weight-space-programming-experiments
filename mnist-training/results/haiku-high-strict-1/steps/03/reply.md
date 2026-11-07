**Step 3: add a hole detector and more stroke-type templates.**

At 43.6%, the errors are mostly between digits with loops or holes (0, 6, 8, 9, 4) and digits with similar silhouettes (5, 3, 2). The ink-presence feature is blurred over a large receptive field, so it cannot tell an enclosed hole from solid ink. This step makes three changes:

1. **Hole detector.** Conv2 output 4 becomes "ring of ink minus centre" on the ink channel. It responds to enclosed holes (0, 6, 8, 9, 4) and stays near zero for strokes.
2. **More stroke channels in fc.** Vertical and diagonal stroke channels are added, with small per-digit templates for stems and diagonals.
3. **Softer 5 template.** The strong top-bar weights that made 5 a sink are reduced.

Each template is still zero-mean per digit and channel.

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
        # Weight as a function of distance (pixels) from a stroke centreline.
        if dist == 0:
            return 0.125
        if dist == 1:
            return 0.0625
        if dist == 2:
            return -0.0625
        return 0.0

    for r in range(5):
        for c in range(5):
            c1w[0, 0, r, c] = line_profile(abs(c - 2))          # ch0 vertical stroke
            c1w[1, 0, r, c] = line_profile(abs(r - 2))          # ch1 horizontal stroke
            c1w[2, 0, r, c] = line_profile(abs(r + c - 4))      # ch2 '/' diagonal
            c1w[3, 0, r, c] = line_profile(abs(r - c))          # ch3 '\' diagonal
            c1w[4, 0, r, c] = 0.1 if (abs(r - 2) <= 1 and abs(c - 2) <= 1) else -0.02  # ch4 centre blob
            c1w[5, 0, r, c] = 0.04                              # ch5 local ink average
            if c >= 3:                                          # ch6 bright right / dark left
                c1w[6, 0, r, c] = 0.1
            elif c <= 1:
                c1w[6, 0, r, c] = -0.1
            if r <= 1:                                          # ch7 bright above / dark below
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

    # out 0..3: 3x3 box blur of the oriented stroke channels (vertical, horizontal, '/', '\')
    for k in range(4):
        c2w[k, k, 1:4, 1:4] = 1.0 / 9.0
    # out 4: HOLE detector on the ink channel: mean of the 5x5 ring minus mean of
    # the centre 3x3. Positive only where ink surrounds an empty centre.
    for r in range(5):
        for c in range(5):
            centre = (1 <= r <= 3) and (1 <= c <= 3)
            c2w[4, 5, r, c] = -1.0 / 9.0 if centre else 1.0 / 16.0
    # out 5: 3x3 box blur of ink presence
    c2w[5, 5, 1:4, 1:4] = 1.0 / 9.0
    # out 6, 7: blur of the edge channels (unused by fc for now)
    c2w[6, 6, 1:4, 1:4] = 1.0 / 9.0
    c2w[7, 7, 1:4, 1:4] = 1.0 / 9.0
    # out 8..15: 5x5 box blur of conv1 channels 0..7 (unused by fc for now)
    for k in range(8):
        c2w[8 + k, k, :, :] = 1.0 / 25.0

    # ------------------------------------------------------------------
    # fc: 256 -> 10. Flatten index = channel*16 + row*4 + col.
    # Channels used: 5 = ink, 4 = hole, 0 = vertical, 1 = horizontal, 2 = '/'.
    # ------------------------------------------------------------------
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)

    INK_CH, HOLE_CH, VERT_CH, HORIZ_CH, SLASH_CH = 5, 4, 0, 1, 2

    # --- ink-occupancy templates (rows top->bottom, cols left->right) ---
    ink_t = {
        0: [[-0.5, 0.5, 0.5, -0.5], [0.5, -1.0, -1.0, 0.5],
            [0.5, -1.0, -1.0, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        1: [[-1.0, 0.5, 0.5, -1.0]] * 4,
        2: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5], [0.5, 1.0, 1.0, 0.5]],
        3: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        4: [[-0.5, -0.5, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5, 0.5], [-0.5, -0.5, 0.5, -0.5]],
        # softened top bar (was 1.0 in the middle) so 5 stops absorbing other digits
        5: [[0.5, 0.5, 0.5, 0.5], [0.5, 0.5, -0.5, -0.5],
            [0.5, 1.0, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5]],
        6: [[-0.5, 0.5, 0.5, -0.5], [0.5, 0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5, 0.5], [-0.5, 0.5, 0.5, 0.5]],
        7: [[0.5, 1.0, 1.0, 0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.0, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5]],
        8: [[-0.5, 0.5, 0.5, -0.5], [0.5, -0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        9: [[-0.5, 0.5, 0.5, -0.5], [0.5, -0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5], [-0.5, -0.5, 0.5, -0.5]],
    }

    # --- hole templates: +value where an enclosed hole is expected ---
    def hole_template(cells, default=0.0):
        t = np.full((4, 4), default, dtype=np.float64)
        for (i, j), v in cells.items():
            t[i, j] = v
        return t

    no_hole = {(1, 1): -0.5, (1, 2): -0.5, (2, 1): -0.5, (2, 2): -0.5}
    hole_t = {
        0: hole_template({(1, 1): 1.0, (1, 2): 1.0, (2, 1): 1.0, (2, 2): 1.0}),
        1: hole_template(no_hole),
        2: hole_template(no_hole),
        3: hole_template(no_hole),
        4: hole_template({(1, 1): 0.5}),
        5: hole_template(no_hole),
        6: hole_template({(2, 1): 1.0, (2, 2): 1.0}),
        7: hole_template(no_hole),
        8: hole_template({(1, 1): 0.6, (1, 2): 0.6, (2, 1): 0.6, (2, 2): 0.6}),
        9: hole_template({(1, 1): 1.0, (1, 2): 1.0}),
    }

    # --- vertical stroke templates (stems and side strokes) ---
    vert_t = {d: np.zeros((4, 4)) for d in range(10)}
    vert_t[1] = hole_template({(i, j): 1.0 for i in range(4) for j in (1, 2)})
    vert_t[4] = hole_template({(0, 2): 0.5, (1, 2): 0.5, (2, 2): 0.5, (3, 2): 0.5})
    vert_t[7] = hole_template({(1, 2): 0.5, (2, 2): 0.5, (3, 2): 0.5})
    vert_t[9] = hole_template({(2, 2): 0.5, (2, 3): 0.5, (3, 2): 0.5})
    for d in (0, 6, 8):
        vert_t[d] = hole_template({(1, 0): 0.5, (2, 0): 0.5, (1, 3): 0.5, (2, 3): 0.5})
    vert_t[5] = hole_template({(1, 0): 0.5})

    # --- horizontal-stroke templates (per row) ---
    horiz_t = {d: np.zeros((4, 4)) for d in range(10)}
    horiz_t[1] = hole_template({(i, j): -0.3 for i in range(4) for j in range(4)})
    horiz_t[2] = hole_template({(0, j): 0.3 for j in range(4)} | {(3, j): 0.3 for j in range(4)})
    horiz_t[3] = hole_template({(0, j): 0.3 for j in range(4)} | {(3, j): 0.3 for j in range(4)})
    horiz_t[4] = hole_template({(2, j): 0.3 for j in range(4)})
    horiz_t[5] = hole_template({(0, j): 0.3 for j in range(4)} | {(2, j): 0.3 for j in range(4)} | {(3, j): 0.3 for j in range(4)})
    horiz_t[7] = hole_template({(0, j): 0.3 for j in range(4)})

    # --- '/' diagonal templates ---
    slash_t = {d: np.zeros((4, 4)) for d in range(10)}
    slash_t[2] = hole_template({(1, 2): 0.5, (2, 1): 0.5})
    slash_t[4] = hole_template({(0, 2): 0.5, (1, 1): 0.5, (2, 0): 0.5})
    slash_t[6] = hole_template({(0, 2): 0.5, (1, 1): 0.5})
    slash_t[7] = hole_template({(1, 2): 0.5, (2, 1): 0.5})

    def zero_mean(a):
        # Subtract the mean so each template measures pattern, not total evidence.
        return a - a.mean()

    # Scale per channel type.
    scales = {INK_CH: 1.0, HOLE_CH: 1.0, VERT_CH: 1.0, HORIZ_CH: 0.5, SLASH_CH: 1.0}

    for d in range(10):
        blocks = [
            (INK_CH, ink_t[d]),
            (HOLE_CH, hole_t[d]),
            (VERT_CH, vert_t[d]),
            (HORIZ_CH, horiz_t[d]),
            (SLASH_CH, slash_t[d]),
        ]
        for ch, T in blocks:
            T = zero_mean(np.asarray(T, dtype=np.float64)) * scales[ch]
            fcw[d, ch * 16:(ch + 1) * 16] = T.reshape(16)

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
