**Step 9 approach:** biases on the clean network helped (0.7293), so I am keeping that base and making a few changes:

- **Biases:** nudged further in the same direction (4 up, 9 down), with 1 and 6 eased back to offset the changes below.
- **1 shape:** the slanted-1 variant goes back in at reduced weight, since slanted 1s still go to 2 and 7.
- **Negatives:** a small set of correct-direction negatives at modest strength, each drawn into the class that wrongly attracts other digits and placed well away from that class's own strokes:
  - 6: upper right (against 0) and top bar (against 5).
  - 9: bar right of the stem (against 4) and lower left (against 8 and 2).
  - 5: upper right (against 3).
  - 3: the "/" diagonal in the lower part (against 2).
  - 2: lower-right side (against 8).
  - 7: upper left (against 9).

```python
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
        0: [(1.0, arc(0.5, 0.5, 0.30, 0.50, 0, 360))],
        1: [(1.0, [(0.5, 0.0), (0.5, 1.0)]),
            (0.5, [(0.70, 0.0), (0.30, 1.0)])],          # more slanted way of writing 1
        2: [(1.0, arc(0.5, 0.27, 0.25, 0.25, 190, 400) + [(0.22, 0.95)]),
            (1.0, [(0.22, 0.95), (0.82, 0.95)])],
        3: [(1.0, arc(0.45, 0.26, 0.25, 0.24, 200, 450)),
            (1.0, arc(0.45, 0.74, 0.28, 0.24, 270, 520))],
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
        8: [(1.0, arc(0.5, 0.26, 0.21, 0.24, 0, 360)),
            (1.0, arc(0.5, 0.74, 0.25, 0.25, 0, 360))],
        9: [(1.0, arc(0.45, 0.27, 0.22, 0.24, 0, 360)),
            (1.0, [(0.67, 0.20), (0.66, 0.60), (0.60, 0.98)])],
    }
    # negative strokes drawn into class Y, at places where a digit X that gets
    # mistaken for Y has ink but Y itself has none.
    #  'all' = any ink here counts against Y;  'ori' = a stroke of this direction counts against Y
    negs = {
        0: [],
        1: [],
        2: [('all', [(0.78, 0.55), (0.78, 0.72)])],               # 8 / 3 have a lower-right side
        3: [('ori', [(0.25, 0.86), (0.50, 0.62)])],               # 2 has a "/" diagonal down to the base
        4: [],
        5: [('all', [(0.76, 0.25), (0.76, 0.40)])],               # 3 has an upper-right side
        6: [('all', [(0.85, 0.20), (0.85, 0.45)]),                # 0 has an upper-right side
            ('ori', [(0.50, 0.03), (0.82, 0.03)])],               # 5 has a top bar
        7: [('all', [(0.22, 0.22), (0.22, 0.42)])],               # 9 has a loop on the upper left
        8: [],
        9: [('ori', [(0.78, 0.58), (0.94, 0.58)]),                # 4's bar sticks out right of the stem
            ('all', [(0.22, 0.68), (0.22, 0.90)])],               # 8 / 2 have ink lower-left
    }
    shear = 0.10       # typical right-leaning slant of handwriting
    sigma = 2.5        # blur (pixels) of the template windows
    centres = 6.5 + 2.0 * np.arange(8)   # window centres in input pixels

    alpha = 8.0        # logit scale
    pen = 0.02         # general penalty for strokes where the digit has no ink
    gamma = 0.5        # fraction of the template mean that is subtracted
    kappa = 0.08       # strength of the explicit negative strokes

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
        return max(0.0, math.cos(2.0 * (th - k * math.pi / 4.0)))

    fc_w = np.zeros((10, 256), dtype=np.float32)
    # per-class biases tuned from the confusion matrices (4 under-predicted, 9 / 6 over-predicted)
    fc_b = np.array([0.1, 0.0, 0.1, 0.0, 0.9, 0.2, -0.4, -0.2, 0.2, -0.6], dtype=np.float32)

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

        # draw the negative strokes
        N = np.zeros((4, 8, 8))
        for (kind, poly) in negs[d]:
            for (cx, cy, th, w) in sample(poly, 1.0):
                g = window(cx + sx, cy + sy) * w
                for k in range(4):
                    if kind == 'all':
                        N[k] += 0.7 * g
                    else:
                        N[k] += tune(th, k) * g
        N = np.tanh(N / 4.0)

        Wd = T / np.sqrt((T ** 2).sum()) - pen * (1.0 - ink)[None, :, :]
        Wd -= gamma * Wd.mean()                   # partial centring: balance broad vs narrow digits
        Wd -= kappa * N                           # targeted "X has ink here, Y does not" evidence
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
```
