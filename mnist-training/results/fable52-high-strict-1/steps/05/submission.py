import numpy as np
import math


def build_weights():
    # =====================================================================
    # conv1 (unchanged from step 4)
    #   0: horizontal line   1: '/' diagonal line   2: vertical line
    #   3: '\' diagonal line 4: background (1 - local ink)   5: local ink
    # =====================================================================
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    LS = 1.3
    prof = [-1.0, 0.5, 1.0, 0.5, -1.0]
    Hk = np.zeros((5, 5))
    for r in range(5):
        Hk[r, :] = prof[r] / 10.0
    Vk = Hk.T.copy()
    dprof = [1.0, 0.5, -0.25, -1.25, -1.25]
    D1k = np.zeros((5, 5))
    D2k = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            D2k[r, c] = dprof[abs(r - c)] / 9.0        # '\'
            D1k[r, c] = dprof[abs(r + c - 4)] / 9.0    # '/'
    iH, iD1, iV, iD2, iBG, iINK = 0, 1, 2, 3, 4, 5
    c1w[iH, 0] = LS * Hk
    c1w[iD1, 0] = LS * D1k
    c1w[iV, 0] = LS * Vk
    c1w[iD2, 0] = LS * D2k
    bgk = np.zeros((5, 5))
    bgk[1:4, 1:4] = 0.05
    bgk[1, 2] = 0.1
    bgk[3, 2] = 0.1
    bgk[2, 1] = 0.1
    bgk[2, 3] = 0.1
    bgk[2, 2] = 0.4
    c1w[iBG, 0] = -2.0 * bgk
    c1b[iBG] = 1.0
    inkk = np.zeros((5, 5))
    inkk[1:4, 1:4] = 1.0 / 9.0
    c1w[iINK, 0] = inkk

    # =====================================================================
    # conv2 (unchanged from step 4)
    #  0-7: pooled oriented strokes, 8: LR gap, 9: UD gap, 10/11: UD gap open left/right,
    #  12: top tip, 13: narrow bottom, 14: left tip, 15: right tip
    # =====================================================================
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    DINH = 0.28
    for b in (1, 2, 3):
        c2w[0, iH, 1, b] = 0.4
        c2w[1, iH, 3, b] = 0.4
        for (ch, src, row) in ((4, iD1, 1), (5, iD1, 3), (6, iD2, 1), (7, iD2, 3)):
            c2w[ch, src, row, b] = 0.8
            c2w[ch, iH, row, b] = -DINH
            c2w[ch, iV, row, b] = -DINH
    for a in (1, 2, 3):
        c2w[2, iV, a, 1] = 0.4
        c2w[3, iV, a, 3] = 0.4

    WA, WD, WX = 0.42, 0.9, 0.8
    GAPB = -2.5
    c2w[8, iBG, 2, 2] = 1.0
    for cc in (0, 1, 3, 4):
        c2w[8, iV, 2, cc] = WA
        c2w[8, iD1, 2, cc] = WD
        c2w[8, iD2, 2, cc] = WD
        c2w[8, iH, 2, cc] = -WX
    c2b[8] = GAPB
    for ch in (9, 10, 11):
        c2w[ch, iBG, 2, 2] = 1.0
        for rr in (0, 1, 3, 4):
            c2w[ch, iH, rr, 2] = WA
            c2w[ch, iD1, rr, 2] = WD
            c2w[ch, iD2, rr, 2] = WD
            c2w[ch, iV, rr, 2] = -WX
        c2b[ch] = GAPB
    for cc in (0, 1):
        c2w[10, iV, 2, cc] = -1.5 * WA
        c2w[10, iD1, 2, cc] = -1.5 * WD
        c2w[10, iD2, 2, cc] = -1.5 * WD
        c2w[10, iH, 2, cc] = 0.75
    for cc in (3, 4):
        c2w[11, iV, 2, cc] = -1.5 * WA
        c2w[11, iD1, 2, cc] = -1.5 * WD
        c2w[11, iD2, 2, cc] = -1.5 * WD
        c2w[11, iH, 2, cc] = 0.75

    Ktop = np.array([[-1.2, -1.2, -1.0, -1.2, -1.2],
                     [-1.2, -0.3, 1.0, -0.3, -1.2],
                     [-0.8, 0.4, 0.4, 0.4, -0.8],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    c2w[12, iINK] = 1.3 * Ktop
    c2b[12] = -0.39
    Kbot = np.zeros((5, 5))
    Kbot[4] = [-1.2, -0.3, 1.0, -0.3, -1.2]
    Kbot[3] = [-0.8, 0.4, 0.4, 0.4, -0.8]
    c2w[13, iINK] = 0.9 * Kbot
    c2b[13] = -0.27
    Kleft = Ktop.T.copy()
    c2w[14, iINK] = 1.3 * Kleft
    c2b[14] = -0.39
    Kr = np.fliplr(Kleft)
    Kright = np.zeros((5, 5))
    Kright[0:4] = Kr[1:5]
    c2w[15, iINK] = 1.3 * Kright
    c2b[15] = -0.39

    # =====================================================================
    # fc: DIAGNOSTIC PROBE.
    # three scalar measurements (linear in the pooled features):
    #   xa = sum of LR-gap channel (8) over all 16 cells
    #   xb = sum of UD-gap channel (9) over all 16 cells
    #   xc = sum of narrow-bottom channel (13) over the bottom grid row
    # output k = a + 2b + 4c gets logit  M * sum_bits (+/-)(x - tau),
    # so the argmax is the combination of thresholded bits. Outputs 8, 9 are disabled.
    # =====================================================================
    M = 20.0
    va = np.zeros(256)
    vb = np.zeros(256)
    vc = np.zeros(256)
    va[8 * 16:9 * 16] = 1.0
    vb[9 * 16:10 * 16] = 1.0
    vc[13 * 16 + 12:13 * 16 + 16] = 1.0     # bottom row (R=3) of channel 13
    ta, tb, tc = 0.3, 0.3, 0.3

    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for k in range(8):
        sa = 1.0 if (k & 1) else -1.0
        sb = 1.0 if (k & 2) else -1.0
        sc = 1.0 if (k & 4) else -1.0
        fcw[k] = M * (sa * va + sb * vb + sc * vc)
        fcb[k] = -M * (sa * ta + sb * tb + sc * tc)
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
