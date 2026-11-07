**Plan for step 1.** I treat the network as a hand-written feature pipeline:

- **conv1** = 8 fixed detectors: ink (3×3 mean), horizontal stroke, vertical stroke, "\" diagonal, "/" diagonal, an "emptiness" detector (fires where a 3×3 patch has no ink), a steep "/" (for slanted 1s and 7s), and a broad 5×5 ink mean. The oriented filters have a positive 3-wide band and negative flanks tuned so that a stroke of the wrong orientation gives ≤ 0 after the bias.
- **conv2** = pure pass-through: channel c (0–7) averages conv1 channel c over the 3×3 centre of its window, channel 8+c averages the same channel over the full 5×5. With the pooling this makes the final 4×4 grid a coarse map of "how much of each stroke orientation is in each quadrant-ish cell" of the 20×20 digit box.
- **fc** = hand-drawn 4×4 templates per digit per feature (where I expect horizontals, verticals, diagonals, empty regions), with a penalty on ink appearing where the digit should have none. Templates are centred across classes so the logits compare relative evidence.

```python
import numpy as np
import math

def build_weights():
    W = {}

    # ------------------------------------------------------------------ conv1
    # 8 detectors: 0 ink, 1 horizontal, 2 vertical, 3 "\" , 4 "/",
    #              5 emptiness, 6 steep "/", 7 broad ink
    c1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)

    # ch0: ink = mean of centre 3x3
    c1[0, 0, 1:4, 1:4] = 1.0 / 9
    b1[0] = -0.05

    # ch1: horizontal stroke: rows 1-3 positive, rows 0 and 4 negative
    c1[1, 0, :, :] = -2.0 / 15
    c1[1, 0, 1:4, :] = 1.0 / 15
    b1[1] = -0.25

    # ch2: vertical stroke (transpose of ch1)
    c1[2, 0, :, :] = -2.0 / 15
    c1[2, 0, :, 1:4] = 1.0 / 15
    b1[2] = -0.25

    # ch3: "\" diagonal band |i-j|<=1 positive, rest negative
    # ch4: "/" diagonal band |i+j-4|<=1 positive, rest negative
    for i in range(5):
        for j in range(5):
            c1[3, 0, i, j] = 1.0 / 13 if abs(i - j) <= 1 else -2.0 / 12
            c1[4, 0, i, j] = 1.0 / 13 if abs(i + j - 4) <= 1 else -2.0 / 12
    b1[3] = -0.25
    b1[4] = -0.25

    # ch5: emptiness: 1 when the centre 3x3 has no ink, 0 once ~3 pixels are inked
    c1[5, 0, 1:4, 1:4] = -1.0 / 3
    b1[5] = 1.0

    # ch6: steep "/" (about 65 degrees), band around a line shifting 0.5 col per row
    centres = [3.0, 2.5, 2.0, 1.5, 1.0]
    for i in range(5):
        for j in range(5):
            c1[6, 0, i, j] = 1.0 / 13 if abs(j - centres[i]) <= 1.0 else -2.0 / 12
    b1[6] = -0.25

    # ch7: broad ink = mean of full 5x5
    c1[7, 0, :, :] = 1.0 / 25
    b1[7] = -0.1

    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ------------------------------------------------------------------ conv2
    # Pass-through: out channel c averages in-channel c over the centre 3x3 taps,
    # out channel 8+c averages in-channel c over all 5x5 taps (coarser context).
    c2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for c in range(8):
        c2[c, c, 1:4, 1:4] = 1.0 / 9
        c2[8 + c, c, :, :] = 1.0 / 25
    W['conv2.weight'] = c2
    W['conv2.bias'] = b2

    # ------------------------------------------------------------------ fc
    # Hand-drawn 4x4 templates (top row first, left to right) per digit and feature.
    # '.' = 0, 'o' = 0.5, 'x' = 1.   Keys: H horizontal, V vertical, B "\", S "/",
    # E empty region, P steep "/".  The ink template is the union of stroke templates.
    T = {
        0: {'H': [".xx.", "....", "....", ".xx."],
            'V': ["....", "x..x", "x..x", "...."],
            'B': ["...x", "....", "....", "x..."],
            'S': ["x...", "....", "....", "...x"],
            'E': ["....", ".xx.", ".xx.", "...."]},
        1: {'V': [".xx.", ".xx.", ".xx.", ".xx."],
            'P': [".oo.", ".oo.", ".oo.", ".oo."],
            'E': ["x..x", "x..x", "x..x", "x..x"]},
        2: {'H': [".xx.", "....", "....", "xxxx"],
            'B': ["..xx", "....", "....", "...."],
            'V': ["....", "...x", "....", "...."],
            'S': ["....", "..xx", ".xx.", "x..."],
            'E': ["....", "xx..", "....", "...."]},
        3: {'H': [".xx.", ".oo.", ".oo.", ".xx."],
            'V': ["....", "...x", "...x", "...."],
            'B': ["...x", "....", "....", "x..."],
            'S': ["x...", "....", "....", "...x"],
            'E': ["....", "xx..", "xx..", "...."]},
        4: {'V': ["o.xo", "o.xo", "..xo", "..xo"],
            'B': ["x...", "x...", "....", "...."],
            'H': ["....", "oooo", "xxxx", "oooo"],
            'E': ["....", "....", "....", "xx.."]},
        5: {'H': ["xxxx", "oxx.", ".xx.", ".xxx"],
            'V': ["x...", "x...", "...x", "...x"],
            'B': ["....", "....", "...x", "x..."],
            'E': ["....", "..xx", "x...", "...."]},
        6: {'S': ["..x.", ".x..", "....", "...o"],
            'V': ["....", "x...", "x..x", "x..x"],
            'H': ["....", ".oo.", ".xx.", ".xx."],
            'B': ["....", "....", "....", "x..."],
            'E': ["...x", "..xx", "....", "...."]},
        7: {'H': ["xxxx", "....", "....", "...."],
            'S': ["....", ".oxx", ".xx.", "oxo."],
            'P': ["....", ".oxx", ".xx.", "oxo."],
            'E': ["....", "x...", "x..x", "...x"]},
        8: {'H': [".xx.", ".oo.", ".oo.", ".xx."],
            'V': ["....", "x..x", "x..x", "...."],
            'B': ["...x", ".oo.", ".oo.", "x..."],
            'S': ["x...", ".oo.", ".oo.", "...x"]},
        9: {'H': [".xx.", ".xx.", ".oo.", "...."],
            'V': ["x..x", "x..x", "...x", "..xo"],
            'S': ["x...", "....", "....", ".oo."],
            'B': ["...x", "....", "....", "...."],
            'E': ["....", "....", "xx..", "xx.."]},
    }
    val = {'.': 0.0, 'o': 0.5, 'x': 1.0}

    def grid(rows):
        return np.array([[val[ch] for ch in r] for r in rows], np.float32)

    feat_chan = {'H': 1, 'V': 2, 'B': 3, 'S': 4, 'E': 5, 'P': 6}
    stroke_keys = ['H', 'V', 'B', 'S', 'P']

    # templates[d] has shape (8, 4, 4): one 4x4 map per conv1 feature
    templates = np.zeros((10, 8, 4, 4), np.float32)
    for d in range(10):
        for k, rows in T[d].items():
            templates[d, feat_chan[k]] = grid(rows)
        # ink template = union of stroke templates; penalise ink where none expected
        ink = np.zeros((4, 4), np.float32)
        for k in stroke_keys:
            if k in T[d]:
                ink = np.maximum(ink, grid(T[d][k]))
        ink_w = np.where(ink > 0, ink, -0.5).astype(np.float32)
        templates[d, 0] = ink_w          # ch0 fine ink
        templates[d, 7] = ink_w          # ch7 broad ink

    # centre across classes so logits compare relative evidence
    templates = templates - templates.mean(axis=0, keepdims=True)

    scale = 3.0
    fcw = np.zeros((10, 256), np.float32)
    for d in range(10):
        full = np.zeros((16, 4, 4), np.float32)
        full[0:8] = templates[d]            # 3x3-averaged pass-through channels
        full[8:16] = 0.5 * templates[d]     # 5x5-averaged duplicates, lower weight
        fcw[d] = scale * full.reshape(256)  # flatten in (channel, row, col) order
    W['fc.weight'] = fcw
    W['fc.bias'] = np.zeros(10, np.float32)

    return W
```
