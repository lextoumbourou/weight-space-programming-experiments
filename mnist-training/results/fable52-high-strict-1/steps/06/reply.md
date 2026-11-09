**What the probe showed** (reading the output as LR bit + 2·UD bit + 4·bottom bit):

- **Narrow-bottom detector works.** It fires on about 95% or more of 1, 4, 7 and 9, and on about 3–11% of 0, 3, 5, 6 and 8. Digit 2 is the exception at about 24%.
- **LR and UD gap detectors carry little information at this threshold.** They fire on nearly every digit, including about 85% of 1s for LR.

The narrow-bottom detector differs from the gap detectors in one way: its inputs are ink and background maps that are capped at 1, so an AND of several conditions is exact. The gap detectors summed uncapped line responses, where one strong wall can stand in for two.

**Changes in this step:**
- **Saturated ink:** conv1 gets one more channel so conv2 can form "ink present in this cell", capped at exactly 1.
- **Gap channels rebuilt as exact ANDs** of capped ink and background cells. Each needs all five conditions to fire:
  - closed hole (walls on all four sides),
  - tall slot (walls left and right, empty above and below — for 0),
  - cup open at the top (for 4),
  - cavity open to the left (3, top of 2, bottom of 5),
  - cavity open to the right (top of 5 and 6, bottom of 2).
- **Final layer:** cosine stroke templates as before, plus required/forbidden rules on the new channels and the verified narrow-bottom channel.

```python
import numpy as np
import math


def build_weights():
    # =====================================================================
    # conv1
    #   0: horizontal line   1: '/' line   2: vertical line   3: '\' line
    #   4: background  bg = relu(1 - 2*centre-weighted ink)   (in [0,1])
    #   5: local ink   m  = mean of middle 3x3                (in [0,1])
    #   6: ink excess  e  = relu(4*m - 1)   -> saturated ink  S = 4*m - e = min(4m, 1)
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
    iH, iD1, iV, iD2, iBG, iINK, iE = 0, 1, 2, 3, 4, 5, 6
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
    SK = 4.0
    c1w[iE, 0] = SK * inkk
    c1b[iE] = -1.0

    # =====================================================================
    # conv2
    #  0-7 : pooled oriented strokes (H, H, V, V, '/', '/', '\', '\')
    #  8   : HOLE  = empty centre with ink left, right, above and below
    #  9   : SLOT  = empty centre, ink left and right, empty above and below (tall hole of a 0)
    #  10  : CUP   = empty centre, ink left, right and below, empty above   (top of a 4)
    #  11  : OL    = empty centre, ink above, below and right, empty left   (cavities of a 3)
    #  12  : OR    = empty centre, ink above, below and left, empty right   (top of 5 / 6)
    #  13  : narrow bottom   14: top tip   15: left tip
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

    def need_ink(ch, r, c):      # saturated ink in that cell (value in [0,1])
        c2w[ch, iINK, r, c] = SK
        c2w[ch, iE, r, c] = -1.0

    def need_bg(ch, r, c):       # empty spot in that cell (value in [0,1])
        c2w[ch, iBG, r, c] = 1.0

    Lc, Rc, Uc, Dc, Cc = (2, 0), (2, 4), (0, 2), (4, 2), (2, 2)
    # exact 5-way ANDs: five terms in [0,1], bias -4
    for cell in (Lc, Rc, Uc, Dc):
        need_ink(8, cell[0], cell[1])
    need_bg(8, 2, 2)
    for cell in (Lc, Rc):
        need_ink(9, cell[0], cell[1])
    for cell in (Cc, Uc, Dc):
        need_bg(9, cell[0], cell[1])
    for cell in (Lc, Rc, Dc):
        need_ink(10, cell[0], cell[1])
    for cell in (Cc, Uc):
        need_bg(10, cell[0], cell[1])
    for cell in (Uc, Dc, Rc):
        need_ink(11, cell[0], cell[1])
    for cell in (Cc, Lc):
        need_bg(11, cell[0], cell[1])
    for cell in (Uc, Dc, Lc):
        need_ink(12, cell[0], cell[1])
    for cell in (Cc, Rc):
        need_bg(12, cell[0], cell[1])
    for ch in (8, 9, 10, 11, 12):
        c2b[ch] = -4.0

    # narrow bottom (verified by the probe), top tip, left tip: on the plain ink map
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
    # fc templates, drawn directly on the (channel, 4x4) weight grid
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

    # point features: (channel, row tap (None = bottom grid row only), column tap)
    PT = {'HOLE': (8, 2, 2), 'SLOT': (9, 2, 2), 'CUP': (10, 2, 2), 'OL': (11, 2, 2),
          'OR': (12, 2, 2), 'bot': (13, None, 2), 'top': (14, 1, 2), 'left': (15, 2, 1)}

    def draw_point(Td, kind, y, x, w):
        ch, rt, ct = PT[kind]
        for R in range(4):
            if rt is None:
                mr = 1.0 if R == 3 else 0.0
            else:
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
             ('CUP', 18, 13, 0.4)]),
        1: ([([(5, 14.5), (22, 12.5)], 1.0),
             ([(5, 17), (22, 10)], 0.6)],
            [('top', 5, 15, 1.0), ('bot', 22, 12, 1.0)]),
        2: ([([(9, 8.5), (6.5, 10), (5, 13), (6, 16.5), (9, 18), (12, 17), (16, 13.5),
               (20, 9.5), (22, 8), (21.5, 13), (21.5, 19.5)], 1.0)],
            [('left', 9, 8.5, 0.3), ('OL', 10, 15, 0.6), ('OR', 18, 15, 0.4)]),
        3: ([([(7, 8.5), (5.5, 11), (5, 13.5), (6, 16.5), (8.5, 17.5), (11, 16.5), (13, 13)], 1.0),
             ([(13, 13), (14.5, 16.5), (17.5, 18), (20.5, 17), (22, 14), (22, 11), (20.5, 8)], 1.0)],
            [('left', 7, 8.5, 0.5), ('left', 20.5, 8, 0.5),
             ('OL', 8.8, 14.5, 1.0), ('OL', 17.7, 14.5, 1.0)]),
        4: ([([(5, 9.5), (10, 8.5), (15, 7.5)], 1.0),
             ([(15, 7.5), (15, 21)], 1.0),
             ([(5, 17), (22, 16.5)], 1.0)],
            [('top', 5, 9.5, 0.8), ('top', 5, 17, 0.8), ('bot', 22, 16.5, 1.0),
             ('CUP', 10, 12.75, 1.0), ('CUP', 12, 12.5, 0.7)]),
        5: ([([(5.5, 19), (5.5, 10.5)], 1.0),
             ([(5.5, 10.5), (13, 9.5)], 1.0),
             ([(13, 9.5), (11.5, 12.5), (12, 16), (14.5, 18.5), (18, 18.5), (21, 16.5),
               (22, 13), (21.5, 10), (20, 8)], 1.0)],
            [('left', 20, 8, 0.4), ('OR', 8.7, 14.5, 1.0), ('OL', 16.75, 15, 1.0)]),
        6: ([([(5, 17.5), (8, 13.5), (12, 10.5), (16, 9), (20, 10), (22, 13), (21, 16.5),
               (18, 18), (15, 17), (13.5, 14), (15, 10.5)], 1.0)],
            [('top', 5, 17.5, 0.3), ('HOLE', 17.75, 13.5, 1.0), ('OR', 10.5, 15, 0.5)]),
        7: ([([(5.5, 7.5), (5.5, 19.5)], 1.0),
             ([(5.5, 19.5), (13, 16), (22, 12.5)], 1.0),
             ([(13.5, 11.5), (13.5, 19.5)], 0.3)],
            [('left', 5.5, 7.5, 0.5), ('bot', 22, 12.5, 1.0)]),
        8: ([([(5, 15), (5, 12), (7, 10), (9.5, 10.5), (12.5, 13.5), (15.5, 16.5), (18.5, 17.5),
               (21.5, 16), (22.5, 13.5), (21.5, 11), (18.5, 9.5), (15.5, 10.5), (12.5, 13.5),
               (9.5, 16.5), (7, 17), (5, 15)], 1.0)],
            [('HOLE', 8.5, 13.5, 0.7), ('HOLE', 17.5, 13.5, 1.0)]),
        9: ([([(8, 17.5), (5.5, 15.5), (5, 12.5), (7, 9.5), (10, 9), (13, 10.5), (14, 13.5),
               (12.5, 16.5), (8, 17.5)], 1.0),
             ([(6, 17.5), (13, 17.5), (22, 15.5)], 1.0)],
            [('bot', 22, 15.5, 1.0), ('HOLE', 9.5, 13.25, 1.0)]),
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
    A = 1.3      # scale of the structural rules
    F0 = 0.5     # base strength of "forbidden feature" penalties
    GA = {8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0}
    TH = {8: 0.3, 9: 0.3, 10: 0.3, 11: 0.3, 12: 0.3, 13: 0.35, 14: 0.15, 15: 0.15}
    # how strongly each digit (index 0..9) forbids the feature where it is not expected
    FORB = {
        8:  [0.5, 1.0, 0.0, 0.7, 0.5, 1.0, 0.5, 1.0, 0.0, 0.5],   # HOLE
        9:  [0.0, 1.0, 1.0, 1.0, 0.2, 1.0, 1.0, 1.0, 1.0, 1.0],   # SLOT
        10: [0.0, 1.0, 0.7, 1.0, 0.0, 1.0, 0.5, 1.0, 1.0, 0.3],   # CUP
        11: [1.0, 1.0, 0.3, 0.0, 1.0, 0.5, 1.0, 0.2, 1.0, 0.3],   # OL
        12: [1.0, 1.0, 0.3, 1.0, 0.7, 0.5, 0.5, 1.0, 1.0, 1.0],   # OR
        13: [1.0, 0.0, 0.5, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0],   # narrow bottom (bottom row only)
        14: [0.3, 0.0, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0, 0.3, 0.3],   # top tip
        15: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],   # left tip
    }
    CLASS_BIAS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2, 0.0]

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
        # structural channels: required features (positive, thresholded) and forbidden ones (negative)
        for ch in range(8, 16):
            Wc = A * GA[ch] * T[d, ch].copy()
            mask = T[d, ch] < 0.05
            if ch == 13:
                mask[0:3, :] = False     # narrow-bottom channel is only meaningful in the bottom row
            Wc[mask] = -A * GA[ch] * F0 * FORB[ch][d]
            fcw[d, ch * 16:(ch + 1) * 16] = Wc.reshape(16)
        b = CLASS_BIAS[d]
        for (kind, y, x, w) in protos[d][1]:
            ch = PT[kind][0]
            b -= A * GA[ch] * TH[ch] * w   # a required feature that is absent costs the class
        fcb[d] = b

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
