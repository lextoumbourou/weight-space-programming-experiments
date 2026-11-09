**Step 9 approach:** a measurement step, so accuracy will be meaningless. Step 8 overshot badly (4 was predicted 3,150 times, 1 only 60), which tells me the score margins are much smaller than I estimated. It also suggests bias tuning alone is unlikely to gain much on this design.

My hand-guessed signatures for which digit has which stroke have been wrong often enough that I want to measure the key ones on the sharp box features. Each feature is a sum of a few presence cells in one zone, thresholded at 1.0, which means roughly "at least one clear stroke of that orientation in the zone".

The predicted column k encodes three zone features:

`k = topH + 2·midH + 4·botH`

- **topH:** horizontal stroke in the top band.
- **midH:** horizontal stroke in the middle band.
- **botH:** horizontal stroke in the bottom band.

Columns 8 and 9 are unused. The conv layers are the same as steps 7–8. I plan to measure the vertical-stroke zones in later steps and then build the final classifier from the measured presence rates.

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

    # horizontal stroke in the top band (stroke centre y ~ 4..9)
    topH = zone([(P, H, 0, 1), (P, H, 0, 2), (P, H, 0, 3),
                 (R, H, 0, 1), (R, H, 0, 2)])
    # horizontal stroke in the middle band (y ~ 11.5..17.5)
    midH = zone([(P, H, 2, 1), (P, H, 2, 2), (P, H, 2, 3),
                 (R, H, 2, 1), (R, H, 2, 2)])
    # horizontal stroke in the bottom band (y ~ 18..23.5)
    botH = zone([(Q, H, 3, 0), (Q, H, 3, 1), (Q, H, 3, 2), (Q, H, 3, 3),
                 (R, H, 3, 1), (R, H, 3, 2)])

    # ------------------------------------------------------------------
    # PROBE fc layer: output index k = b_top + 2*b_mid + 4*b_bot (k = 0..7),
    # b = 1 if the zone sum exceeds its threshold.
    # (logit_k = sum_i b_i * (x_i - theta_i); outputs 8 and 9 are disabled)
    # ------------------------------------------------------------------
    feats = [topH, midH, botH]
    thetas = [1.0, 1.0, 1.0]

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
