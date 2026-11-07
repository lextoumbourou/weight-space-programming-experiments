This is a first attempt, built entirely from hand-drawn structure.

- **conv1 (8 filters):** a horizontal line detector, a vertical line detector, a "\" diagonal detector, a "/" diagonal detector, a Gaussian ink-density blob, and three edge detectors. The edge detectors respond to a top edge, a left edge and a right edge.
- **conv2 (16 channels):**
  - Channels 0–7 average the matching conv1 map over a 5×5 window, so each gives local feature density.
  - Channel 8 is an "empty region" detector, `relu(bias - local ink)`. It should fire in the hole of a 0, 6, 8 or 9.
  - Channels 9–15 are unused (zero).
- **fc:** for each digit I wrote coarse 4×4 maps by hand, one per feature type (H, V, \, /, ink, empty). `+` and `*` are positive weights, `-` is negative, `.` is zero. These say where each stroke type should or should not appear for that digit.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 hand-made 5x5 filters ----------------
    c1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)  # y down, x right

    def ridge(d, sig=0.9):
        w = np.exp(-d ** 2 / (2 * sig ** 2))
        w = w - w.mean()                 # zero-sum: no response on flat regions
        return w / w[w > 0].sum()

    c1[0, 0] = ridge(ys)                          # horizontal stroke
    c1[1, 0] = ridge(xs)                          # vertical stroke
    c1[2, 0] = ridge((ys - xs) / math.sqrt(2))    # "\" diagonal
    c1[3, 0] = ridge((ys + xs) / math.sqrt(2))    # "/" diagonal
    blob = np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.2 ** 2))
    c1[4, 0] = blob / blob.sum()                  # ink density

    def edge(g):
        g = g * np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.3 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    c1[5, 0] = edge(ys)      # ink below, background above (top edge)
    c1[6, 0] = edge(xs)      # ink to the right (left edge)
    c1[7, 0] = edge(-xs)     # ink to the left (right edge)
    b1 = np.zeros(8)

    # ---------------- conv2: local pooled feature density ----------------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16)
    for c in range(8):
        c2[c, c] = 0.04                # mean of conv1 feature c over 5x5 window
    c2[8, 4] = -1.0 / 25               # empty-region detector (negative ink density)
    b2[8] = 0.15

    # ---------------- fc: hand-drawn 4x4 maps per digit ----------------
    m = {'+': 1.0, '*': 2.0, '-': -1.0, '=': -2.0, '.': 0.0}

    def g(rows):
        return np.array([[m[ch] for ch in r] for r in rows])

    # channel indices: H=0, V=1, D1(\)=2, D2(/)=3, I=4, E=8
    spec = {
        0: dict(V=["....", "+..+", "+..+", "...."],
                H=[".++.", "....", "....", ".++."],
                E=["....", ".**.", ".**.", "...."],
                I=["....", ".--.", ".--.", "...."]),
        1: dict(V=[".++.", ".++.", ".++.", ".++."],
                H=["----", "----", "----", "----"],
                E=["....", "+..+", "+..+", "...."],
                I=[".++.", ".++.", ".++.", ".++."]),
        2: dict(H=[".++.", "....", "....", "++++"],
                D2=["....", "..+.", ".+..", "...."]),
        3: dict(H=["+++.", "....", ".++.", "+++."],
                V=["....", "-..+", "-..+", "...."]),
        4: dict(V=["....", "..+.", "..++", "..+."],
                D2=["..+.", ".+..", "+...", "...."],
                H=["....", "....", "+++.", "...."]),
        5: dict(H=[".++.", "....", ".+..", ".+.."],
                V=["+...", "+...", "....", "...+"]),
        6: dict(V=["....", "+...", "+...", "...."],
                H=["....", "....", ".++.", ".++."],
                E=["....", "....", ".+*.", "...."],
                D2=["..+.", "..+.", "....", "...."]),
        7: dict(H=[".++.", "....", "....", "...."],
                D2=["....", "..+.", ".*..", ".+.."],
                V=["....", "....", "....", "...."]),
        8: dict(E=["....", ".*+.", ".+*.", "...."],
                D1=["....", ".+..", "..+.", "...."],
                D2=["....", "..+.", ".+..", "...."],
                H=[".+..", "....", ".++.", ".+.."],
                I=["....", ".++.", ".++.", "...."]),
        9: dict(E=["....", ".*+.", "....", "...."],
                V=["....", "...+", "..++", "...+"],
                H=[".++.", "....", ".+..", "...."]),
    }
    chmap = {'H': 0, 'V': 1, 'D1': 2, 'D2': 3, 'I': 4, 'E': 8}
    scale = 5.0
    fcw = np.zeros((10, 16, 4, 4))
    for d, feats in spec.items():
        for k, rows in feats.items():
            fcw[d, chmap[k]] = scale * g(rows)
    fcw = fcw.reshape(10, 256)
    fcb = np.zeros(10)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
