import numpy as np
import math


def build_weights():
    # =====================================================================
    # conv1 (identical to step 7)
    #   0: horizontal line   1: '/' line   2: vertical line   3: '\' line
    #   4: background  bg = relu(1 - 2*centre-weighted ink)
    #   5: local ink   m  = mean of middle 3x3
    #   6: a = relu(3m - 0.8)     7: e = relu(3m - 1.8)
    #      strict saturated ink = a - e ;  loose saturated ink = 2.5m - 0.5a - e/3
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
    iH, iD1, iV, iD2, iBG, iINK, iA, iE = 0, 1, 2, 3, 4, 5, 6, 7
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
    c1w[iA, 0] = 3.0 * inkk
    c1b[iA] = -0.8
    c1w[iE, 0] = 3.0 * inkk
    c1b[iE] = -1.8

    # =====================================================================
    # conv2 (identical to step 7)
    #  0-7: pooled oriented strokes, 8: HOLE, 9: SLOT, 10: CUP, 11: OL, 12: OR,
    #  13: narrow bottom, 14: top tip, 15: left tip
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

    def ink_strict(ch, cell):
        c2w[ch, iA, cell[0], cell[1]] = 1.0
        c2w[ch, iE, cell[0], cell[1]] = -1.0

    def ink_loose(ch, cell):
        c2w[ch, iINK, cell[0], cell[1]] = 2.5
        c2w[ch, iA, cell[0], cell[1]] = -0.5
        c2w[ch, iE, cell[0], cell[1]] = -1.0 / 3.0

    def need_bg(ch, cell):
        c2w[ch, iBG, cell[0], cell[1]] = 1.0

    Lc, Rc, Uc, Dc, Cc = (2, 0), (2, 4), (0, 2), (4, 2), (2, 2)
    for cell in (Lc, Rc, Uc, Dc):          # HOLE
        ink_strict(8, cell)
    need_bg(8, Cc)
    for cell in (Lc, Rc):                  # SLOT
        ink_loose(9, cell)
    for cell in (Cc, Uc, Dc):
        need_bg(9, cell)
    for cell in (Lc, Rc):                  # CUP
        ink_loose(10, cell)
    ink_strict(10, Dc)
    for cell in (Cc, Uc):
        need_bg(10, cell)
    for cell in (Uc, Dc):                  # OL
        ink_strict(11, cell)
    ink_loose(11, Rc)
    for cell in (Cc, Lc):
        need_bg(11, cell)
    for cell in (Uc, Dc):                  # OR
        ink_strict(12, cell)
    ink_loose(12, Lc)
    for cell in (Cc, Rc):
        need_bg(12, cell)
    for ch in (8, 9, 10, 11, 12):
        c2b[ch] = -4.0

    Kbot = np.zeros((5, 5))
    Kbot[4] = [-1.2, -0.3, 1.0, -0.3, -1.2]
    Kbot[3] = [-0.8, 0.4, 0.4, 0.4, -0.8]
    c2w[13, iINK] = 0.9 * Kbot
    c2b[13] = -0.27
    Ktop = np.array([[-1.2, -1.2, -1.0, -1.2, -1.2],
                     [-1.2, -0.3, 1.0, -0.3, -1.2],
                     [-0.8, 0.4, 0.4, 0.4, -0.8],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    c2w[14, iINK] = 1.3 * Ktop
    c2b[14] = -0.39
    c2w[15, iINK] = 1.3 * Ktop.T
    c2b[15] = -0.39

    # =====================================================================
    # fc: DIAGNOSTIC PROBE.
    #   xa = sum of HOLE channel (8) over all cells
    #   xb = sum of OL channel (11) over all cells
    #   xc = sum of OR channel (12) over all cells
    # output k = a + 2b + 4c ; outputs 8 and 9 disabled.
    # =====================================================================
    M = 20.0
    va = np.zeros(256)
    vb = np.zeros(256)
    vc = np.zeros(256)
    va[8 * 16:9 * 16] = 1.0
    vb[11 * 16:12 * 16] = 1.0
    vc[12 * 16:13 * 16] = 1.0
    ta, tb, tc = 0.4, 0.4, 0.4

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
