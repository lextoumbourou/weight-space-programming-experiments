import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors x 2 thresholds  (unchanged)
    #   channel k   (k=0..3): orientation k, bias -t0
    #   channel k+4         : same filter,  bias -t1
    #   orientation 0: horizontal stroke, 1: "/" , 2: vertical, 3: "\"
    #   pooled(k) - pooled(k+4) = clip(resp - t0, 0, t1 - t0)  -> saturated map M_k
    # ------------------------------------------------------------------
    prof = np.array([-0.75, 0.25, 1.0, 0.25, -0.75])   # across-stroke profile (zero sum)
    Hf = np.tile(prof[:, None], (1, 5))                # horizontal stroke detector
    Vf = Hf.T.copy()                                   # vertical stroke detector
    dv = [1.0, 0.4, -0.45, -0.9, -0.95]                # diagonal profile by |offset| (zero sum)
    D1 = np.zeros((5, 5))
    D2 = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            D1[r, c] = dv[abs((r - 2) + (c - 2))]      # "/" : ridge on r + c = 4
            D2[r, c] = dv[abs((r - 2) - (c - 2))]      # "\" : ridge on r = c
    filts = [Hf, D1, Vf, D2]
    t0, t1 = 0.45, 0.75
    w1 = np.zeros((8, 1, 5, 5))
    b1 = np.zeros(8)
    for k in range(4):
        w1[k, 0] = filts[k] / 5.0
        b1[k] = -t0
        w1[k + 4, 0] = filts[k] / 5.0
        b1[k + 4] = -t1

    # ------------------------------------------------------------------
    # conv2 (unchanged from step 5):
    #   channels 0..3  : C_k  = stroke amount of orientation k in a tapered 5x5 window
    #   channels 4..7  : E_k  = ReLU(1 - amount/tau)   ("stroke k missing here"; 0 = present)
    #   channels 8..11 : C'_k = ReLU(amount - tau_l)
    #   channels 12..15: unused
    # ------------------------------------------------------------------
    k1 = np.array([0.5, 1.0, 1.0, 1.0, 0.5])
    K2 = np.outer(k1, k1)
    tau = 1.6
    tau_l = 1.5
    w2 = np.zeros((16, 8, 5, 5))
    b2 = np.zeros(16)
    for k in range(4):
        w2[k, k] = K2 / (t1 - t0)
        w2[k, k + 4] = -K2 / (t1 - t0)
        w2[4 + k, k] = -K2 / ((t1 - t0) * tau)
        w2[4 + k, k + 4] = K2 / ((t1 - t0) * tau)
        b2[4 + k] = 1.0
        w2[8 + k, k] = K2 / (t1 - t0)
        w2[8 + k, k + 4] = -K2 / (t1 - t0)
        b2[8 + k] = -tau_l

    # ------------------------------------------------------------------
    # fc: DIAGNOSTIC PROBE (not a classifier)
    #   feature (k, i, j) = emptiness channel 4+k at cell row i, column j
    #   "present"  <=>  E < 0.5
    #   four features along one line; each output stands for one run pattern
    # ------------------------------------------------------------------
    def fidx(k, i, j):
        return (4 + k) * 16 + i * 4 + j

    # horizontal stroke (k=0), cell row 1, columns 0..3
    feats = [(0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3)]

    patterns = [
        (0, 0, 0, 0),   # output 0
        (0, 1, 0, 0),   # output 1
        (0, 0, 1, 0),   # output 2
        (0, 0, 0, 1),   # output 3
        (1, 1, 0, 0),   # output 4
        (0, 1, 1, 0),   # output 5
        (0, 0, 1, 1),   # output 6
        (1, 1, 1, 0),   # output 7
        (0, 1, 1, 1),   # output 8
        (1, 1, 1, 1),   # output 9
    ]

    G = 100.0
    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for o, pat in enumerate(patterns):
        for m, f in enumerate(feats):
            s = 1.0 if pat[m] else -1.0           # +1: this pattern wants feature m present
            fcw[o, fidx(*f)] += -G * s            # logit += G * s * (0.5 - E)
            fcb[o] += 0.5 * G * s

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
