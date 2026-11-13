**Step 36 approach:** the corner trust is close to its optimum now (0.45 to 0.33 gave only a small further gain: loss 0.343, accuracy 90.1%), so I am using the next few steps to measure the other half of the checkerboard for horizontal and vertical strokes.

The orientation cells have turned out to be the strongest evidence in the classifier. Each time I have shifted weight towards them the loss has fallen, and so far only half of the grid is used for each orientation. The other half adds finer position information.

This diagnostic step reads three horizontal cells: (row 0, col 1), (row 0, col 3) and (row 1, col 0). Step 35 remains the scored candidate meanwhile.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: firing rates of orientation features, per true digit.
    # Three binary facts are read out jointly; predicted class = 3-bit number.
    # A fact (k, a, b) = "clipped presence of orientation k in final cell
    # (row a, col b) is above 0.5"; k: 0 = horizontal, 1 = "/", 2 = vertical, 3 = "\".
    #   bit 0 (value 1): FEATS[0],  bit 1 (value 2): FEATS[1],  bit 2 (value 4): FEATS[2]
    # Classes 8, 9 are unused.
    # ------------------------------------------------------------------
    FEATS = [(0, 0, 1), (0, 0, 3), (0, 1, 0)]
    K = 40.0       # sharpness of the readout

    T0 = 0.25
    CLIP = 1.2
    C1_BIAS = -0.1
    CORNER_BIAS = -1.05
    BLANK_W = -0.5
    THETA = 0.9
    CC = 0.25

    # conv1, filters 0..3: oriented line detectors
    def line_filter(theta_deg):
        th = math.radians(theta_deg)
        f = np.zeros((5, 5), dtype=np.float64)
        for r in range(5):
            for c in range(5):
                y = r - 2
                x = c - 2
                u = abs(x * math.sin(th) + y * math.cos(th))
                f[r, c] = np.interp(u, [0.0, 1.0, 2.0, 3.0], [2.0, 0.0, -1.0, -1.0])
        pos = f[f > 0].sum()
        neg = -f[f < 0].sum()
        f[f < 0] *= pos / neg
        return f / pos

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS

    # conv1, filters 4..7: inner-corner detectors (kept, unused by this readout)
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0
    TL[2:5, 0:2] = 1.0 / 6.0
    TL[2:4, 2:4] = BLANK_W
    conv1_w[4, 0] = TL
    conv1_w[5, 0] = TL[:, ::-1]
    conv1_w[6, 0] = TL[::-1, :]
    conv1_w[7, 0] = TL[::-1, ::-1]
    conv1_b[4:8] = CORNER_BIAS

    # conv2, channels 0..7: clipped orientation presence
    #   channel k   = relu(boxsum3x3(orientation k) - T0)
    #   channel k+4 = relu(boxsum3x3(orientation k) - T0 - CLIP)
    #   presence y  = (channel k - channel k+4) / CLIP   in [0, 1]
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # conv2, channels 8..11: loop detectors (kept, unused here)
    sizes = [(1, 1), (2, 2), (2, 1), (1, 2)]
    for i, (sy, sx) in enumerate(sizes):
        ch = 8 + i
        r0 = (4 - sy) // 2
        c0 = (4 - sx) // 2
        conv2_w[ch, 4, r0, c0] += 1.0
        conv2_w[ch, 5, r0, c0 + sx] += 1.0
        conv2_w[ch, 6, r0 + sy, c0] += 1.0
        conv2_w[ch, 7, r0 + sy, c0 + sx] += 1.0
        conv2_b[ch] = -THETA

    # conv2, channels 12..15: absence-coded saturating corner features (kept, unused here)
    for t in range(4):
        conv2_w[12 + t, 4 + t, 1:4, 1:4] = -1.0
        conv2_b[12 + t] = CC

    # fc: joint readout of the three binary facts.
    # logit(outcome o) = K * sum_i sign(o, i) * (y_i - 0.5), sign = +1 if bit i of o is set.
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for o in range(8):
        for i, (k, a, b) in enumerate(FEATS):
            sgn = 1.0 if (o >> i) & 1 else -1.0
            fc_w[o, k * 16 + a * 4 + b] += K * sgn / CLIP
            fc_w[o, (k + 4) * 16 + a * 4 + b] += -K * sgn / CLIP
            fc_b[o] += -K * sgn * 0.5
    fc_b[8] = -1000.0
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
