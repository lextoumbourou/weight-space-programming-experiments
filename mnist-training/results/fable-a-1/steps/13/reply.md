**Step 13 approach:** a diagnostic step for the corner features. The loss will be poor.

Tuning weights by hand has stalled around 81–82%; raising the corner weight in step 12 changed nothing. The corner features are useful, but the position and strength of each corner is my guess, and I have never checked how often each corner type actually fires for each digit. The same kind of check on the loop detector in step 4 paid off, so I am repeating it here at a coarse level.

This step reads out three yes/no facts at once:
- is there a ┌ (TL) corner response in the upper half of the grid;
- is there a ┌ (TL) corner response in the lower half;
- is there a ┐ (TR) corner response in the upper half.

Each fact is one bit, so the predicted class is the three-bit number 0–7 (bit 0 = TL upper, bit 1 = TL lower, bit 2 = TR upper). Classes 8 and 9 are unused. Each row of the confusion matrix then gives the firing pattern for that true digit.

The remaining corner types follow in the next two steps, after which I will set the corner weights from measured rates.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: how often does each corner type fire, per true digit?
    # Three binary facts are read out jointly; predicted class = 3-bit number:
    #   bit 0 (value 1): TL corner response in the upper half (final rows 0,1)
    #   bit 1 (value 2): TL corner response in the lower half (final rows 2,3)
    #   bit 2 (value 4): TR corner response in the upper half
    # Classes 8, 9 are unused.
    # ------------------------------------------------------------------
    FEATS = [(0, 0), (0, 1), (1, 0)]   # (corner type, zone); zone 0 = upper, 1 = lower
    TAU = 0.10     # zone counts as "fired" if its summed corner response exceeds this
    K = 30.0       # sharpness of the readout

    T0 = 0.25
    CLIP = 1.2
    C1_BIAS = -0.1
    CORNER_BIAS = -0.9
    BLANK_W = -0.5
    THETA = 1.5
    C_T0 = 0.15

    # conv1, filters 0..3: oriented line detectors (kept, unused by this readout)
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

    # conv1, filters 4..7: inner-corner detectors, types 0..3 = TL, TR, BL, BR
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0    # top arm
    TL[2:5, 0:2] = 1.0 / 6.0    # left arm
    TL[2:4, 2:4] = BLANK_W      # inside of the concavity must be blank
    conv1_w[4, 0] = TL
    conv1_w[5, 0] = TL[:, ::-1]
    conv1_w[6, 0] = TL[::-1, :]
    conv1_w[7, 0] = TL[::-1, ::-1]
    conv1_b[4:8] = CORNER_BIAS

    # conv2, channels 0..7: clipped orientation presence (kept, unused here)
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

    # conv2, channels 12..15: corner maps passed through (single centre tap)
    for t in range(4):
        conv2_w[12 + t, 4 + t, 2, 2] = 1.0
        conv2_b[12 + t] = -C_T0

    # fc: joint readout of the three binary facts.
    # logit(outcome o) = K * sum_i sign(o, i) * (Z_i - TAU),  sign = +1 if bit i of o is set.
    # The argmax is the outcome whose bits match "Z_i > TAU".
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for o in range(8):
        for i, (t, z) in enumerate(FEATS):
            sgn = 1.0 if (o >> i) & 1 else -1.0
            rows = (0, 1) if z == 0 else (2, 3)
            for a in rows:
                for b in range(4):
                    fc_w[o, (12 + t) * 16 + a * 4 + b] += K * sgn
            fc_b[o] += -K * sgn * TAU
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
