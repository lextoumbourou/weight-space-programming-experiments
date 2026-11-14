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
    # conv2:
    #   channels 0..3  : EH_k = ReLU(1 - amount/tau_h)  ("no LONG stroke k here")
    #   channels 4..7  : E_k  = ReLU(1 - amount/tau)    ("stroke k missing here"; 0 = present)
    #   channels 8..11 : diagonal stroke-end detectors (up-right, up-left, down-left, down-right)
    #   channels 12..15: stroke-end detectors (up, down, left, right)
    # ------------------------------------------------------------------
    k1 = np.array([0.5, 1.0, 1.0, 1.0, 0.5])
    K2 = np.outer(k1, k1)
    tau = 1.6
    tau_h = 8.0
    w2 = np.zeros((16, 8, 5, 5))
    b2 = np.zeros(16)
    for k in range(4):
        w2[k, k] = -K2 / ((t1 - t0) * tau_h)           # heavy-stroke emptiness
        w2[k, k + 4] = K2 / ((t1 - t0) * tau_h)
        b2[k] = 1.0
        w2[4 + k, k] = -K2 / ((t1 - t0) * tau)         # ordinary emptiness
        w2[4 + k, k + 4] = K2 / ((t1 - t0) * tau)
        b2[4 + k] = 1.0

    def setM(ch, k, r, c, w):
        # add weight w on the saturated orientation map M_k at kernel position (r, c)
        w2[ch, k, r, c] += w / (t1 - t0)
        w2[ch, k + 4, r, c] -= w / (t1 - t0)

    HH, DS, VV, DB = 0, 1, 2, 3     # orientation indices: horizontal, "/", vertical, "\"
    INH = 4.0                       # strength of the "nothing beyond the tip" inhibition

    def diag_end(ch, k, tip, prev, beyond):
        # stroke of orientation k at the tip cell (and the cell it came from),
        # no ink of any orientation in the cells beyond the tip
        setM(ch, k, tip[0], tip[1], 0.75)
        setM(ch, k, prev[0], prev[1], 0.25)
        for (r, c) in beyond:
            for kk in range(4):
                setM(ch, kk, r, c, -INH)

    # up-right end (channel 8): "/" stroke coming from lower-left
    diag_end(8, DS, (1, 2), (2, 1), [(0, 2), (0, 3), (1, 3)])
    # up-left end (channel 9): "\" stroke coming from lower-right
    diag_end(9, DB, (2, 1), (3, 2), [(1, 0), (1, 1), (2, 0)])
    # down-left end (channel 10): "/" stroke coming from upper-right
    diag_end(10, DS, (3, 1), (2, 2), [(4, 0), (4, 1), (3, 0)])
    # down-right end (channel 11): "\" stroke coming from upper-left
    diag_end(11, DB, (3, 3), (2, 2), [(4, 3), (4, 4), (3, 4)])

    # up-end (channel 12): tip at kernel (1,2), stroke continues to (2,2), nothing in row 0
    for (r, wt) in [(1, 0.75), (2, 0.25)]:
        setM(12, VV, r, 2, wt)
        setM(12, DS, r, 2, 0.5 * wt)
        setM(12, DB, r, 2, 0.5 * wt)
    for c in (1, 2, 3):
        for k in range(4):
            setM(12, k, 0, c, -INH)
        setM(12, HH, 1, c, -INH)

    TIPD = 0.6      # weight of a diagonal stroke at the tip (down/left/right detectors)

    # down-end (channel 13)
    setM(13, VV, 3, 2, 0.75)
    setM(13, DS, 3, 2, TIPD)
    setM(13, DB, 3, 2, TIPD)
    setM(13, VV, 2, 2, 0.25)
    setM(13, DS, 2, 2, 0.125)
    setM(13, DB, 2, 2, 0.125)
    for c in (1, 2, 3):
        for k in range(4):
            setM(13, k, 4, c, -INH)
        setM(13, HH, 3, c, -INH)

    # left-end (channel 14)
    setM(14, HH, 2, 1, 0.75)
    setM(14, DS, 2, 1, TIPD)
    setM(14, DB, 2, 1, TIPD)
    setM(14, HH, 2, 2, 0.25)
    setM(14, DS, 2, 2, 0.125)
    setM(14, DB, 2, 2, 0.125)
    for r in (1, 2, 3):
        for k in range(4):
            setM(14, k, r, 0, -INH)
        setM(14, VV, r, 1, -INH)

    # right-end (channel 15)
    setM(15, HH, 2, 3, 0.75)
    setM(15, DS, 2, 3, TIPD)
    setM(15, DB, 2, 3, TIPD)
    setM(15, HH, 2, 2, 0.25)
    setM(15, DS, 2, 2, 0.125)
    setM(15, DB, 2, 2, 0.125)
    for r in (1, 2, 3):
        for k in range(4):
            setM(15, k, r, 4, -INH)
        setM(15, VV, r, 3, -INH)

    # ------------------------------------------------------------------
    # fc: DIAGNOSTIC PROBE (not a classifier)
    #   output 0     : no up-left end found
    #   output 1..8  : the listed cell has the strongest up-left end
    #   output 9     : the strongest up-left end is in one of the other cells
    # ------------------------------------------------------------------
    def cidx(ch, i, j):
        return ch * 16 + i * 4 + j

    CH = 9
    chain = [(CH, 1, 0), (CH, 1, 1), (CH, 2, 0), (CH, 2, 1),
             (CH, 2, 2), (CH, 3, 0), (CH, 3, 1), (CH, 3, 2)]
    rest = [(CH, i, j) for i in range(4) for j in range(4) if (CH, i, j) not in chain]
    theta = 0.45                                   # end counts as present above this

    G = 100.0
    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for r in range(1, 9):
        fcw[r, cidx(*chain[r - 1])] += G           # G * (f - theta)
        fcb[r] += -G * theta
    for cell in rest:
        fcw[9, cidx(*cell)] += G                   # remaining cells pooled together
    fcb[9] += -G * theta

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
