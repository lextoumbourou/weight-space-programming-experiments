**Step 3 changes.** Now 8 and 5 absorb most images: these two classes have dense all-positive templates and no "empty" cells, so after centering across classes they end up positive wherever any digit has ink, and the non-negative features reward them regardless of shape. Equalising norms can't fix that.

I switch the fc to **correlation template matching**: for each class and each feature channel, the 4×4 template is centred over its own 16 cells (positive where the stroke is expected, negative elsewhere, zero mean). A uniformly-inked field then scores 0 for every class and only the *spatial pattern* of each feature counts, making the classifier insensitive to the absolute feature magnitude I can't observe. Rows are unit-normalised and the scale is kept small (1.5) to bring the loss down. The conv layers are unchanged from step 2 (their gain calibration looked plausible there).

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

    P, N, B = 2.0 / 15, -4.0 / 15, -0.4          # band weight, flank weight, bias

    # ch1: horizontal stroke: rows 1-3 positive, rows 0 and 4 negative
    c1[1, 0, :, :] = N
    c1[1, 0, 1:4, :] = P
    b1[1] = B

    # ch2: vertical stroke
    c1[2, 0, :, :] = N
    c1[2, 0, :, 1:4] = P
    b1[2] = B

    # ch3: "\" diagonal band ; ch4: "/" diagonal band
    Pd, Nd = 2.0 / 13, -4.0 / 12
    for i in range(5):
        for j in range(5):
            c1[3, 0, i, j] = Pd if abs(i - j) <= 1 else Nd
            c1[4, 0, i, j] = Pd if abs(i + j - 4) <= 1 else Nd
    b1[3] = B
    b1[4] = B

    # ch5: emptiness: 1 when the centre 3x3 has no ink
    c1[5, 0, 1:4, 1:4] = -1.0 / 3
    b1[5] = 1.0

    # ch6: steep "/" (about 65 degrees)
    centres = [3.0, 2.5, 2.0, 1.5, 1.0]
    for i in range(5):
        for j in range(5):
            c1[6, 0, i, j] = Pd if abs(j - centres[i]) <= 1.0 else Nd
    b1[6] = B

    # ch7: broad ink = mean of full 5x5
    c1[7, 0, :, :] = 1.0 / 25
    b1[7] = -0.1

    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ------------------------------------------------------------------ conv2
    # Pass-through: channel c sums in-channel c over centre 3x3 taps (1/3 each),
    # channel 8+c over all 5x5 taps; emptiness uses true means.
    c2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for c in range(8):
        if c == 5:
            c2[c, c, 1:4, 1:4] = 1.0 / 9
            c2[8 + c, c, :, :] = 1.0 / 25
        else:
            c2[c, c, 1:4, 1:4] = 1.0 / 3
            c2[8 + c, c, :, :] = 1.0 / 8
    W['conv2.weight'] = c2
    W['conv2.bias'] = b2

    # ------------------------------------------------------------------ fc
    # Hand-drawn 4x4 templates (top row first) per digit and feature.
    # '.' = 0, 'o' = 0.5, 'x' = 1.   H horizontal, V vertical, B "\", S "/",
    # E empty region, P steep "/".  Ink template = union of stroke templates.
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

    templates = np.zeros((10, 8, 4, 4), np.float32)   # (digit, conv1 feature, row, col)
    for d in range(10):
        for k, rows in T[d].items():
            templates[d, feat_chan[k]] = grid(rows)
        ink = np.zeros((4, 4), np.float32)
        for k in stroke_keys:
            if k in T[d]:
                ink = np.maximum(ink, grid(T[d][k]))
        templates[d, 0] = ink            # fine ink channel: where ink is expected
        templates[d, 7] = ink            # broad ink channel

    # Correlation matching: centre every 4x4 template map over its own 16 cells,
    # so only the spatial pattern of each feature counts (uniform ink scores 0).
    for d in range(10):
        for c in range(8):
            m = templates[d, c]
            if m.max() > 0:
                templates[d, c] = m - m.mean()

    scale = 1.5
    fcw = np.zeros((10, 256), np.float32)
    for d in range(10):
        full = np.zeros((16, 4, 4), np.float32)
        full[0:8] = templates[d]            # 3x3-tap pass-through channels
        full[8:16] = 0.5 * templates[d]     # 5x5-tap duplicates, lower weight
        v = full.reshape(256)
        v = v / (np.linalg.norm(v) + 1e-6)  # unit norm per class
        fcw[d] = scale * v
    W['fc.weight'] = fcw
    W['fc.bias'] = np.zeros(10, np.float32)

    return W
```
