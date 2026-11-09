**Step 1 approach:** a hand-built "oriented strokes + structure" network whose final layer is one hand-drawn stroke template per digit. Nothing has been run, so every magnitude here is an estimate to be corrected from the confusion matrix.

- **conv1:** four line detectors (horizontal, `/`, vertical, `\`), a "background here" detector and a local ink detector. Two filters are left unused.
- **conv2, channels 0–7:** each orientation pooled onto the 4x4 output grid at two offsets, giving five position bands along the axis that matters most for that orientation.
- **conv2, channels 8–11:** gap detectors — empty space between a left and a right wall, between an upper and a lower wall, and the latter open to the left or open to the right. Together these separate loops (0, 6, 8, 9), the open top of a 4, and the side-open cavities of 2, 3 and 5.
- **conv2, channels 12–15:** stroke-tip detectors (top tip, narrow bottom, left tip, right tip).
- **fc:** each digit is described as a polyline, shifted so its centre of mass sits at the image centre as MNIST does, and drawn directly onto the weight grid along with a few hand-placed gap and tip points. The bias is a nearest-template term, minus a fraction of the template's squared size.

```python
import numpy as np
import math


def build_weights():
    # =====================================================================
    # conv1: 8 filters on the raw image
    #   0: horizontal line   1: '/' diagonal line   2: vertical line
    #   3: '\' diagonal line 4: background (1 - local ink)   5: local ink
    #   6,7: unused
    # =====================================================================
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    LS = 1.3  # line gain so that a typical anti-aliased stroke gives ~1
    prof = [-1.0, 0.5, 1.0, 0.5, -1.0]          # profile across the stroke (zero sum)
    Hk = np.zeros((5, 5))
    for r in range(5):
        Hk[r, :] = prof[r] / 10.0
    Vk = Hk.T.copy()
    dprof = [1.0, 0.5, -0.25, -1.25, -1.25]     # by |distance from diagonal| (zero sum)
    D1k = np.zeros((5, 5))
    D2k = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            D2k[r, c] = dprof[abs(r - c)] / 9.0        # '\'  (main diagonal)
            D1k[r, c] = dprof[abs(r + c - 4)] / 9.0    # '/'  (anti diagonal)
    iH, iD1, iV, iD2, iBG, iINK = 0, 1, 2, 3, 4, 5
    c1w[iH, 0] = LS * Hk
    c1w[iD1, 0] = LS * D1k
    c1w[iV, 0] = LS * Vk
    c1w[iD2, 0] = LS * D2k
    # background detector: 1 - 2*(centre-weighted ink in the middle 3x3)
    bgk = np.zeros((5, 5))
    bgk[1:4, 1:4] = 0.05
    bgk[1, 2] = 0.1
    bgk[3, 2] = 0.1
    bgk[2, 1] = 0.1
    bgk[2, 3] = 0.1
    bgk[2, 2] = 0.4
    c1w[iBG, 0] = -2.0 * bgk
    c1b[iBG] = 1.0
    # ink detector: mean of the middle 3x3
    inkk = np.zeros((5, 5))
    inkk[1:4, 1:4] = 1.0 / 9.0
    c1w[iINK, 0] = inkk

    # =====================================================================
    # conv2: 16 feature maps (each ends as a 4x4 grid after pooling)
    #  0,1 : horizontal strokes, fine row bands (kernel row 1 / row 3)
    #  2,3 : vertical strokes, fine column bands (kernel col 1 / col 3)
    #  4,5 : '/' strokes, fine row bands      6,7 : '\' strokes, fine row bands
    #  8   : LR gap  = empty cell with a wall on the left AND on the right
    #  9   : UD gap  = empty cell with a wall above AND below
    #  10  : UD gap that is open to the left   (no wall on the left)
    #  11  : UD gap that is open to the right  (no wall on the right)
    #  12  : top stroke tip      13 : narrow (pointed) bottom
    #  14  : left stroke tip     15 : right stroke tip
    # =====================================================================
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    for b in (1, 2, 3):
        c2w[0, iH, 1, b] = 0.4
        c2w[1, iH, 3, b] = 0.4
        c2w[4, iD1, 1, b] = 0.8
        c2w[5, iD1, 3, b] = 0.8
        c2w[6, iD2, 1, b] = 0.8
        c2w[7, iD2, 3, b] = 0.8
    for a in (1, 2, 3):
        c2w[2, iV, a, 1] = 0.4
        c2w[3, iV, a, 3] = 0.4

    DW = 0.7  # how much a diagonal stroke counts as a wall
    # LR gap: background at centre + vertical-ish wall left + right, thresholded (AND)
    c2w[8, iBG, 2, 2] = 1.0
    for cc in (0, 1, 3, 4):
        c2w[8, iV, 2, cc] = 1.0
        c2w[8, iD1, 2, cc] = DW
        c2w[8, iD2, 2, cc] = DW
    c2b[8] = -2.4
    # UD gaps: background at centre + horizontal-ish wall above + below
    for ch in (9, 10, 11):
        c2w[ch, iBG, 2, 2] = 1.0
        for rr in (0, 1, 3, 4):
            c2w[ch, iH, rr, 2] = 1.0
            c2w[ch, iD1, rr, 2] = DW
            c2w[ch, iD2, rr, 2] = DW
        c2b[ch] = -2.4
    for cc in (0, 1):   # open-left version is vetoed by a left wall
        c2w[10, iV, 2, cc] = -1.5
        c2w[10, iD1, 2, cc] = -1.5 * DW
        c2w[10, iD2, 2, cc] = -1.5 * DW
    for cc in (3, 4):   # open-right version is vetoed by a right wall
        c2w[11, iV, 2, cc] = -1.5
        c2w[11, iD1, 2, cc] = -1.5 * DW
        c2w[11, iD2, 2, cc] = -1.5 * DW

    # stroke tips, computed on the ink map
    # top tip at kernel cell (1,2): ink there and below, nothing above / sideways
    Ktop = np.array([[-1.2, -1.2, -1.0, -1.2, -1.2],
                     [-1.2, -0.3, 1.0, -0.3, -1.2],
                     [-0.8, 0.4, 0.4, 0.4, -0.8],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    c2w[12, iINK] = 1.3 * Ktop
    c2b[12] = -0.39
    # narrow bottom: narrow isolated stroke in the last kernel rows (used only in bottom grid row)
    Kbot = np.zeros((5, 5))
    Kbot[4] = [-1.2, -0.3, 1.0, -0.3, -1.2]
    Kbot[3] = [-0.8, 0.4, 0.4, 0.4, -0.8]
    c2w[13, iINK] = 0.9 * Kbot
    c2b[13] = -0.27
    # left tip at (2,1): transpose of the top tip
    Kleft = Ktop.T.copy()
    c2w[14, iINK] = 1.3 * Kleft
    c2b[14] = -0.39
    # right tip: mirror of left tip, shifted up one row so the tip sits at (1,3)
    Kr = np.fliplr(Kleft)
    Kright = np.zeros((5, 5))
    Kright[0:4] = Kr[1:5]
    c2w[15, iINK] = 1.3 * Kright
    c2b[15] = -0.39

    # =====================================================================
    # fc: one hand-drawn template per digit, drawn straight onto the
    # (channel, 4x4 cell) weight grid.
    # Geometry: a grid cell k of a channel whose kernel tap is t looks at
    # image coordinates [4k+2t+1.5, 4k+2t+5.5]; the 3-tap pooled axis looks at
    # [4k+3.5, 4k+11.5].
    # =====================================================================
    MARG = 2.5   # soft edge (pixels) for stroke templates
    PM = 2.5     # soft edge for point features

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

    # (conv2 channel, orientation index, row spec, column spec)
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
    PT = {'LR': (8, 2, 2), 'UD': (9, 2, 2), 'UDL': (10, 2, 2), 'UDR': (11, 2, 2),
          'top': (12, 1, 2), 'bot': (13, None, 2), 'left': (14, 2, 1), 'right': (15, 1, 3)}

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

    # ---------------- digit prototypes: (row, col) polylines in a box with rows 5..22 ----
    zero = []
    for k in range(25):
        t = 2.0 * math.pi * k / 24.0
        y = 13.5 - 8.5 * math.cos(t)
        x = 13.5 + 6.0 * math.sin(t) + 0.12 * (13.5 - y)   # slight right slant
        zero.append((y, x))

    protos = {
        0: ([(zero, 1.0)],
            [('LR', 8.0, 14.1, 0.8), ('LR', 13.5, 13.5, 0.6), ('LR', 19.0, 12.9, 0.8)]),
        1: ([([(5, 14.5), (22, 12.5)], 1.0),
             ([(5, 17), (22, 10)], 0.6)],                    # optional: strongly slanted 1
            [('top', 5, 15, 1.0), ('bot', 22, 12, 1.0)]),
        2: ([([(9, 8.5), (6.5, 10), (5, 13), (6, 16.5), (9, 18), (12, 17), (16, 13.5),
               (20, 9.5), (22, 8), (21.5, 13), (21.5, 19.5)], 1.0)],
            [('left', 9, 8.5, 0.5), ('right', 21.5, 19.5, 0.6),
             ('UD', 10, 15, 0.7), ('UDL', 10, 15, 0.7),
             ('UD', 18, 15, 0.5), ('UDR', 18, 15, 0.5), ('LR', 9, 13, 0.3)]),
        3: ([([(7, 8.5), (5.5, 11), (5, 13.5), (6, 16.5), (8.5, 17.5), (11, 16.5), (13, 13)], 1.0),
             ([(13, 13), (14.5, 16.5), (17.5, 18), (20.5, 17), (22, 14), (22, 11), (20.5, 8)], 1.0)],
            [('left', 7, 8.5, 0.6), ('left', 20.5, 8, 0.6), ('left', 13, 12.5, 0.4),
             ('UD', 8.8, 14.5, 1.0), ('UDL', 8.8, 14.5, 1.0),
             ('UD', 17.7, 14.5, 1.0), ('UDL', 17.7, 14.5, 1.0)]),
        4: ([([(5, 9.5), (10, 8.5), (15, 7.5)], 1.0),
             ([(15, 7.5), (15, 21)], 1.0),
             ([(5, 17), (22, 16.5)], 1.0)],
            [('top', 5, 9.5, 0.8), ('top', 5, 17, 0.8), ('bot', 22, 16.5, 1.0),
             ('right', 15, 21, 0.4), ('LR', 9.5, 12.75, 1.0), ('LR', 12, 12.5, 0.6)]),
        5: ([([(5.5, 19), (5.5, 10.5)], 1.0),
             ([(5.5, 10.5), (13, 9.5)], 1.0),
             ([(13, 9.5), (11.5, 12.5), (12, 16), (14.5, 18.5), (18, 18.5), (21, 16.5),
               (22, 13), (21.5, 10), (20, 8)], 1.0)],
            [('right', 5.5, 19, 0.8), ('left', 20, 8, 0.6),
             ('UD', 8.7, 14.5, 0.8), ('UDR', 8.7, 14.5, 0.8),
             ('UD', 16.75, 15.5, 0.8), ('UDL', 16.75, 15.5, 0.8)]),
        6: ([([(5, 17.5), (8, 13.5), (12, 10.5), (16, 9), (20, 10), (22, 13), (21, 16.5),
               (18, 18), (15, 17), (13.5, 14), (15, 10.5)], 1.0)],
            [('top', 5, 17.5, 0.5), ('LR', 17.75, 13.5, 1.0), ('UD', 17.75, 13.5, 1.0),
             ('UD', 10.5, 15, 0.4), ('UDR', 10.5, 15, 0.4)]),
        7: ([([(5.5, 7.5), (5.5, 19.5)], 1.0),
             ([(5.5, 19.5), (13, 16), (22, 12.5)], 1.0),
             ([(13.5, 11.5), (13.5, 19.5)], 0.3)],           # optional crossbar
            [('left', 5.5, 7.5, 0.7), ('bot', 22, 12.5, 1.0),
             ('UD', 9.5, 15, 0.3), ('UDL', 9.5, 15, 0.3)]),
        8: ([([(5, 15), (5, 12), (7, 10), (9.5, 10.5), (12.5, 13.5), (15.5, 16.5), (18.5, 17.5),
               (21.5, 16), (22.5, 13.5), (21.5, 11), (18.5, 9.5), (15.5, 10.5), (12.5, 13.5),
               (9.5, 16.5), (7, 17), (5, 15)], 1.0)],
            [('LR', 8.5, 13.5, 0.8), ('UD', 8.5, 13.5, 0.8),
             ('LR', 17.5, 13.5, 0.8), ('UD', 17.5, 13.5, 0.8)]),
        9: ([([(8, 17.5), (5.5, 15.5), (5, 12.5), (7, 9.5), (10, 9), (13, 10.5), (14, 13.5),
               (12.5, 16.5), (8, 17.5)], 1.0),
             ([(6, 17.5), (13, 17.5), (22, 15.5)], 1.0)],
            [('bot', 22, 15.5, 1.0), ('LR', 9.5, 13.25, 1.0), ('UD', 9.5, 13.25, 1.0)]),
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

    # channel gains: structural channels have few active cells, so they get more weight
    G = [1.0] * 8 + [2.5, 2.0, 2.0, 2.0, 1.5, 2.0, 1.5, 1.5]
    S = 0.2        # global logit scale
    GAMMA = 0.35   # nearest-template bias: -GAMMA * |template|^2

    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for d in range(10):
        tot = 0.0
        for ch in range(16):
            fcw[d, ch * 16:(ch + 1) * 16] = S * G[ch] * T[d, ch].reshape(16)
            tot += G[ch] * float(np.sum(T[d, ch] ** 2))
        fcb[d] = -S * GAMMA * tot

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
