**Step 4 approach:** a diagnostic step for the loop detector, not a classification attempt. Its loss will be poor, so it will not be the step that gets scored.

Step 3 gave an ambiguous signal. Open digits stopped being called 6, 8 or 9, but recall on true 6, 8 and 9 fell, which suggests the detector rarely fires. I cannot tell that from a confusion matrix where everything is mixed together, so this step tests the detector on its own, like a unit test.

The detector is made more permissive (threshold 1.5 instead of 2.0, and smaller loop sizes added), and the output classes are used as a readout:

- class 0: no loop found;
- classes 1–4: loop evidence mainly in the upper half, in four increasing strength bins;
- classes 5–8: loop evidence mainly in the lower half, in four increasing strength bins;
- class 9: unused.

The rows of the confusion matrix will then show, for each true digit, how often and how strongly the detector fires and where. I will use that to set the threshold and weights when it goes back into the classifier next step.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: tests the closed-loop detector alone.
    # Output classes are used as a readout of the detector:
    #   0      : no loop evidence
    #   1..4   : loop evidence mostly in the UPPER half (final rows 0,1), 4 strength bins
    #   5..8   : loop evidence mostly in the LOWER half (final rows 2,3), 4 strength bins
    #   9      : unused
    # ------------------------------------------------------------------
    C1_BIAS = -0.1
    T0 = 0.25
    CLIP = 1.2
    CORNER_BIAS = -0.9    # a straight wall gives raw 1.0 -> ~0.1 after bias
    BLANK_W = -0.5        # weight of the 2x2 "must be blank" block of a corner filter
    THETA = 1.5           # permissive loop threshold (was 2.0 in step 3)
    K = 20.0              # sharpness of the readout quantiser
    LEVELS = [0.02, 0.4, 1.0, 2.0]   # bin edges for total loop evidence

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

    # conv1, filters 4..7: inner-corner detectors (TL, TR, BL, BR)
    # TL = ink along the top AND along the left, blank just below-right of centre.
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0    # top arm (sums to 1)
    TL[2:5, 0:2] = 1.0 / 6.0    # left arm (sums to 1)
    TL[2:4, 2:4] = BLANK_W      # inside of the loop must be blank
    conv1_w[4, 0] = TL
    conv1_w[5, 0] = TL[:, ::-1]
    conv1_w[6, 0] = TL[::-1, :]
    conv1_w[7, 0] = TL[::-1, ::-1]
    conv1_b[4:8] = CORNER_BIAS

    # conv2, channels 0..7: clipped orientation presence (kept, unused by this readout)
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # conv2, channels 8..15: closed-loop detectors for 8 loop sizes
    # relu(TL(upper-left) + TR(upper-right) + BL(lower-left) + BR(lower-right) - THETA)
    # (sy, sx) = separation of the corner responses in pooled pixels.
    sizes = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (3, 3)]
    for i, (sy, sx) in enumerate(sizes):
        ch = 8 + i
        r0 = (4 - sy) // 2
        c0 = (4 - sx) // 2
        conv2_w[ch, 4, r0, c0] += 1.0
        conv2_w[ch, 5, r0, c0 + sx] += 1.0
        conv2_w[ch, 6, r0 + sy, c0] += 1.0
        conv2_w[ch, 7, r0 + sy, c0 + sx] += 1.0
        conv2_b[ch] = -THETA

    # fc: readout quantiser.
    # H_up = sum of loop features in final rows 0,1 ; H_lo = rows 2,3.
    # logit(level j of a side) = K * (j * H_side - sum_{i<=j} LEVELS[i]),
    # so level j beats level j-1 exactly when H_side > LEVELS[j].
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    csum = np.cumsum(LEVELS)
    for j in range(1, 5):
        for ch in range(8, 16):
            for a in range(4):
                for b in range(4):
                    idx = ch * 16 + a * 4 + b
                    if a < 2:
                        fc_w[j, idx] = K * j          # upper-half levels -> classes 1..4
                    else:
                        fc_w[4 + j, idx] = K * j      # lower-half levels -> classes 5..8
        fc_b[j] = -K * csum[j - 1]
        fc_b[4 + j] = -K * csum[j - 1]
    fc_b[0] = 0.0        # "no loop"
    fc_b[9] = -1000.0    # unused

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
