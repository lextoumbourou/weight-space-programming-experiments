**What the second probe showed** (firing rates at a threshold of 0.4 on each channel's summed output):

| Digit | Closed hole | Open-left cavity | Open-right cavity |
|---|---|---|---|
| 0 | 39% | 90% | 93% |
| 1 | 0% | 14% | 12% |
| 2 | 45% | 97% | 88% |
| 3 | 51% | 99% | 94% |
| 4 | 47% | 69% | 69% |
| 5 | 32% | 94% | 95% |
| 6 | 80% | 76% | 96% |
| 7 | 29% | 94% | 35% |
| 8 | 88% | 98% | 97% |
| 9 | 78% | 92% | 84% |

- **Cavity channels fire on almost everything.** The pinched ends of any loop look like a side-open cavity. Their presence is only informative in two cases: both absent points to 1, and open-right absent points to 7. My rules forbidding them for 0, 3, 4, 6 and 9 were wrong.
- **Closed hole is moderately informative:** high for 6, 8 and 9, lower for the rest, never for 1.

**Changes in this step:**
1. **Narrow-bottom rule:** now a strong rule over the whole bottom row, in favour of 1, 4, 7 and 9 and against the others.
2. **New narrow-top channel:** a mirror of the narrow-bottom detector, replacing the unverified left-tip channel. It favours 1, 4 and 6 at moderate strength, since it is untested.
3. **Cavity rules:** forbids removed except strong ones for 1 and the open-right forbid for 7; only mild location preferences remain.
4. **Hole forbids:** softened.
5. **Class biases:** set from the step-7 prediction counts (down for 0, 3 and 8; up for 2, 5 and 6).

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
    # conv2
    #  0-7 : pooled oriented strokes (H, H, V, V, '/', '/', '\', '\')
    #  8: HOLE  9: SLOT  10: CUP  11: OL  12: OR   (exact ANDs of ink / background cells)
    #  13: narrow bottom (read in bottom grid row)   14: top tip
    #  15: narrow top (read in top grid row)
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

    # narrow bottom: narrow isolated stroke in the last kernel rows
    Kbot = np.zeros((5, 5))
    Kbot[4] = [-1.2, -0.3, 1.0, -0.3, -1.2]
    Kbot[3] = [-0.8, 0.4, 0.4, 0.4, -0.8]
    c2w[13, iINK] = 0.9 * Kbot
    c2b[13] = -0.27
    # top tip (with an "empty above" check)
    Ktop = np.array([[-1.2, -1.2, -1.0, -1.2, -1.2],
                     [-1.2, -0.3, 1.0, -0.3, -1.2],
                     [-0.8, 0.4, 0.4, 0.4, -0.8],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    c2w[14, iINK] = 1.3 * Ktop
    c2b[14] = -0.39
    # narrow top: mirror image of the narrow-bottom detector
    c2w[15, iINK] = 0.9 * np.flipud(Kbot)
    c2b[15] = -0.27

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

    # located point features: (channel, row tap, column tap)
    PT = {'HOLE': (8, 2, 2), 'SLOT': (9, 2, 2), 'CUP': (10, 2, 2), 'OL': (11, 2, 2),
          'OR': (12, 2, 2), 'top': (14, 1, 2)}

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
             ('CUP', 18, 13, 0.4), ('OL', 13.5, 16.5, 0.5), ('OR', 13.5, 10.5, 0.5)]),
        1: ([([(5, 14.5), (22, 12.5)], 1.0),
             ([(5, 17), (22, 10)], 0.6)],
            [('top', 5, 15, 1.0)]),
        2: ([([(9, 8.5), (6.5, 10), (5, 13), (6, 16.5), (9, 18), (12, 17), (16, 13.5),
               (20, 9.5), (22, 8), (21.5, 13), (21.5, 19.5)], 1.0)],
            [('OL', 10, 15, 0.6), ('OR', 18, 15, 0.4)]),
        3: ([([(7, 8.5), (5.5, 11), (5, 13.5), (6, 16.5), (8.5, 17.5), (11, 16.5), (13, 13)], 1.0),
             ([(13, 13), (14.5, 16.5), (17.5, 18), (20.5, 17), (22, 14), (22, 11), (20.5, 8)], 1.0)],
            [('OL', 8.8, 14.5, 1.0), ('OL', 17.7, 14.5, 1.0), ('OR', 13, 18.5, 0.3)]),
        4: ([([(5, 9.5), (10, 8.5), (15, 7.5)], 1.0),
             ([(15, 7.5), (15, 21)], 1.0),
             ([(5, 17), (22, 16.5)], 1.0)],
            [('top', 5, 9.5, 0.8), ('top', 5, 17, 0.8),
             ('CUP', 10, 12.75, 1.0), ('CUP', 12, 12.5, 0.7)]),
        5: ([([(5.5, 19), (5.5, 10.5)], 1.0),
             ([(5.5, 10.5), (13, 9.5)], 1.0),
             ([(13, 9.5), (11.5, 12.5), (12, 16), (14.5, 18.5), (18, 18.5), (21, 16.5),
               (22, 13), (21.5, 10), (20, 8)], 1.0)],
            [('OR', 8.7, 14.5, 1.0), ('OL', 16.75, 15, 1.0)]),
        6: ([([(5, 17.5), (8, 13.5), (12, 10.5), (16, 9), (20, 10), (22, 13), (21, 16.5),
               (18, 18), (15, 17), (13.5, 14), (15, 10.5)], 1.0)],
            [('top', 5, 17.5, 0.3), ('HOLE', 17.75, 13.5, 1.0), ('OR', 10.5, 15, 0.5),
             ('OL', 17.75, 15.5, 0.4), ('OR', 17.75, 11.5, 0.4)]),
        7: ([([(5.5, 7.5), (5.5, 19.5)], 1.0),
             ([(5.5, 19.5), (13, 16), (22, 12.5)], 1.0),
             ([(13.5, 11.5), (13.5, 19.5)], 0.3)],
            [('OL', 10, 15, 0.5)]),                       # wedge under the bar, left of the stem
        8: ([([(5, 15), (5, 12), (7, 10), (9.5, 10.5), (12.5, 13.5), (15.5, 16.5), (18.5, 17.5),
               (21.5, 16), (22.5, 13.5), (21.5, 11), (18.5, 9.5), (15.5, 10.5), (12.5, 13.5),
               (9.5, 16.5), (7, 17), (5, 15)], 1.0)],
            [('HOLE', 8.5, 13.5, 0.7), ('HOLE', 17.5, 13.5, 1.0),
             ('OL', 12.5, 9.5, 0.7), ('OR', 12.5, 17.5, 0.7)]),
        9: ([([(8, 17.5), (5.5, 15.5), (5, 12.5), (7, 9.5), (10, 9), (13, 10.5), (14, 13.5),
               (12.5, 16.5), (8, 17.5)], 1.0),
             ([(6, 17.5), (13, 17.5), (22, 15.5)], 1.0)],
            [('HOLE', 9.5, 13.25, 1.0), ('OL', 9.5, 15, 0.4), ('OR', 9.5, 11.5, 0.4)]),
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
    TH = {8: 0.3, 9: 0.3, 10: 0.3, 11: 0.3, 12: 0.3, 14: 0.15}
    # how strongly each digit (index 0..9) forbids the feature where it is not expected
    FORB = {
        8:  [0.4, 1.5, 0.2, 0.4, 0.4, 0.6, 0.5, 0.7, 0.0, 0.5],   # HOLE
        9:  [0.0, 1.0, 0.6, 0.6, 0.0, 0.6, 0.6, 0.6, 0.6, 0.6],   # SLOT
        10: [0.0, 1.0, 0.4, 0.6, 0.0, 0.6, 0.3, 0.6, 0.6, 0.3],   # CUP
        11: [0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],   # OL (probe: only 1 lacks it)
        12: [0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],   # OR (probe: 1 and 7 lack it)
        14: [0.3, 0.0, 0.2, 0.2, 0.0, 0.1, 0.0, 0.0, 0.3, 0.3],   # top tip
    }
    # narrow-bottom rule (verified by probe): summed over the bottom grid row
    WB = 2.0
    BOTSET = (1, 4, 7, 9)
    FB = [1.0, 0.0, 0.4, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0]
    # narrow-top rule (new, moderate): summed over the top grid row
    WT = 1.2
    TOPSET = (1, 4, 6)
    FT = [1.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.0, 0.7, 1.0, 1.0]
    CLASS_BIAS = [-0.3, 0.0, 0.3, -0.5, 0.0, 0.3, 0.3, 0.0, -0.3, 0.0]

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
        for ch in (8, 9, 10, 11, 12, 14):
            Wc = A * T[d, ch].copy()
            mask = T[d, ch] < 0.05
            Wc[mask] = -A * F0 * FORB[ch][d]
            fcw[d, ch * 16:(ch + 1) * 16] = Wc.reshape(16)
        for (kind, y, x, w) in protos[d][1]:
            ch = PT[kind][0]
            b -= A * TH[ch] * w   # a required feature that is absent costs the class
        # narrow bottom: bottom grid row (R=3) of channel 13
        if d in BOTSET:
            fcw[d, 13 * 16 + 12:13 * 16 + 16] = WB
            b -= WB * 0.3
        else:
            fcw[d, 13 * 16 + 12:13 * 16 + 16] = -WB * FB[d]
        # narrow top: top grid row (R=0) of channel 15
        if d in TOPSET:
            fcw[d, 15 * 16 + 0:15 * 16 + 4] = WT
            b -= WT * 0.3
        else:
            fcw[d, 15 * 16 + 0:15 * 16 + 4] = -WT * FT[d]
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
