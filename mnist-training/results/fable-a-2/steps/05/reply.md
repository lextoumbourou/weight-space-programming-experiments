**Step 5 plan:** the probe shows straight strokes give a pooled line response of about 1.0, so amplitude was not the problem. The cavity detectors in step 3 failed because they summed several walls against a threshold. That breaks when straight walls respond strongly and curved loops weakly.

This step replaces them with features that depend on only one or two walls plus a hard veto:

- **conv1 channels 4–7:** polarity edge detectors (ink to the right, left, below, above). These have a much more uniform amplitude than line detectors and mark which side of a stroke is empty.
- **conv2 channels 8–13:** "characteristic loci" of background points.
  - Wall on one side and the opposite side clear: right-wall/left-open, left-wall/right-open, floor/open-above, ceiling/open-below. Any ink on the open ray or at the centre vetoes the response.
  - Walls on both sides: left and right, or above and below.
- **fc:** the step-1 stroke templates, plus hand-described segments per digit where each locus type should occur. The loci templates are normalised the same way as the stroke templates.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1
    #   channels 0..3: oriented line detectors (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\")
    #   channels 4..7: polarity edge detectors
    #       4: ink to the RIGHT of the edge   5: ink to the LEFT
    #       6: ink BELOW the edge             7: ink ABOVE
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
    c = np.array([-0.5, -1.0, 0.0, 1.0, 0.5])   # derivative profile across the edge
    r = np.array([0.5, 1.0, 1.0, 1.0, 0.5])     # smoothing along the edge
    conv1_w[4, 0] = np.outer(r, c) / 6.0        # ink right
    conv1_w[5, 0] = -np.outer(r, c) / 6.0       # ink left
    conv1_w[6, 0] = np.outer(c, r) / 6.0        # ink below
    conv1_w[7, 0] = -np.outer(c, r) / 6.0       # ink above
    conv1_b[4:8] = -0.1

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
    # conv2 channels 8..13: "characteristic loci" of background points.
    # The kernel centre (2,2) is the background point p; rays go 2 cells (about 5px) out.
    #   8 : wall on the right, left ray open        9 : wall on the left, right ray open
    #   10: floor below, ray upwards open           11: ceiling above, ray downwards open
    #   12: walls left AND right                    13: walls above AND below
    # A "wall" is an inward-facing polarity edge; "open" = any ink on the ray vetoes.
    # ------------------------------------------------------------------
    lat = (0.25, 0.5, 0.25)     # lateral smoothing across the ray
    KINH = 1.5                  # veto strength

    def block_R(ch):
        for a, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 4, a, 3] += wl
            conv2_w[ch, 4, a, 4] += wl

    def block_L(ch):
        for a, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 5, a, 0] += wl
            conv2_w[ch, 5, a, 1] += wl

    def block_D(ch):
        for b, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 6, 3, b] += wl
            conv2_w[ch, 6, 4, b] += wl

    def block_U(ch):
        for b, wl in zip((1, 2, 3), lat):
            conv2_w[ch, 7, 0, b] += wl
            conv2_w[ch, 7, 1, b] += wl

    def inhibit(ch, cells, exclude=()):
        for (a, b) in cells:
            for cc in range(8):
                if cc not in exclude:
                    conv2_w[ch, cc, a, b] -= KINH

    block_R(8);  inhibit(8, [(2, 0), (2, 1)]);  inhibit(8, [(2, 2)], exclude=(4,))
    block_L(9);  inhibit(9, [(2, 3), (2, 4)]);  inhibit(9, [(2, 2)], exclude=(5,))
    block_D(10); inhibit(10, [(0, 2), (1, 2)]); inhibit(10, [(2, 2)], exclude=(6,))
    block_U(11); inhibit(11, [(3, 2), (4, 2)]); inhibit(11, [(2, 2)], exclude=(7,))
    conv2_b[8:12] = -0.4
    block_L(12); block_R(12); inhibit(12, [(2, 2)], exclude=(4, 5))
    block_U(13); block_D(13); inhibit(13, [(2, 2)], exclude=(6, 7))
    conv2_b[12:14] = -1.8       # one wall alone must not be enough

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

    # Where each locus type is expected, as segments in the digit's own drawing frame:
    # (type, weight, start, end); types: 0 wallR/openL, 1 wallL/openR, 2 floor/openUp,
    # 3 ceiling/openDown, 4 walls left+right, 5 walls above+below
    loci = {
        0: [(4, 1.0, (0.0, 0.2), (0.0, 0.8)),            # inside the ring
            (2, 0.8, (-0.12, 0.8), (0.12, 0.8)),         # inside, above the bottom
            (3, 0.8, (-0.12, 0.2), (0.12, 0.2))],        # inside, below the top
        1: [(0, 1.0, (-0.2, 0.1), (-0.2, 0.9)),          # left of the stroke
            (1, 1.0, (0.2, 0.1), (0.2, 0.9))],           # right of the stroke
        2: [(0, 0.8, (-0.02, 0.2), (-0.02, 0.35)),       # under the hook
            (3, 0.8, (-0.12, 0.3), (0.08, 0.3)),
            (1, 0.8, (0.15, 0.68), (0.15, 0.82)),        # wedge between diagonal and base
            (2, 0.8, (0.1, 0.78), (0.32, 0.78))],
        3: [(0, 1.0, (-0.02, 0.12), (-0.02, 0.88)),      # both bowls open to the left
            (5, 0.8, (-0.05, 0.25), (0.1, 0.25)),
            (5, 0.8, (-0.05, 0.74), (0.1, 0.74))],
        4: [(4, 1.0, (-0.08, 0.05), (-0.08, 0.4)),       # inside the open cup
            (2, 1.0, (-0.15, 0.33), (0.0, 0.33)),
            (0, 0.8, (-0.08, 0.65), (-0.08, 0.95)),      # below bar, left of stem
            (3, 0.8, (-0.25, 0.75), (-0.02, 0.75)),
            (1, 0.8, (0.3, 0.05), (0.3, 0.4)),           # right of stem
            (1, 0.8, (0.3, 0.65), (0.3, 0.95))],
        5: [(1, 1.0, (0.02, 0.1), (0.02, 0.3)),          # upper cavity opens right
            (5, 0.6, (0.05, 0.19), (0.2, 0.19)),
            (0, 1.0, (0.02, 0.55), (0.02, 0.82)),        # bowl opens left
            (5, 0.6, (-0.05, 0.68), (0.1, 0.68))],
        6: [(1, 1.0, (0.03, 0.12), (0.03, 0.38)),        # upper cavity opens right
            (4, 1.0, (0.0, 0.65), (0.0, 0.8)),           # loop
            (5, 1.0, (-0.05, 0.72), (0.05, 0.72))],
        7: [(0, 1.0, (0.03, 0.15), (-0.2, 0.9)),         # left of the diagonal
            (3, 0.8, (-0.25, 0.22), (0.05, 0.22)),       # under the bar
            (1, 0.7, (0.42, 0.25), (0.2, 0.9))],         # right of the diagonal
        8: [(4, 1.0, (0.0, 0.15), (0.0, 0.3)),           # upper loop
            (5, 1.0, (-0.05, 0.22), (0.05, 0.22)),
            (4, 1.0, (0.0, 0.7), (0.0, 0.85)),           # lower loop
            (5, 1.0, (-0.05, 0.78), (0.05, 0.78)),
            (0, 0.6, (-0.22, 0.45), (-0.22, 0.55)),      # waist notches
            (1, 0.6, (0.22, 0.45), (0.22, 0.55))],
        9: [(4, 1.0, (0.0, 0.2), (0.0, 0.35)),           # loop
            (5, 1.0, (-0.05, 0.27), (0.05, 0.27)),
            (0, 1.0, (0.0, 0.65), (0.0, 0.95)),          # left of stem, below loop
            (3, 0.8, (-0.2, 0.72), (0.05, 0.72)),
            (1, 0.7, (0.42, 0.3), (0.4, 0.9))],          # right of stem
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
        # footprint of one final cell for locus-centre positions
        return np.clip((5.0 - dist) / 3.0, 0.0, 1.0)

    centA = 7.5 + 4.0 * np.arange(4)     # pixel centres of grid A cells (also locus cells)
    centB = 9.5 + 4.0 * np.arange(4)     # pixel centres of grid B cells

    def deposit(X, Y, TH, L):
        T = np.zeros((16, 4, 4))
        for k in range(4):
            rr = np.maximum(0.0, np.cos(2.0 * (TH - k * math.pi / 4.0)))  # orientation tuning
            for g, cent in enumerate((centA, centB)):
                fy = foot(np.abs(Y[:, None] - cent[None, :]))
                fx = foot(np.abs(X[:, None] - cent[None, :]))
                T[4 * g + k] = np.einsum('n,ni,nj->ij', L * rr, fy, fx) / 7.5
        return T

    # ------------------------------------------------------------------
    # fc: normalised stroke templates (channels 0..7) + normalised loci templates (8..13)
    # ------------------------------------------------------------------
    ALPHA = 4.0
    GAMMA = 3.0
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
        for (tp, w, p0, p1) in loci[d]:
            for s in np.linspace(0.0, 1.0, 9):
                x = p0[0] + s * (p1[0] - p0[0])
                y = p0[1] + s * (p1[1] - p0[1])
                xs = x + SHEAR * (0.5 - y)
                px = min(max((xs - cx) * sc + 13.5, 6.5), 20.5)   # valid range of conv2 centres
                py = min(max((y - cy) * sc + 13.5, 6.5), 20.5)
                e = w * np.outer(footc(np.abs(py - centA)), footc(np.abs(px - centA)))
                E[8 + tp] = np.maximum(E[8 + tp], e)
        E = E / (np.linalg.norm(E) + 1e-9)

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
