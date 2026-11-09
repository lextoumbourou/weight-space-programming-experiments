**Reading step 14:** level with step 13 (78.65% against 78.66%), but the two parts of the change pulled in opposite directions.

- **The `\` penalty on 2 helped.** Wrong "2" predictions fell from 279 to 139, most of them 8s now read correctly, at a cost of about 55 true 2s.
- **The small `\` bonus for 8 hurt.** It added clear new false 8s: 5 → 8 went from 46 to 77, 6 → 8 from 45 to 69, 0 → 8 from 31 to 43, and 3 → 8 from 38 to 49.

**Final step:** I keep the penalty on 2 and remove the bonus for 8, which I estimate is worth roughly half a percent. Two small bias adjustments go with it:
- 2 goes up, since it is now the most under-predicted class (711 predictions against 990 true).
- 0 goes down slightly, since it is still over-predicted.

Everything else is identical to step 14. These last adjustments are not validated, so the final network could land slightly either side of 78.7%.

```python
import numpy as np
import math


def build_weights():
    # =====================================================================
    # conv1
    #   0: horizontal line   1: '/' line   2: vertical line   3: '\' line
    #   4: background  bg = relu(1 - 2*centre-weighted ink)
    #   5: local ink   m  = mean of middle 3x3
    #   6: a = relu(3m - 0.8)     7: e = relu(3m - 1.8)
    #      strict saturated ink = a - e ;  loose saturated ink = 2.5m - 0.5a - e/3
    # =====================================================================
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    LS = 1.3
    prof = [-1.0, 0.5, 1.0, 0.5, -1.0]          # profile across a stroke (zero sum)
    Hk = np.zeros((5, 5))
    for r in range(5):
        Hk[r, :] = prof[r] / 10.0
    Vk = Hk.T.copy()
    dprof = [1.0, 0.5, -0.25, -1.25, -1.25]     # by |distance from the diagonal| (zero sum)
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
    # conv2
    #  0-7 : pooled oriented strokes (H, H, V, V, '/', '/', '\', '\')
    #  8: HOLE (8-direction ring)  9: SLOT  10: OPENTOP  11: OL  12: OR
    #  13: narrow bottom (read in bottom grid row)
    #  14: right tip      15: narrow top (read in top grid row)
    # =====================================================================
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    DINH = 0.28   # diagonal channels are inhibited by H and V responses (cross-talk removal)
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

    def ink_strict(ch, cell):    # stroke really inside that cell (in [0,1])
        c2w[ch, iA, cell[0], cell[1]] = 1.0
        c2w[ch, iE, cell[0], cell[1]] = -1.0

    def ink_loose(ch, cell):     # stroke in or touching that cell (in [0,1])
        c2w[ch, iINK, cell[0], cell[1]] = 2.5
        c2w[ch, iA, cell[0], cell[1]] = -0.5
        c2w[ch, iE, cell[0], cell[1]] = -1.0 / 3.0

    def need_bg(ch, cell):       # an empty spot in that cell (in [0,1])
        c2w[ch, iBG, cell[0], cell[1]] = 1.0

    def no_ink(ch, cell):        # 1 - strict ink; the constant 1 goes into the bias
        c2w[ch, iA, cell[0], cell[1]] = -1.0
        c2w[ch, iE, cell[0], cell[1]] = 1.0

    Lc, Rc, Uc, Dc, Cc = (2, 0), (2, 4), (0, 2), (4, 2), (2, 2)
    # HOLE: ink in 8 directions around an empty centre (9 terms, bias -8)
    for cell in (Lc, Rc, Uc, Dc):
        ink_strict(8, cell)
    for cell in ((1, 1), (1, 3), (3, 1), (3, 3)):
        ink_loose(8, cell)
    need_bg(8, Cc)
    c2b[8] = -8.0
    # SLOT: walls left and right, empty centre / above / below (tall hole of a 0)
    for cell in (Lc, Rc):
        ink_loose(9, cell)
    for cell in (Cc, Uc, Dc):
        need_bg(9, cell)
    c2b[9] = -4.0
    # OPENTOP: walls left and right of the bottom cell, clear column of 4 cells above (top of a 4)
    ink_loose(10, (4, 0))
    ink_loose(10, (4, 4))
    for cell in ((4, 2), (3, 2), (2, 2), (1, 2)):
        no_ink(10, cell)
    c2b[10] = 4.0 - 5.0
    # OL: cavity open to the left
    for cell in (Uc, Dc):
        ink_strict(11, cell)
    ink_loose(11, Rc)
    for cell in (Cc, Lc):
        need_bg(11, cell)
    c2b[11] = -4.0
    # OR: cavity open to the right
    for cell in (Uc, Dc):
        ink_strict(12, cell)
    ink_loose(12, Lc)
    for cell in (Cc, Rc):
        need_bg(12, cell)
    c2b[12] = -4.0

    # narrow bottom: narrow isolated stroke in the last kernel rows
    Kbot = np.zeros((5, 5))
    Kbot[4] = [-1.2, -0.3, 1.0, -0.3, -1.2]
    Kbot[3] = [-0.8, 0.4, 0.4, 0.4, -0.8]
    c2w[13, iINK] = 0.9 * Kbot
    c2b[13] = -0.27
    # right tip: horizontal stroke ending on the right with nothing beyond
    Ktop = np.array([[-1.2, -1.2, -1.0, -1.2, -1.2],
                     [-1.2, -0.3, 1.0, -0.3, -1.2],
                     [-0.8, 0.4, 0.4, 0.4, -0.8],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    c2w[14, iINK] = 1.3 * np.fliplr(Ktop.T)
    c2b[14] = -0.39
    # narrow top: mirror image of the narrow-bottom detector
    c2w[15, iINK] = 0.9 * np.flipud(Kbot)
    c2b[15] = -0.27

    # =====================================================================
    # fc templates, drawn directly on the (channel, 4x4) weight grid.
    # A grid cell k of a channel with kernel tap t looks at image coordinates
    # [4k+2t+1.5, 4k+2t+5.5]; the 3-tap pooled axis looks at [4k+3.5, 4k+11.5].
    # =====================================================================
    MARG = 2.5
    PM = 2.5

    def mem(x, lo, hi, m):
        if x < lo:
            d = lo - x
        elif x > hi:
            d = x - hi
        else:
            d = 0.0
        return max(0.0, 1.0 - d / m)

    def band(k, t):
        return (4 * k + 2 * t + 1.5, 4 * k + 2 * t + 5.5)

    def wide(k):
        return (4 * k + 3.5, 4 * k + 11.5)

    def mvec(x, spec, m):
        out = []
        for k in range(4):
            if spec[0] == 'b':
                lo, hi = band(k, spec[1])
            else:
                lo, hi = wide(k)
            out.append(mem(x, lo, hi, m))
        return out

    ORI = [(0, 0, ('b', 1), ('w', 0)), (1, 0, ('b', 3), ('w', 0)),
           (2, 2, ('w', 0), ('b', 1)), (3, 2, ('w', 0), ('b', 3)),
           (4, 1, ('b', 1), ('w', 0)), (5, 1, ('b', 3), ('w', 0)),
           (6, 3, ('b', 1), ('w', 0)), (7, 3, ('b', 3), ('w', 0))]
    ANG = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]  # H, '/', V, '\'

    def centroid(strokes):
        sy = 0.0
        sx = 0.0
        sl = 0.0
        for pts, w in strokes:
            if w < 0.9:
                continue
            for i in range(len(pts) - 1):
                y0, x0 = pts[i]
                y1, x1 = pts[i + 1]
                L = math.hypot(y1 - y0, x1 - x0)
                sy += L * (y0 + y1) / 2.0
                sx += L * (x0 + x1) / 2.0
                sl += L
        return sy / sl, sx / sl

    def draw_strokes(Td, strokes, dy, dx):
        for pts, w in strokes:
            for i in range(len(pts) - 1):
                y0, x0 = pts[i]
                y1, x1 = pts[i + 1]
                L = math.hypot(y1 - y0, x1 - x0)
                n = max(1, int(math.ceil(L / 0.5)))
                th = math.atan2(-(y1 - y0), (x1 - x0)) % math.pi
                for o in range(4):
                    d = abs(th - ANG[o])
                    d = min(d, math.pi - d)
                    f = math.cos(2.0 * d)
                    if f <= 0.05:
                        continue
                    for (ch, oo, rs, cs) in ORI:
                        if oo != o:
                            continue
                        for s in range(n + 1):
                            y = y0 + (y1 - y0) * s / n + dy
                            x = x0 + (x1 - x0) * s / n + dx
                            mr = mvec(y, rs, MARG)
                            mc = mvec(x, cs, MARG)
                            for R in range(4):
                                if mr[R] <= 0.0:
                                    continue
                                for C in range(4):
                                    v = w * f * mr[R] * mc[C]
                                    if v > Td[ch, R, C]:
                                        Td[ch, R, C] = v

    # located point features: (channel, row tap, column tap)
    PT = {'HOLE': (8, 2, 2), 'SLOT': (9, 2, 2), 'OL': (11, 2, 2), 'OR': (12, 2, 2)}

    def draw_point(Td, kind, y, x, w):
        ch, rt, ct = PT[kind]
        for R in range(4):
            lo, hi = band(R, rt)
            mr = mem(y, lo, hi, PM)
            if mr <= 0.0:
                continue
            for C in range(4):
                lo, hi = band(C, ct)
                mc = mem(x, lo, hi, PM)
                v = w * mr * mc
                if v > Td[ch, R, C]:
                    Td[ch, R, C] = v

    # ---------------- digit prototypes ((row, col) polylines + structural points) --------
    zero = []
    for k in range(25):
        t = 2.0 * math.pi * k / 24.0
        y = 13.5 - 8.5 * math.cos(t)
        x = 13.5 + 6.0 * math.sin(t) + 0.12 * (13.5 - y)
        zero.append((y, x))

    protos = {
        0: ([(zero, 1.0)],
            [('SLOT', 13.5, 13.5, 1.0), ('SLOT', 10, 13.9, 0.7), ('SLOT', 17, 13.1, 0.7),
             ('OL', 13.5, 16.5, 0.5), ('OR', 13.5, 10.5, 0.5)]),
        1: ([([(5, 14.5), (22, 12.5)], 1.0),
             ([(5, 17), (22, 10)], 0.6)],
            []),
        2: ([([(9, 8.5), (6.5, 10), (5, 13), (6, 16.5), (9, 18), (12, 17), (16, 13.5),
               (20, 9.5), (22, 8), (21.5, 13), (21.5, 19.5)], 1.0)],
            [('OL', 10, 15, 0.6), ('OR', 18, 15, 0.4)]),
        3: ([([(7, 8.5), (5.5, 11), (5, 13.5), (6, 16.5), (8.5, 17.5), (11, 16.5), (13, 13)], 1.0),
             ([(13, 13), (14.5, 16.5), (17.5, 18), (20.5, 17), (22, 14), (22, 11), (20.5, 8)], 1.0)],
            [('OL', 8.8, 14.5, 1.0), ('OL', 17.7, 14.5, 1.0), ('OR', 13, 18.5, 0.3)]),
        4: ([([(5, 9.5), (10, 8.5), (15, 7.5)], 1.0),
             ([(15, 7.5), (15, 21)], 1.0),
             ([(5, 17), (22, 16.5)], 1.0)],
            []),
        5: ([([(5.5, 19), (5.5, 10.5)], 1.0),
             ([(5.5, 10.5), (13, 9.5)], 1.0),
             ([(13, 9.5), (11.5, 12.5), (12, 16), (14.5, 18.5), (18, 18.5), (21, 16.5),
               (22, 13), (21.5, 10), (20, 8)], 1.0)],
            [('OR', 8.7, 14.5, 1.0), ('OL', 16.75, 15, 1.0)]),
        6: ([([(5, 17.5), (8, 13.5), (12, 10.5), (16, 9), (20, 10), (22, 13), (21, 16.5),
               (18, 18), (15, 17), (13.5, 14), (15, 10.5)], 1.0)],
            [('HOLE', 17.75, 13.5, 1.0), ('OR', 10.5, 15, 0.5),
             ('OL', 17.75, 15.5, 0.4), ('OR', 17.75, 11.5, 0.4)]),
        7: ([([(5.5, 7.5), (5.5, 19.5)], 1.0),
             ([(5.5, 19.5), (13, 16), (22, 12.5)], 1.0),
             ([(13.5, 11.5), (13.5, 19.5)], 0.3)],
            [('OL', 10, 15, 0.5)]),
        8: ([([(5, 15), (5, 12), (7, 10), (9.5, 10.5), (12.5, 13.5), (15.5, 16.5), (18.5, 17.5),
               (21.5, 16), (22.5, 13.5), (21.5, 11), (18.5, 9.5), (15.5, 10.5), (12.5, 13.5),
               (9.5, 16.5), (7, 17), (5, 15)], 1.0)],
            [('HOLE', 8.5, 13.5, 0.5), ('HOLE', 17.5, 13.5, 0.8),
             ('OL', 12.5, 9.5, 0.7), ('OR', 12.5, 17.5, 0.7)]),
        9: ([([(8, 17.5), (5.5, 15.5), (5, 12.5), (7, 9.5), (10, 9), (13, 10.5), (14, 13.5),
               (12.5, 16.5), (8, 17.5)], 1.0),
             ([(6, 17.5), (13, 17.5), (22, 15.5)], 1.0)],
            [('HOLE', 9.5, 13.25, 1.0), ('OL', 9.5, 15, 0.4), ('OR', 9.5, 11.5, 0.8)]),
    }

    T = np.zeros((10, 16, 4, 4), dtype=np.float64)
    for d in range(10):
        strokes, points = protos[d]
        cy, cx = centroid(strokes)
        dy = 13.5 - cy      # MNIST centres each digit by its centre of mass
        dx = 13.5 - cx
        draw_strokes(T[d], strokes, dy, dx)
        for (kind, y, x, w) in points:
            draw_point(T[d], kind, y + dy, x + dx, w)

    # ---------------- fc assembly ----------------
    S = 1.5      # scale of the cosine-normalised orientation template score
    A = 1.3      # scale of the located structural rules
    F0 = 0.5     # base strength of "forbidden feature" penalties
    KW = {8: 1.0, 9: 0.45, 11: 1.0, 12: 1.0}
    THB = {8: 0.39, 9: 0.375, 11: 0.39, 12: 0.39}
    # how strongly each digit (index 0..9) forbids the feature where it is not expected
    FORB = {
        8:  [0.4, 1.5, 0.2, 0.8, 0.8, 0.9, 0.5, 1.3, 0.0, 0.5],   # HOLE
        9:  [0.0, 1.0, 0.6, 0.6, 0.0, 0.6, 0.6, 0.6, 0.6, 0.6],   # SLOT
        11: [0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],   # OL (only 1 lacks it)
        12: [0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.3, 0.0, 0.0],   # OR (1 and 7 lack it)
    }
    # OPENTOP rule (channel 10): expected for 4 in the two upper grid rows; neutral for 0
    WO = 1.3
    OT = [0.0, -1.0, -0.5, -0.5, 1.0, -0.5, -0.5, -1.0, -0.5, -1.0]
    # narrow-bottom rule (verified by probe): summed over the bottom grid row
    WB = 2.0
    BOTSET = (1, 4, 7, 9)
    FB = [1.0, 0.0, 0.2, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0]
    # narrow-top rule: summed over the top grid row
    WT = 1.2
    TOPSET = (1, 4, 6)
    FT = [1.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.0, 0.7, 1.0, 1.0]
    # right-tip rule: bottom grid row -> 2 ; top grid row -> 5
    WR = 1.2
    RT_BOTTOM = [-0.5, -0.5, 1.0, -0.5, 0.0, -0.5, -0.5, -0.5, -0.5, -0.5]
    RT_TOP = [-0.5, 0.0, -0.5, -0.5, 0.0, 1.0, 0.0, -0.5, -0.5, -0.5]
    CLASS_BIAS = [-0.35, 0.0, 0.75, -0.5, 0.3, 0.3, 0.3, 0.2, 0.0, -0.25]

    # hand-written discriminative "anti-strokes".
    # vertical-stroke channels:
    #   channel 2: column bands C=1 -> cols 7.5-11.5, C=3 -> cols 15.5-19.5
    #   channel 3: column bands C=0 -> cols 7.5-11.5, C=2 -> cols 15.5-19.5
    #   row windows: R=0 rows 3.5-11.5 (upper), R=2 rows 11.5-19.5, R=3 rows 15.5-23.5 (lower)
    # '\' channels:
    #   channel 6: row band R=2 -> rows 11.5-15.5 ; channel 7: row band R=1 -> rows 11.5-15.5
    #   column windows C=1 cols 7.5-15.5, C=2 cols 11.5-19.5 (centre)
    EXTRA = [
        # upper-left vertical stroke: stem of a 5, not found in 3
        (3, 2, (0,), (1,), -0.4), (3, 3, (0,), (0,), -0.4),
        (5, 2, (0,), (1,), 0.2), (5, 3, (0,), (0,), 0.2),
        # upper-right vertical stroke: arc of a 3, not found in 5 (or 6)
        (5, 2, (0,), (3,), -0.4), (5, 3, (0,), (2,), -0.4),
        (3, 2, (0,), (3,), 0.2), (3, 3, (0,), (2,), 0.2),
        (6, 2, (0,), (3,), -0.2), (6, 3, (0,), (2,), -0.2),
        # lower-left vertical stroke: loop wall of 8 / 6 / 0, not found in 3 and 5
        (3, 2, (2, 3), (1,), -0.3), (3, 3, (2, 3), (0,), -0.3),
        (5, 2, (3,), (1,), -0.4), (5, 3, (3,), (0,), -0.4),
        # '\' stroke through the centre: crossing of an 8, not found in 2
        (2, 6, (2,), (1, 2), -0.25), (2, 7, (1,), (1, 2), -0.25),
    ]

    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for d in range(10):
        # orientation channels: cosine-style template matching
        tot = 0.0
        for ch in range(8):
            tot += float(np.sum(T[d, ch] ** 2))
        nrm = math.sqrt(tot)
        for ch in range(8):
            fcw[d, ch * 16:(ch + 1) * 16] = S * T[d, ch].reshape(16) / nrm
        b = CLASS_BIAS[d]
        # located structural channels: required (positive, thresholded) / forbidden (negative)
        for ch in (8, 9, 11, 12):
            Wc = A * KW[ch] * T[d, ch].copy()
            mask = T[d, ch] < 0.05
            Wc[mask] = -A * F0 * FORB[ch][d]
            fcw[d, ch * 16:(ch + 1) * 16] = Wc.reshape(16)
        for (kind, y, x, w) in protos[d][1]:
            ch = PT[kind][0]
            b -= THB[ch] * w      # a required feature that is absent costs the class
        # OPENTOP: channel 10
        if OT[d] > 0.5:
            fcw[d, 10 * 16 + 0:10 * 16 + 8] = WO          # two upper grid rows
            b -= WO * 0.5
        else:
            fcw[d, 10 * 16:11 * 16] = WO * OT[d]
        # narrow bottom: bottom grid row (R=3) of channel 13
        if d in BOTSET:
            fcw[d, 13 * 16 + 12:13 * 16 + 16] = WB
            b -= WB * 0.3
        else:
            fcw[d, 13 * 16 + 12:13 * 16 + 16] = -WB * FB[d]
        # right tip: channel 14, bottom row (R=3) and top row (R=0)
        fcw[d, 14 * 16 + 12:14 * 16 + 16] = WR * RT_BOTTOM[d]
        fcw[d, 14 * 16 + 0:14 * 16 + 4] = WR * RT_TOP[d]
        if RT_BOTTOM[d] > 0.5 or RT_TOP[d] > 0.5:
            b -= WR * 0.2
        # narrow top: top grid row (R=0) of channel 15
        if d in TOPSET:
            fcw[d, 15 * 16 + 0:15 * 16 + 4] = WT
            b -= WT * 0.3
        else:
            fcw[d, 15 * 16 + 0:15 * 16 + 4] = -WT * FT[d]
        fcb[d] = b

    # add the hand-written anti-strokes
    for (d, ch, Rs, Cs, v) in EXTRA:
        for R in Rs:
            for C in Cs:
                fcw[d, ch * 16 + R * 4 + C] += v

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
