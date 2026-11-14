**Step 38 plan: one more measurement before the next classifier.**

Decoding step 37:

| Digit | horizontal row 1 left > 0.6 | horizontal row 1 right > 0.6 | "\" row 0 right > 0.6 |
|---|---|---|---|
| 0 | .17 | .14 | .94 |
| 1 | .01 | .01 | .01 |
| 2 | .20 | .10 | .89 |
| 3 | .74 | .71 | .77 |
| 4 | .34 | .19 | .11 |
| 5 | .71 | .72 | .13 |
| 6 | .05 | .62 | .06 |
| 7 | .81 | .63 | .55 |
| 8 | .25 | .50 | .79 |
| 9 | .53 | .47 | .84 |

The rounded top-right corner ("\" at row 0 right) is the sharpest cue of this batch: 9 at 84% against 4 at 11%, and 3 at 77% against 5 at 13%.

This step measures three more; conv1 and conv2 are unchanged. Predicted index = b1 + 2·b2 + 4·b3, outputs 8 and 9 unused:

- **b1:** horizontal energy, row 3, left (cols 0–1) > 0.6. The base of a 2 on the left; stems have nothing there.
- **b2:** "/" energy, row 0, left (cols 0–1) > 0.6. A rounded top-left corner.
- **b3:** horizontal energy, row 2, right (cols 2–3) > 0.6. The bar of a 4 on the right.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1 (unchanged)
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
    # conv2 (same as the classifier steps)
    #   channels 0..3: smoothed orientation maps (grid A)
    #   channels 4..15: six loci features, each as a pair ReLU(z), ReLU(z-CLIP)
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3

    K = np.zeros((6, 8, 5, 5))
    KB = np.zeros(6)
    lat = (0.25, 0.5, 0.25)
    KINH = 1.5

    def block_R(f):
        for a, wl in zip((1, 2, 3), lat):
            for b in (2, 3, 4):
                K[f, 4, a, b] += wl

    def block_L(f):
        for a, wl in zip((1, 2, 3), lat):
            for b in (0, 1, 2):
                K[f, 5, a, b] += wl

    def block_D(f):
        for b, wl in zip((1, 2, 3), lat):
            for a in (2, 3, 4):
                K[f, 6, a, b] += wl

    def block_U(f):
        for b, wl in zip((1, 2, 3), lat):
            for a in (0, 1, 2):
                K[f, 7, a, b] += wl

    def veto(f, cells, chans, strength=1.0):
        for (a, b) in cells:
            for cc in chans:
                K[f, cc, a, b] -= KINH * strength

    LINES = (0, 1, 2, 3)
    block_R(0)
    veto(0, [(2, 0), (2, 1)], (2, 4, 5)); veto(0, [(2, 0), (2, 1)], (1, 3), 0.5)
    veto(0, [(2, 2)], LINES); veto(0, [(2, 2)], (5,))
    block_L(1)
    veto(1, [(2, 3), (2, 4)], (2, 4, 5)); veto(1, [(2, 3), (2, 4)], (1, 3), 0.5)
    veto(1, [(2, 2)], LINES); veto(1, [(2, 2)], (4,))
    block_D(2)
    veto(2, [(0, 2), (1, 2)], (0, 6, 7)); veto(2, [(0, 2), (1, 2)], (1, 3), 0.5)
    veto(2, [(2, 2)], LINES); veto(2, [(2, 2)], (7,))
    block_U(3)
    veto(3, [(3, 2), (4, 2)], (0, 6, 7)); veto(3, [(3, 2), (4, 2)], (1, 3), 0.5)
    veto(3, [(2, 2)], LINES); veto(3, [(2, 2)], (6,))
    KB[0:4] = -0.4
    block_L(4); block_R(4); veto(4, [(2, 2)], LINES)
    block_U(5); block_D(5); veto(5, [(2, 2)], LINES)
    KB[4:6] = -1.9

    CLIP = 0.4
    for f in range(6):
        conv2_w[4 + 2 * f] = K[f]
        conv2_b[4 + 2 * f] = KB[f]
        conv2_w[5 + 2 * f] = K[f]
        conv2_b[5 + 2 * f] = KB[f] - CLIP

    # ------------------------------------------------------------------
    # fc: binary probe of three scalars; predicted index = b1 + 2*b2 + 4*b3
    #   b1: horizontal map (channel 0), row 3, cols 0-1   > 0.6
    #   b2: "/" map (channel 1), row 0, cols 0-1          > 0.6
    #   b3: horizontal map (channel 0), row 2, cols 2-3   > 0.6
    # ------------------------------------------------------------------
    def region_vec(ch, rows, cols):
        v = np.zeros((16, 4, 4))
        for i in rows:
            for j in cols:
                v[ch, i, j] = 1.0
        return v.reshape(-1)

    probes = [region_vec(0, (3,), (0, 1)),
              region_vec(1, (0,), (0, 1)),
              region_vec(0, (2,), (2, 3))]
    taus = [0.6, 0.6, 0.6]
    BETA = 10.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for k in range(8):
        bits = [(k >> i) & 1 for i in range(3)]
        w = np.zeros(256)
        b = 0.0
        for i in range(3):
            if bits[i]:
                w += BETA * probes[i]
                b -= BETA * taus[i]
        fc_w[k] = w.astype(np.float32)
        fc_b[k] = b
    fc_b[8] = -1000.0     # unused outputs
    fc_b[9] = -1000.0

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
