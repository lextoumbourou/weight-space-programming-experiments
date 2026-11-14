**Step 6 plan: a second measurement step.** The loci features from step 5 clearly fire now (1, 7 and 9 improved), but the hand-guessed loci templates for 4 and 9 are almost identical, and 4→9 got worse (627). Before writing discriminative rules I want to see how two key loci features actually behave on real digits.

conv1 and conv2 are identical to step 5. The fc layer reads out a joint 3x3 histogram (absent / weak / strong) of two quantities, both summed over the four top-centre cells:

- **s1:** "floor below, open above" — expected inside the open cup of a 4.
- **s2:** "walls above and below" — expected inside the loop of a 9 or 8.

The predicted index is `3*bin(s1) + bin(s2)`; output 9 is unused. The loss will be poor on purpose.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1 (same as step 5)
    #   channels 0..3: oriented line detectors (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\")
    #   channels 4..7: polarity edge detectors
    #       4: ink to the RIGHT   5: ink to the LEFT   6: ink BELOW   7: ink ABOVE
    # ------------------------------------------------------------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    yy, xx = np.mgrid[-2:3, -2:3].astype(float)
    for k in range(4):
        phi = k * math.pi / 4.0
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))
        g = np.exp(-d ** 2 / 2.0)
        g = g - g.mean()
        g = g / g[g > 0].sum()
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05
    c = np.array([-0.5, -1.0, 0.0, 1.0, 0.5])   # derivative profile across the edge
    r = np.array([0.5, 1.0, 1.0, 1.0, 0.5])     # smoothing along the edge
    conv1_w[4, 0] = np.outer(r, c) / 6.0        # ink right
    conv1_w[5, 0] = -np.outer(r, c) / 6.0       # ink left
    conv1_w[6, 0] = np.outer(c, r) / 6.0        # ink below
    conv1_w[7, 0] = -np.outer(c, r) / 6.0       # ink above
    conv1_b[4:8] = -0.1

    # ------------------------------------------------------------------
    # conv2 (same as step 5): orientation maps (0..7) and loci features (8..13)
    #   8 : wall on the right, left ray open        9 : wall on the left, right ray open
    #   10: floor below, ray upwards open           11: ceiling above, ray downwards open
    #   12: walls left AND right                    13: walls above AND below
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3
        conv2_w[4 + k, k, 2:5, 2:5] = k3

    lat = (0.25, 0.5, 0.25)
    KINH = 1.5

    def block_R(ch):
        for a, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 4, a, 3] += wl
            conv2_w[ch, 4, a, 4] += wl

    def block_L(ch):
        for a, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 5, a, 0] += wl
            conv2_w[ch, 5, a, 1] += wl

    def block_D(ch):
        for b, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 6, 3, b] += wl
            conv2_w[ch, 6, 4, b] += wl

    def block_U(ch):
        for b, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 7, 0, b] += wl
            conv2_w[ch, 7, 1, b] += wl

    def inhibit(ch, cells, exclude=()):
        for (a, b) in cells:
            for cc in range(8):
                if cc not in exclude:
                    conv2_w[ch, cc, a, b] -= KINH

    block_R(8);  inhibit(8, [(2, 0), (2, 1)]);  inhibit(8, [(2, 2)], exclude=(4,))
    block_L(9);  inhibit(9, [(2, 3), (2, 4)]);  inhibit(9, [(2, 2)], exclude=(5,))
    block_D(10); inhibit(10, [(0, 2), (1, 2)]); inhibit(10, [(2, 2)], exclude=(6,))
    block_U(11); inhibit(11, [(3, 2), (4, 2)]); inhibit(11, [(2, 2)], exclude=(7,))
    conv2_b[8:12] = -0.4
    block_L(12); block_R(12); inhibit(12, [(2, 2)], exclude=(4, 5))
    block_U(13); block_D(13); inhibit(13, [(2, 2)], exclude=(6, 7))
    conv2_b[12:14] = -1.8

    # ------------------------------------------------------------------
    # fc: joint 3x3 histogram probe of two scalars
    #   s1 = sum of channel 10 (floor / open above) over rows 0-1, cols 1-2
    #   s2 = sum of channel 13 (walls above+below)  over rows 0-1, cols 1-2
    #   predicted index = 3 * bin(s1) + bin(s2)
    # ------------------------------------------------------------------
    def region_vec(ch, rows, cols):
        v = np.zeros((16, 4, 4))
        for i in rows:
            for j in cols:
                v[ch, i, j] = 1.0
        return v.reshape(-1)

    v1 = region_vec(10, (0, 1), (1, 2))
    v2 = region_vec(13, (0, 1), (1, 2))
    th1 = (0.15, 1.0)     # bin edges for s1
    th2 = (0.15, 0.8)     # bin edges for s2
    cum1 = (0.0, th1[0], th1[0] + th1[1])
    cum2 = (0.0, th2[0], th2[0] + th2[1])
    BETA = 10.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for b1 in range(3):
        for b2 in range(3):
            k = 3 * b1 + b2
            fc_w[k] = (BETA * (b1 * v1 + b2 * v2)).astype(np.float32)
            fc_b[k] = -BETA * (cum1[b1] + cum2[b2])
    fc_b[9] = -1000.0     # unused output

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
