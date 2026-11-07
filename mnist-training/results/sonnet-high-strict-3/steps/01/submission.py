import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 hand-made 5x5 filters ----------------
    w1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    rr, cc = np.meshgrid(np.arange(-2, 3), np.arange(-2, 3), indexing="ij")

    def bar(dr, dc):
        # oriented line detector through the centre with direction (dr, dc);
        # gaussian ridge minus its mean (zero-sum), normalised so an ideal
        # stroke covering the positive part gives ~1
        n = math.hypot(dr, dc)
        dr, dc = dr / n, dc / n
        perp = rr * dc - cc * dr
        g = np.exp(-perp ** 2 / (2 * 0.9 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    w1[0, 0] = bar(1, 0)    # 0: vertical stroke
    w1[1, 0] = bar(0, 1)    # 1: horizontal stroke
    w1[2, 0] = bar(-1, 1)   # 2: "/" diagonal
    w1[3, 0] = bar(1, 1)    # 3: "\" diagonal
    g = np.exp(-(rr ** 2 + cc ** 2) / (2 * 1.3 ** 2))
    w1[4, 0] = g / g.sum()  # 4: ink blob (smoothed density)
    colg = np.exp(-cc ** 2 / (2 * 1.5 ** 2))
    prof = np.array([-1, -1, 0, 1, 1], dtype=np.float32)[:, None] * colg
    w1[5, 0] = prof / prof[prof > 0].sum()   # 5: ink below, empty above
    w1[6, 0] = -w1[5, 0]                     # 6: ink above, empty below
    rad = np.sqrt(rr ** 2 + cc ** 2)
    ring = np.exp(-(rad - 2.0) ** 2 / (2 * 0.6 ** 2))
    ring = ring / ring.sum()
    cen = np.exp(-rad ** 2 / (2 * 0.8 ** 2))
    cen = cen / cen.sum()
    w1[7, 0] = ring - 1.5 * cen              # 7: ring / hole detector
    b1[7] = -0.2

    # ---------------- conv2: 16 channels of region-pooled features ----------------
    w2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros(16, dtype=np.float32)

    def mask(kind):
        m = np.zeros((5, 5), dtype=np.float32)
        if kind == "full":
            m[:, :] = 1
        elif kind == "top":
            m[0:3, :] = 1
        elif kind == "bot":
            m[2:5, :] = 1
        elif kind == "left":
            m[:, 0:3] = 1
        elif kind == "right":
            m[:, 2:5] = 1
        elif kind == "center":
            m[1:4, 1:4] = 1
        return 2.0 * m / m.sum()

    spec = [
        (0, 0, "full"),    # 0: vertical anywhere
        (1, 1, "full"),    # 1: horizontal anywhere
        (2, 2, "full"),    # 2: "/" anywhere
        (3, 3, "full"),    # 3: "\" anywhere
        (4, 4, "full"),    # 4: ink density
        (5, 7, "full"),    # 5: hole anywhere
        (6, 5, "full"),    # 6: edge ink-below
        (7, 6, "full"),    # 7: edge ink-above
        (8, 1, "top"),     # 8: horizontal in upper part
        (9, 1, "bot"),     # 9: horizontal in lower part
        (10, 0, "left"),   # 10: vertical in left part
        (11, 0, "right"),  # 11: vertical in right part
        (12, 4, "center"), # 12: ink at centre
        (13, 7, "center"), # 13: hole at centre
        (14, 2, "bot"),    # 14: "/" in lower part
        (15, 3, "top"),    # 15: "\" in upper part
    ]
    for o, c, k in spec:
        w2[o, c] = mask(k)

    # ---------------- fc: class rules on the 4x4 grid of cells ----------------
    W = np.zeros((10, 16, 4, 4), dtype=np.float32)

    def s(cls, ch, rows, cols, val):
        for r in rows:
            for c in cols:
                W[cls, ch, r, c] += val

    R = range(4)
    mid = [1, 2]
    top = [0, 1]
    bot = [2, 3]
    left = [0, 1]
    right = [2, 3]

    # 0: central hole, vertical strokes at the sides
    s(0, 5, mid, mid, 1.5); s(0, 13, mid, mid, 1.0); s(0, 12, mid, mid, -1.0)
    s(0, 0, mid, R, 0.5); s(0, 10, R, R, 0.2); s(0, 11, R, R, 0.2)
    s(0, 1, R, R, 0.1)
    # 1: single central vertical, nothing else
    s(1, 0, R, mid, 1.0); s(1, 1, R, R, -0.7); s(1, 5, R, R, -1.0)
    s(1, 4, R, [0, 3], -0.5); s(1, 4, R, mid, 0.3)
    # 2: bottom bar, "/" through middle, curved top
    s(2, 9, bot, R, 1.0); s(2, 2, mid, R, 1.0); s(2, 8, [0], R, 0.5)
    s(2, 14, bot, R, 0.5); s(2, 5, R, R, -0.8); s(2, 0, R, R, -0.3)
    # 3: right-side vertical, upper "\", no hole
    s(3, 15, top, R, 0.7); s(3, 11, R, right, 0.7); s(3, 5, R, R, -0.8)
    s(3, 10, R, left, -0.5); s(3, 1, R, R, 0.4)
    # 4: right vertical, crossbar, "/" at upper left
    s(4, 0, R, right, 0.7); s(4, 1, mid, R, 0.7); s(4, 5, top, R, 0.5)
    s(4, 2, [0, 1, 2], left, 0.7); s(4, 9, [3], R, -0.5)
    # 5: top bar, upper-left vertical, bottom curve
    s(5, 8, [0], R, 1.0); s(5, 10, top, R, 0.7); s(5, 9, bot, R, 0.5)
    s(5, 11, bot, R, 0.5); s(5, 5, R, R, -1.0)
    # 6: left vertical, hole in lower part
    s(6, 10, [1, 2, 3], R, 0.7); s(6, 5, bot, R, 1.0); s(6, 2, top, R, 0.5)
    s(6, 11, top, R, -0.5)
    # 7: top bar, long "/" below, no hole
    s(7, 8, [0, 1], R, 1.0); s(7, 2, [1, 2, 3], R, 1.0); s(7, 5, R, R, -1.0)
    s(7, 9, [3], R, -0.7); s(7, 10, R, R, -0.3)
    # 8: two holes stacked, both diagonals through the middle
    s(8, 5, R, mid, 1.0); s(8, 2, mid, R, 0.5); s(8, 3, mid, R, 0.5)
    s(8, 12, mid, mid, 0.5)
    # 9: hole in upper part, right vertical down the lower part
    s(9, 5, top, R, 1.2); s(9, 5, bot, R, -0.7); s(9, 11, [1, 2, 3], R, 0.7)
    s(9, 10, bot, R, -0.5)

    wf = (3.0 * W).reshape(10, 256).astype(np.float32)
    bf = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2,
        "fc.weight": wf,
        "fc.bias": bf,
    }
