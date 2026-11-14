import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors (channels 0..3), channels 4..7 unused
    #   channel k responds to strokes with direction angle k*45 degrees
    #   (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\")
    # ------------------------------------------------------------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    yy, xx = np.mgrid[-2:3, -2:3].astype(float)   # yy: row offset (down), xx: col offset (right)
    for k in range(4):
        phi = k * math.pi / 4.0
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))   # distance from line of direction phi
        g = np.exp(-d ** 2 / 2.0)          # ridge profile (sigma = 1 px)
        g = g - g.mean()                   # zero-sum
        g = g / g[g > 0].sum()             # ideal stroke -> response about 1
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05

    # ------------------------------------------------------------------
    # conv2: channels 0..3 = orientation k smoothed, grid A (kernel centre (2,2))
    #        channels 4..7 = orientation k smoothed, grid B (kernel centre (3,3))
    #        channels 8..15 unused
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3
        conv2_w[4 + k, k, 2:5, 2:5] = k3

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (unit coords: x right, y down, height = 1).
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=48):
        a = np.radians(np.linspace(a0, a1, n))
        return list(zip(cx + rx * np.cos(a), cy - ry * np.sin(a)))  # 90deg = top

    def eight():
        tt = np.linspace(0.0, 2.0 * math.pi, 97)
        return list(zip(0.25 * np.sin(2 * tt), 0.5 - 0.5 * np.cos(tt)))

    digits = {
        0: [(1.0, arc(0.0, 0.5, 0.33, 0.5, 0, 360, 72))],
        1: [(1.0, [(0.0, 0.0), (0.0, 1.0)]),
            (0.7, [(0.15, 0.0), (-0.15, 1.0)]),                  # slanted variants
            (0.4, [(0.30, 0.0), (-0.30, 1.0)])],
        2: [(1.0, arc(0.0, 0.27, 0.27, 0.27, 160, -30)),         # top hook
            (1.0, [(0.234, 0.405), (-0.3, 0.97)]),               # diagonal sweep
            (1.0, [(-0.3, 0.97), (0.35, 0.97)])],                # base
        3: [(1.0, arc(0.0, 0.25, 0.27, 0.25, 150, -90)),         # upper bowl
            (1.0, arc(0.0, 0.74, 0.30, 0.26, 90, -150))],        # lower bowl
        4: [(1.0, [(-0.25, 0.0), (-0.30, 0.55)]),                # left stroke
            (1.0, [(-0.30, 0.55), (0.38, 0.55)]),                # crossbar
            (1.0, [(0.12, 0.0), (0.12, 1.0)])],                  # main vertical
        5: [(1.0, [(0.30, 0.0), (-0.20, 0.0)]),                  # top bar
            (1.0, [(-0.20, 0.0), (-0.22, 0.42)]),                # short vertical
            (1.0, arc(0.0, 0.68, 0.30, 0.30, 135, -150))],       # bowl
        6: [(1.0, arc(0.30, 0.62, 0.55, 0.62, 100, 180)),        # long left curve from top
            (1.0, arc(0.0, 0.72, 0.25, 0.27, 0, 360, 60))],      # bottom loop
        7: [(1.0, [(-0.30, 0.0), (0.30, 0.0)]),                  # top bar
            (1.0, [(0.30, 0.0), (0.0, 1.0)]),                    # diagonal
            (0.25, [(-0.05, 0.5), (0.30, 0.5)])],                # optional crossbar
        8: [(1.0, eight())],
        9: [(1.0, arc(0.0, 0.27, 0.24, 0.27, 0, 360, 60)),       # top loop
            (1.0, [(0.24, 0.25), (0.20, 1.0)])],                 # stem
    }

    # Strokes each digit should NOT contain (same coordinate frame as its own drawing);
    # ink matching them counts against the class.
    forbid = {
        0: [(1.0, [(-0.15, 0.5), (0.15, 0.5)]),                  # anything in the middle
            (0.5, [(0.0, 0.3), (0.0, 0.7)]),
            (0.5, [(-0.12, 0.62), (0.12, 0.38)]),
            (0.5, [(-0.12, 0.38), (0.12, 0.62)])],
        1: [],
        2: [(1.0, [(0.30, 0.58), (0.30, 0.88)]),                 # lower-right vertical (3, 8)
            (0.7, [(-0.22, 0.22), (0.0, 0.5)])],                 # upper-left "\" (8)
        3: [(1.0, [(-0.24, 0.20), (-0.24, 0.45)]),               # upper-left vertical (5, 9, 4, 8)
            (0.5, [(-0.28, 0.50), (-0.28, 0.68)]),               # lower-left vertical (6, 8)
            (1.0, [(0.0, 0.62), (-0.25, 0.90)])],                # "/" sweep to lower-left (2)
        4: [(1.0, [(-0.20, 0.02), (0.10, 0.02)]),                # closed top (9)
            (0.7, [(-0.25, 0.98), (0.30, 0.98)]),                # base (2, 3, 8, 6)
            (0.6, [(-0.27, 0.72), (-0.27, 0.95)])],              # lower-left vertical (6, 8)
        5: [(0.8, [(0.27, 0.05), (0.27, 0.28)]),                 # upper-right vertical (3, 8, 9)
            (0.6, [(-0.27, 0.58), (-0.27, 0.75)])],              # lower-left vertical (6, 8)
        6: [(1.0, [(0.27, 0.05), (0.27, 0.33)])],                # upper-right vertical (0, 8, 9)
        7: [(1.0, [(-0.27, 0.12), (-0.27, 0.45)]),               # upper-left vertical (9, 4)
            (0.7, [(-0.30, 0.98), (0.30, 0.98)]),                # base (2, 3)
            (0.5, [(-0.28, 0.52), (-0.08, 0.52)])],              # loop bottom on the left (9)
        8: [],
        9: [(1.0, [(-0.25, 0.68), (-0.25, 0.92)]),               # lower-left vertical (6, 8, 0)
            (0.4, [(-0.25, 0.98), (0.05, 0.98)])],               # base on the left (2, 3)
    }

    SHEAR = 0.10          # typical right slant of handwriting
    BOX = 17.5            # centre-line extent in pixels (20px box minus stroke thickness)

    def raw(strokes):
        # sample strokes -> rows (x_sheared, y, theta, weighted length), unit coordinates
        rec = []
        for w, pts in strokes:
            for a, b in zip(pts[:-1], pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                ln = math.hypot(dx, dy)
                if ln < 1e-9:
                    continue
                n = max(1, int(math.ceil(ln / 0.02)))
                for s in range(n):
                    tt = (s + 0.5) / n
                    x = a[0] + dx * tt
                    y = a[1] + dy * tt
                    rec.append((x + SHEAR * (0.5 - y), y,
                                math.atan2(-dy, dx - SHEAR * dy), w * ln / n))
        return np.array(rec, dtype=float).reshape(-1, 4)

    def foot(dist):
        # spatial footprint of one final 4x4 cell (plateau +-2px, fading out to 6px)
        return np.clip((6.0 - dist) / 4.0, 0.0, 1.0)

    centA = 7.5 + 4.0 * np.arange(4)     # pixel centres of grid A cells
    centB = 9.5 + 4.0 * np.arange(4)     # pixel centres of grid B cells

    def deposit(X, Y, TH, L):
        # draw stroke samples directly into the (channel, row, col) layout of the fc input
        T = np.zeros((16, 4, 4))
        if len(X) == 0:
            return T
        for k in range(4):
            # orientation tuning of the line filters (about 25% leak at 45 degrees off)
            r = np.maximum(0.0, (np.cos(2.0 * (TH - k * math.pi / 4.0)) + 0.33) / 1.33)
            for g, cent in enumerate((centA, centB)):
                fy = foot(np.abs(Y[:, None] - cent[None, :]))
                fx = foot(np.abs(X[:, None] - cent[None, :]))
                T[4 * g + k] = np.einsum('n,ni,nj->ij', L * r, fy, fx) / 7.5
        return T

    # ------------------------------------------------------------------
    # fc: normalised templates with forbidden-stroke penalties
    # ------------------------------------------------------------------
    ALPHA = 4.0
    LAMBDA = 0.8                          # strength of forbidden strokes
    class_bias = np.array([0.0, 0.0, 0.4, -0.5, 0.4, 0.0, -0.4, 0.0, -0.6, -0.3])
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for d in range(10):
        P = raw(digits[d])
        ext = max(P[:, 0].max() - P[:, 0].min(), P[:, 1].max() - P[:, 1].min())
        sc = BOX / ext                                    # size-normalise to the 20px box
        cx = (P[:, 0] * P[:, 3]).sum() / P[:, 3].sum()    # centre of mass -> image centre
        cy = (P[:, 1] * P[:, 3]).sum() / P[:, 3].sum()
        T = deposit((P[:, 0] - cx) * sc + 13.5, (P[:, 1] - cy) * sc + 13.5,
                    P[:, 2], P[:, 3] * sc)
        Q = raw(forbid[d])
        N = deposit((Q[:, 0] - cx) * sc + 13.5, (Q[:, 1] - cy) * sc + 13.5,
                    Q[:, 2], Q[:, 3] * sc)
        nrm = np.linalg.norm(T) + 1e-9
        W = (T - LAMBDA * N) / nrm
        fc_w[d] = (ALPHA * W.reshape(-1)).astype(np.float32)
        fc_b[d] = class_bias[d]

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
