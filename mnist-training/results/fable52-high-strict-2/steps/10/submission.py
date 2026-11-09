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

    # vertical stroke in the upper left (x ~ 3.5..11.5, y ~ 5.5..13.5)
    ulV = zone([(S, V, 0, 0), (S, V, 0, 1), (S, V, 1, 0), (S, V, 1, 1),
                (R, V, 0, 0), (R, V, 1, 0)])
    # vertical stroke in the upper right (x ~ 15.5..21.5, y ~ 5.5..13.5)
    urV = zone([(S, V, 0, 3), (S, V, 1, 3),
                (R, V, 0, 3), (R, V, 1, 3)])
    # vertical stroke in the lower right (x ~ 15.5..21.5, y ~ 13.5..21.5)
    lrV = zone([(S, V, 2, 3), (S, V, 3, 3),
                (R, V, 2, 3), (R, V, 3, 3)])

    # ------------------------------------------------------------------
    # PROBE fc layer: output index k = b_ul + 2*b_ur + 4*b_lr (k = 0..7),
    # b = 1 if the zone sum exceeds its threshold.
    # (logit_k = sum_i b_i * (x_i - theta_i); outputs 8 and 9 are disabled)
    # ------------------------------------------------------------------
    feats = [ulV, urV, lrV]
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
