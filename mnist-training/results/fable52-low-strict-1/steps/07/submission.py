import numpy as np
import math


def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    # channel k detects strokes whose direction is theta = k*45deg
    # (x = column to the right, y = row downward)
    # k=0 horizontal, k=1 "\" , k=2 vertical, k=3 "/" ; channels 4..7 unused.
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)
    for k in range(4):
        th = k * math.pi / 4.0
        ker = np.zeros((5, 5))
        for iy in range(5):
            for ix in range(5):
                dy, dx = iy - 2, ix - 2
                d = -dx * math.sin(th) + dy * math.cos(th)  # perpendicular distance to line
                ker[iy, ix] = math.exp(-d * d / 2.0)
        ker -= ker.mean()                 # zero mean: solid ink / background -> 0
        ker /= ker[ker > 0].sum()         # ideal stroke -> response about 1
        conv1_w[k, 0] = ker
        conv1_b[k] = -0.05                # small threshold against noise

    # ---------------- conv2: 2x2 box averages at 4 phases ----------------
    # channel = k*4 + orow*2 + ocol ; reads orientation k only.
    # After pool2, cell (i,j) of this channel is centred at input pixel
    # row 4i+2*orow+6.5, col 4j+2*ocol+6.5  -> interleaved 8x8 grid, centre 6.5+2R.
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros((16,), dtype=np.float32)
    for k in range(4):
        for orow in range(2):
            for ocol in range(2):
                ch = k * 4 + orow * 2 + ocol
                conv2_w[ch, k, 1 + orow:3 + orow, 1 + ocol:3 + ocol] = 0.25

    # ---------------- hand-described digit strokes ----------------
    # unit coords: x right, y down, 1.0 = 20 pixels (the MNIST digit box height)
    def arc(cx, cy, rx, ry, a0, a1, n=30):
        # angles in degrees; 0=right, 90=bottom, 180=left, 270=top
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * t / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
                for t in range(n + 1)]

    # positive strokes: (weight, polyline)
    digits = {
        0: [(1.0, arc(0.5, 0.5, 0.36, 0.50, 0, 360))],
        1: [(1.0, [(0.5, 0.0), (0.5, 1.0)]),
            (0.6, [(0.70, 0.0), (0.30, 1.0)])],          # more slanted way of writing 1
        2: [(1.0, arc(0.5, 0.27, 0.25, 0.25, 190, 400) + [(0.22, 0.95)]),
            (1.0, [(0.22, 0.95), (0.82, 0.95)])],
        3: [(1.0, arc(0.45, 0.26, 0.25, 0.24, 200, 450)),
            (1.0, arc(0.45, 0.74, 0.28, 0.24, 270, 510))],
        4: [(1.0, [(0.32, 0.02), (0.20, 0.58)]),
            (1.0, [(0.20, 0.58), (0.85, 0.58)]),
            (1.0, [(0.66, 0.05), (0.66, 1.0)])],
        5: [(1.0, [(0.78, 0.03), (0.36, 0.03)]),
            (1.0, [(0.36, 0.03), (0.33, 0.42)]),
            (1.0, arc(0.45, 0.69, 0.28, 0.27, 235, 510))],
        6: [(1.0, [(0.70, 0.02), (0.48, 0.20), (0.33, 0.42), (0.27, 0.65)]),
            (1.0, arc(0.50, 0.72, 0.23, 0.24, 0, 360))],
        7: [(1.0, [(0.18, 0.04), (0.80, 0.04)]),
            (1.0, [(0.80, 0.04), (0.45, 1.0)])],
        8: [(1.0, arc(0.5, 0.25, 0.18, 0.23, 0, 360)),
            (1.0, arc(0.5, 0.75, 0.21, 0.24, 0, 360)),
            (0.7, [(0.36, 0.36), (0.64, 0.64)]),          # the crossing in the middle of an 8
            (0.7, [(0.64, 0.36), (0.36, 0.64)])],
        9: [(1.0, arc(0.45, 0.27, 0.22, 0.24, 0, 360)),
            (1.0, [(0.67, 0.20), (0.66, 0.60), (0.60, 0.98)])],
    }
    # adjustment strokes, drawn into class Y to stop other digits X being read as Y:
    #  'all' = Y must have no ink of any orientation here (X does)
    #  'ori' = Y must have no stroke of this direction here
    #  'pos' = extra weight on a stroke that is distinctive for Y (X lacks it)
    adj = {
        0: [('all', [(0.5, 0.38), (0.5, 0.62)])],                 # empty centre (vs 8, 2)
        1: [('ori', [(0.30, 0.03), (0.70, 0.03)]),                # no horizontal strokes (vs 7, 8, 4, 2)
            ('ori', [(0.30, 0.50), (0.70, 0.50)]),
            ('ori', [(0.30, 0.97), (0.70, 0.97)]),
            ('all', [(0.22, 0.15), (0.22, 0.45)]),                # nothing upper-left (vs 4, 8, 0)
            ('all', [(0.78, 0.60), (0.78, 0.85)])],               # nothing lower-right (vs 6, 8, 0)
        2: [('all', [(0.76, 0.60), (0.76, 0.78)]),                # lower right empty (vs 3, 8, 9)
            ('pos', [(0.45, 0.95), (0.85, 0.95)])],               # the base
        3: [('all', [(0.18, 0.36), (0.18, 0.46)]),                # left side empty (vs 5, 8, 9)
            ('ori', [(0.25, 0.86), (0.50, 0.62)]),                # no "/" diagonal in the lower part (vs 2)
            ('all', [(0.82, 0.98), (0.92, 0.98)])],               # no base sticking out bottom-right (vs 2)
        4: [('ori', [(0.36, 0.03), (0.62, 0.03)]),                # open top (vs 9)
            ('all', [(0.28, 0.88), (0.40, 0.95)]),                # lower left empty (vs 2, 8)
            ('pos', [(0.72, 0.58), (0.88, 0.58)])],               # bar crossing the stem
        5: [('all', [(0.19, 0.58), (0.19, 0.68)]),                # open lower-left (vs 6)
            ('all', [(0.74, 0.20), (0.74, 0.36)]),                # upper right empty (vs 3, 9, 8)
            ('pos', [(0.35, 0.12), (0.34, 0.40)])],               # upper-left vertical (3 lacks it)
        6: [('all', [(0.80, 0.15), (0.80, 0.40)]),                # upper right empty (vs 0, 8)
            ('ori', [(0.50, 0.03), (0.82, 0.03)]),                # no top bar (vs 5)
            ('pos', [(0.27, 0.60), (0.27, 0.85)])],               # closed lower-left side (5 lacks it)
        7: [('all', [(0.22, 0.22), (0.22, 0.42)]),                # no loop on the upper left (vs 9)
            ('all', [(0.82, 0.70), (0.82, 0.95)]),                # lower right empty (vs 2, 3, 8)
            ('all', [(0.20, 0.62), (0.20, 0.90)])],               # lower left empty (vs 8, 2)
        8: [('pos', [(0.29, 0.66), (0.29, 0.84)]),                # both sides of the lower loop
            ('pos', [(0.71, 0.66), (0.71, 0.84)])],
        9: [('all', [(0.22, 0.65), (0.22, 0.90)]),                # lower left empty (vs 8, 2, 6)
            ('ori', [(0.78, 0.58), (0.94, 0.58)]),                # no bar to the right of the stem (vs 4)
            ('pos', [(0.33, 0.03), (0.58, 0.03)]),                # closed top (4 lacks it)
            ('pos', [(0.23, 0.15), (0.23, 0.40)])],               # left side of the loop (7 lacks it)
    }
    shear = 0.10       # typical right-leaning slant of handwriting
    sigma = 2.5        # blur (pixels) of the template windows
    centres = 6.5 + 2.0 * np.arange(8)   # window centres in input pixels

    alpha = 8.0        # logit scale
    pen = 0.02         # general penalty for strokes where the digit has no ink
    gamma = 0.5        # fraction of the template mean that is subtracted
    kappa = 0.15       # strength of the adjustment strokes

    def sample(poly, w):
        # -> list of (col, row, angle, weighted length) in pixel units, sheared
        out = []
        pts = [((x + shear * (0.5 - y)) * 20.0, y * 20.0) for (x, y) in poly]
        for (p0, p1) in zip(pts[:-1], pts[1:]):
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = math.hypot(dx, dy)
            if L < 1e-9:
                continue
            n = max(1, int(math.ceil(L / 0.5)))
            th = math.atan2(dy, dx)
            for t in range(n):
                f = (t + 0.5) / n
                out.append((p0[0] + f * dx, p0[1] + f * dy, th, w * L / n))
        return out

    def window(cx, cy):
        gr = np.exp(-(cy - centres) ** 2 / (2 * sigma ** 2))
        gc = np.exp(-(cx - centres) ** 2 / (2 * sigma ** 2))
        return np.outer(gr, gc)

    def tune(th, k):
        # response of orientation channel k to a stroke of direction th (cos^4 tuning)
        return math.cos(th - k * math.pi / 4.0) ** 4

    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros((10,), dtype=np.float32)

    for d in range(10):
        samples = []
        for (w, poly) in digits[d]:
            samples += sample(poly, w)
        S = np.array(samples)
        # centre of mass -> image centre, as MNIST does
        wsum = S[:, 3].sum()
        sx = 13.5 - (S[:, 0] * S[:, 3]).sum() / wsum
        sy = 13.5 - (S[:, 1] * S[:, 3]).sum() / wsum

        # draw positive strokes into the 4-orientation 8x8 map
        T = np.zeros((4, 8, 8))
        for (cx, cy, th, w) in S:
            g = window(cx + sx, cy + sy) * w
            for k in range(4):
                T[k] += tune(th, k) * g
        T = np.tanh(T / 4.0)                      # presence-like saturation
        ink = np.minimum(1.0, T.sum(axis=0))      # where this digit has any stroke

        # draw the adjustment strokes (N = negative, P = positive emphasis)
        N = np.zeros((4, 8, 8))
        P = np.zeros((4, 8, 8))
        for (kind, poly) in adj[d]:
            for (cx, cy, th, w) in sample(poly, 1.0):
                g = window(cx + sx, cy + sy) * w
                for k in range(4):
                    if kind == 'all':
                        N[k] += 0.7 * g
                    elif kind == 'ori':
                        N[k] += tune(th, k) * g
                    else:
                        P[k] += tune(th, k) * g
        A = np.tanh(P / 4.0) - np.tanh(N / 4.0)

        Wd = T / np.sqrt((T ** 2).sum()) - pen * (1.0 - ink)[None, :, :]
        Wd -= gamma * Wd.mean()                   # partial centring: balance broad vs narrow digits
        Wd += kappa * (A - A.mean())              # zero-sum adjustments (keep class balance)
        Wd *= alpha

        # write into the fc layout: flatten index = channel*16 + i*4 + j
        for k in range(4):
            for R in range(8):
                for C in range(8):
                    ch = k * 4 + (R % 2) * 2 + (C % 2)
                    idx = ch * 16 + (R // 2) * 4 + (C // 2)
                    fc_w[d, idx] = Wd[k, R, C]

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
