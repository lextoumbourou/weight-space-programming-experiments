**Step 3 plan:** the forbidden strokes in step 2 backfired. The 4x4 cells are too coarse, so the negative strokes smeared onto each digit's own strokes; 3 and 0 collapsed. I am reverting the fc templates to the step-1 baseline and moving the "what must be empty" logic into conv2, where it can work at 2-px resolution and relative to the detected structure.

Channels 8–12 of conv2 become cavity detectors built from the oriented stroke maps:

- **Closed hole:** walls on all four sides, empty centre.
- **Open-left bowl "⊃"**, **open-right bowl "⊂"**, **open-top cup "∪"**, **open-bottom cap "∩"**: three walls, with an inhibitory ray on the open side and at the centre, plus a threshold.

The fc layer adds a bonus where each digit is expected to have a given cavity type, for example 3 = ⊃ top and bottom, 5 = ⊂ top and ⊃ bottom, 4 = ∪ top, 6 = ⊂ top and hole bottom, 9 = hole top, 8 = two holes.

```python
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
    # conv2 channels 0..7: smoothed orientation maps on two staggered grids
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3          # grid A
        conv2_w[4 + k, k, 2:5, 2:5] = k3      # grid B (+2px)

    # ------------------------------------------------------------------
    # conv2 channels 8..12: cavity detectors drawn in kernel coordinates
    #   (cell units, 1 cell = 2px, centre (0,0), x right, y down)
    #   8: closed hole, 9: open-left bowl, 10: open-right bowl,
    #   11: open-top cup, 12: open-bottom cap
    # ------------------------------------------------------------------
    def karc(cx, cy, r, a0, a1, n=9):
        a = np.radians(np.linspace(a0, a1, n))
        return list(zip(cx + r * np.cos(a), cy - r * np.sin(a)))

    gy, gx = np.mgrid[-2:3, -2:3].astype(float)

    def kdep(strokes, sigma=0.6):
        # deposit wall strokes into (orientation, row, col) kernel; return kernel and total length
        P = np.zeros((4, 5, 5))
        tot = 0.0
        for w, pts in strokes:
            for a, b in zip(pts[:-1], pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                ln = math.hypot(dx, dy)
                if ln < 1e-9:
                    continue
                n = max(1, int(math.ceil(ln / 0.1)))
                th = math.atan2(-dy, dx)
                for s in range(n):
                    tt = (s + 0.5) / n
                    x = a[0] + dx * tt
                    y = a[1] + dy * tt
                    gsp = np.exp(-((gx - x) ** 2 + (gy - y) ** 2) / (2 * sigma ** 2))
                    for k in range(4):
                        r = max(0.0, math.cos(2.0 * (th - k * math.pi / 4.0)))
                        P[k] += (w * ln / n) * r * gsp
                tot += w * ln
        return P, tot

    H = 1.8   # wall distance from centre (cells)
    C = 1.2   # start of rounded corner
    TR = karc(C, -C, 0.6, 90, 0)
    BR = karc(C, C, 0.6, 0, -90)
    BL = karc(-C, C, 0.6, -90, -180)
    TL = karc(-C, -C, 0.6, 180, 90)
    cav_kernels = [
        # 0: closed hole: full ring
        ([(1.0, [(-C, -H), (C, -H)]), (1.0, TR), (1.0, [(H, -C), (H, C)]), (1.0, BR),
          (1.0, [(C, H), (-C, H)]), (1.0, BL), (1.0, [(-H, C), (-H, -C)]), (1.0, TL)],
         [(2, 2)], 0.65),
        # 1: open-left bowl: right wall + top/bottom walls, ray to the left must be empty
        ([(0.8, [(H, -C), (H, C)]), (1.0, TR), (1.0, BR),
          (0.8, [(-0.6, -H), (C, -H)]), (0.8, [(-0.6, H), (C, H)])],
         [(2, 2), (2, 1), (2, 0)], 0.55),
        # 2: open-right bowl: left wall + top/bottom walls, ray to the right must be empty
        ([(0.8, [(-H, -C), (-H, C)]), (1.0, TL), (1.0, BL),
          (0.8, [(-C, -H), (0.6, -H)]), (0.8, [(-C, H), (0.6, H)])],
         [(2, 2), (2, 3), (2, 4)], 0.55),
        # 3: open-top cup: bottom wall + side walls, ray upwards must be empty
        ([(0.8, [(-C, H), (C, H)]), (1.0, BL), (1.0, BR),
          (0.8, [(-H, -0.6), (-H, C)]), (0.8, [(H, -0.6), (H, C)])],
         [(2, 2), (1, 2), (0, 2)], 0.55),
        # 4: open-bottom cap: top wall + side walls, ray downwards must be empty
        ([(0.8, [(-C, -H), (C, -H)]), (1.0, TL), (1.0, TR),
          (0.8, [(-H, -C), (-H, 0.6)]), (0.8, [(H, -C), (H, 0.6)])],
         [(2, 2), (3, 2), (4, 2)], 0.55),
    ]
    for tp, (strokes, inhib, theta) in enumerate(cav_kernels):
        P, tot = kdep(strokes)
        # normalise by total wall length: complete pattern at typical stroke amplitude -> about 1
        conv2_w[8 + tp, 0:4] = P / (1.17 * tot)
        for (a, b) in inhib:
            conv2_w[8 + tp, 0:4, a, b] -= 0.8        # any ink here vetoes the cavity
        conv2_b[8 + tp] = -theta

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

    # Expected cavities per digit: (type, x, y, weight) in the digit's own drawing frame.
    # types: 0 hole, 1 open-left bowl, 2 open-right bowl, 3 open-top cup, 4 open-bottom cap
    cavs = {
        0: [],
        1: [],
        2: [(1, -0.05, 0.30, 0.7), (2, 0.12, 0.78, 0.7)],
        3: [(1, -0.03, 0.25, 1.0), (1, -0.03, 0.74, 1.0)],
        4: [(3, -0.08, 0.30, 1.0)],
        5: [(2, 0.05, 0.20, 1.0), (1, -0.03, 0.68, 1.0)],
        6: [(2, 0.02, 0.25, 0.8), (0, 0.0, 0.72, 1.0), (3, 0.0, 0.75, 0.4)],
        7: [(1, 0.0, 0.30, 0.5)],
        8: [(0, 0.0, 0.20, 1.0), (0, 0.0, 0.80, 1.0), (4, 0.0, 0.22, 0.4), (3, 0.0, 0.78, 0.4)],
        9: [(0, 0.0, 0.27, 1.0), (4, 0.0, 0.30, 0.6), (1, -0.02, 0.78, 0.4)],
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
        # footprint of one final cell for the smoothed orientation maps
        return np.clip((6.0 - dist) / 4.0, 0.0, 1.0)

    def footc(dist):
        # footprint of one final cell for cavity-centre positions
        return np.clip((5.0 - dist) / 3.0, 0.0, 1.0)

    centA = 7.5 + 4.0 * np.arange(4)     # pixel centres of grid A cells (also cavity cells)
    centB = 9.5 + 4.0 * np.arange(4)     # pixel centres of grid B cells

    def deposit(X, Y, TH, L):
        T = np.zeros((16, 4, 4))
        for k in range(4):
            r = np.maximum(0.0, np.cos(2.0 * (TH - k * math.pi / 4.0)))  # orientation tuning
            for g, cent in enumerate((centA, centB)):
                fy = foot(np.abs(Y[:, None] - cent[None, :]))
                fx = foot(np.abs(X[:, None] - cent[None, :]))
                T[4 * g + k] = np.einsum('n,ni,nj->ij', L * r, fy, fx) / 7.5
        return T

    # ------------------------------------------------------------------
    # fc: normalised stroke templates (channels 0..7) + cavity bonuses (channels 8..12)
    # ------------------------------------------------------------------
    ALPHA = 4.0
    GAMMA = 4.0
    class_bias = np.zeros(10)
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
        T = T / (np.linalg.norm(T) + 1e-9)
        E = np.zeros((16, 4, 4))
        for (tp, x, y, w) in cavs[d]:
            xs = x + SHEAR * (0.5 - y)
            px = min(max((xs - cx) * sc + 13.5, 7.0), 20.0)
            py = min(max((y - cy) * sc + 13.5, 7.0), 20.0)
            e = w * np.outer(footc(np.abs(py - centA)), footc(np.abs(px - centA)))
            E[8 + tp] = np.maximum(E[8 + tp], e)
        W = ALPHA * T + GAMMA * E
        fc_w[d] = W.reshape(-1).astype(np.float32)
        fc_b[d] = class_bias[d]

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
