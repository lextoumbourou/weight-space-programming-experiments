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
        # perpendicular distance of each tap from a line through the centre with direction phi
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))
        g = np.exp(-d ** 2 / 2.0)          # ridge profile (sigma = 1 px)
        g = g - g.mean()                   # zero-sum: no response to flat ink / perpendicular strokes
        g = g / g[g > 0].sum()             # ideal stroke -> response about 1
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05                 # small threshold against weak cross-talk

    # ------------------------------------------------------------------
    # conv2: channels 0..3  = orientation k, smoothed, grid A (kernel centre (2,2))
    #        channels 4..7  = orientation k, smoothed, grid B (kernel centre (3,3), i.e. +2px shift)
    #        channels 8..15 = unused (zero) in this step
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0              # long stroke through the centre -> about its pool1 value
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3
        conv2_w[4 + k, k, 2:5, 2:5] = k3

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes. Unit coordinates: x to the right, y downwards,
    # digit height = 1.  Each stroke is (weight, list of points).
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
            (0.4, [(0.2, 0.0), (-0.2, 1.0)])],                  # slanted variant
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

    SHEAR = 0.10          # typical right slant of handwriting
    BOX = 17.5            # centre-line extent in pixels (20px box minus stroke thickness)

    def sample(strokes):
        # -> arrays x, y (pixels), theta (stroke direction), weight (pixel length)
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
                    xs = x + SHEAR * (0.5 - y)          # shear
                    dxs = dx - SHEAR * dy
                    rec.append((xs, y, math.atan2(-dy, dxs), w * ln / n))
        rec = np.array(rec, dtype=float)
        X, Y, TH, L = rec[:, 0], rec[:, 1], rec[:, 2], rec[:, 3]
        ext = max(X.max() - X.min(), Y.max() - Y.min())
        sc = BOX / ext                                   # size-normalise to the 20px box
        X, Y, L = X * sc, Y * sc, L * sc
        X = X - (X * L).sum() / L.sum() + 13.5           # centre of mass -> image centre
        Y = Y - (Y * L).sum() / L.sum() + 13.5
        return X, Y, TH, L

    def foot(dist):
        # spatial footprint of one final 4x4 cell (plateau +-2px, fading out to 6px)
        return np.clip((6.0 - dist) / 4.0, 0.0, 1.0)

    centA = 7.5 + 4.0 * np.arange(4)     # pixel centres of grid A cells
    centB = 9.5 + 4.0 * np.arange(4)     # pixel centres of grid B cells

    def template(strokes):
        # draw the strokes directly in (channel, row, col) layout of the fc input
        X, Y, TH, L = sample(strokes)
        T = np.zeros((16, 4, 4))
        for k in range(4):
            r = np.maximum(0.0, np.cos(2.0 * (TH - k * math.pi / 4.0)))  # orientation tuning
            for g, cent in enumerate((centA, centB)):
                fy = foot(np.abs(Y[:, None] - cent[None, :]))
                fx = foot(np.abs(X[:, None] - cent[None, :]))
                T[4 * g + k] = np.einsum('n,ni,nj->ij', L * r, fy, fx) / 7.5
        return T

    # ------------------------------------------------------------------
    # fc: normalised templates (cosine-style matching), modest logit scale
    # ------------------------------------------------------------------
    ALPHA = 4.0
    class_bias = np.zeros(10)            # per-class offsets, to be tuned from feedback
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for d in range(10):
        T = template(digits[d]).reshape(-1)
        T = T / (np.linalg.norm(T) + 1e-9)
        fc_w[d] = (ALPHA * T).astype(np.float32)
        fc_b[d] = class_bias[d]

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
