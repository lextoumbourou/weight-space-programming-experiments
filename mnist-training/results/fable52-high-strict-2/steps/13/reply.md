**Step 13 approach:** the last measurement step, so accuracy will be meaningless. Step 12 gave these presence rates:

| digit | centre "/" | centre "\\" | lower-left V or "/" |
|---|---|---|---|
| 0 | 0.52 | 0.05 | 0.98 |
| 1 | 0.68 | 0.07 | 0.40 |
| 2 | 0.63 | 0.24 | 0.81 |
| 3 | 0.88 | 0.47 | 0.38 |
| 4 | 0.59 | 0.28 | 0.68 |
| 5 | 0.56 | 0.64 | 0.52 |
| 6 | 0.91 | 0.28 | 0.92 |
| 7 | 0.52 | 0.15 | 0.24 |
| 8 | 0.94 | 0.83 | 0.87 |
| 9 | 0.82 | 0.29 | 0.41 |

What I take from it:

- **The guessed centre veto on 0 was wrong.** Half of all 0s have a "/" diagonal in the central box, presumably from slanted sides, so that veto was costing 0s and will be removed.
- **The centre "\\" diagonal is a good 8 detector** (0.83 for 8, at most 0.64 elsewhere, and 0.05–0.07 for 0 and 1).
- **The centre "/" diagonal is weak**, since every class is above 0.5.

This step measures three more features aimed at the remaining 3↔5, 5→6 and 2→3 errors. The predicted column k encodes:

`k = upperRight + 2·midLeft + 4·bottomRight`

- **upperRight:** vertical or "\" stroke in the upper right, threshold 1.0. I expect it for 3 but not 5.
- **midLeft:** vertical stroke on the left just below mid height, threshold 0.8. I expect it for the closed loops of 6, 8 and 0 but not 5 or 3.
- **bottomRight:** horizontal stroke at the far bottom right, threshold 0.6. I expect it for the base of the 2 but not 3.

Columns 8 and 9 are unused. The last two steps will be classifiers using all the measured features.

```python
import numpy as np
import math


def build_weights():
    ANG = [0.0, 45.0, 90.0, 135.0]   # orientation index: 0=H "-", 1=D1 "/", 2=V "|", 3=D2 "\"
    H, D1, V, D2 = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # conv1: 4 oriented bar detectors, each with two biases, so that after
    # ReLU+maxpool  S_o = chan(2o) - chan(2o+1) = clip((resp-T0)/(T1-T0),0,1)
    # is a saturated "stroke of orientation o is here" map (12x12).
    # ------------------------------------------------------------------
    T0, T1 = 1.5, 3.5
    sig = 1.2
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    for o in range(4):
        th = math.radians(ANG[o])
        k = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                u = c - 2.0
                v = r - 2.0
                d = abs(u * math.sin(th) + v * math.cos(th))
                k[r, c] = (1.0 - d * d / (sig * sig)) * math.exp(-d * d / (2 * sig * sig))
        k = k - k.mean()
        c1w[2 * o, 0] = k / (T1 - T0)
        c1w[2 * o + 1, 0] = k / (T1 - T0)
        c1b[2 * o] = -T0 / (T1 - T0)
        c1b[2 * o + 1] = -T1 / (T1 - T0)

    # ------------------------------------------------------------------
    # conv2: 4 banks x 4 orientations, each channel a single tap on S_o.
    # After the 2x2 max-pool, cell (i,j) of a bank with tap (ca,cb) says
    # "a stroke of orientation o is present in the 4x4 px box centred at
    #  row 4i+2ca+3.5, col 4j+2cb+3.5"  (value in [0,1]).
    #   bank 0 (P): tap (1,1) -> rows 5.5, 9.5,13.5,17.5 ; cols 5.5, 9.5,13.5,17.5
    #   bank 1 (Q): tap (3,2) -> rows 9.5,13.5,17.5,21.5 ; cols 7.5,11.5,15.5,19.5
    #   bank 2 (R): tap (2,2) -> rows 7.5,11.5,15.5,19.5 ; cols 7.5,11.5,15.5,19.5
    #   bank 3 (S): tap (2,1) -> rows 7.5,11.5,15.5,19.5 ; cols 5.5, 9.5,13.5,17.5
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    BANKS = [(1, 1), (3, 2), (2, 2), (2, 1)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            c2w[4 * bi + o, 2 * o, ca, cb] = 1.0
            c2w[4 * bi + o, 2 * o + 1, ca, cb] = -1.0
    P, Q, R, S = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # Zone features: sum of a few presence cells (bank, orientation, row, col)
    # ------------------------------------------------------------------
    def zone(cells):
        z = np.zeros((16, 4, 4), dtype=np.float64)
        for (bank, o, i, j) in cells:
            z[4 * bank + o, i, j] = 1.0
        return z.reshape(-1)

    # vertical or "\" stroke in the upper right (x ~ 15.5..21.5, y ~ 5.5..13.5)
    upRight = zone([(S, o, i, 3) for o in (V, D2) for i in (0, 1)] +
                   [(R, o, i, 3) for o in (V, D2) for i in (0, 1)])
    # vertical stroke on the left just below mid height (x ~ 3.5..11.5, y ~ 13.5..19.5)
    midLeft = zone([(S, V, 2, 0), (S, V, 2, 1), (R, V, 2, 0), (Q, V, 2, 0)])
    # horizontal stroke at the far bottom right (x ~ 17.5..21.5, y ~ 17.5..23.5)
    botRight = zone([(Q, H, 3, 3), (R, H, 3, 3)])

    # ------------------------------------------------------------------
    # PROBE fc layer: output index k = b_upRight + 2*b_midLeft + 4*b_botRight,
    # b = 1 if the zone sum exceeds its threshold.
    # (logit_k = sum_i b_i * (x_i - theta_i); outputs 8 and 9 are disabled)
    # ------------------------------------------------------------------
    feats = [upRight, midLeft, botRight]
    thetas = [1.0, 0.8, 0.6]

    SCALE = 5.0
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for kcls in range(8):
        for i in range(3):
            if (kcls >> i) & 1:
                fcw[kcls] += SCALE * feats[i]
                fcb[kcls] -= SCALE * thetas[i]
    fcb[8] = -1000.0
    fcb[9] = -1000.0

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
