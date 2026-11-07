## Step 1 plan

I hand-build a stroke-orientation feature extractor and attach a template-matching classifier to it.

**conv1: oriented line detectors.** Four channels detect lines at 0°, 45°, 90° and 135°. Each 5×5 ridge kernel has a Gaussian profile across the line and is made zero-mean, so flat ink or background gives 0. The positive weights sum to 1, so a well-aligned stroke gives about 1. A small negative bias (−0.15) removes weak responses. The other 4 channels are left at zero.

**conv2: routing only.** Each of the 16 channels is one copy of an orientation map, shifted by (0 or 4, 0 or 4) pool1 pixels. Each kernel has a single weight of 1. After the second max-pool, the 256 features hold a clean 6×6 grid for each orientation.
- Grid cell (b_r, b_c) is the maximum line response over input centres in rows 4b_r+2..4b_r+5 and columns 4b_c+2..4b_c+5.
- Grid rows and columns 2–3 appear twice, once from each offset copy. The fc layer divides by this count.

**fc: hand-drawn templates.** I describe each digit as polylines and ellipses in a normalised box.
- I turn those strokes directly into an expected (orientation × 6×6) occupancy map. Each stroke is softly assigned to orientations and smeared spatially with a Gaussian. Nothing is passed through the network.
- Each template is L2-normalised, the mean template is subtracted, and the result is scaled.

## Code

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    # orientation angles theta (degrees); line direction in (row, col) = (sin t, cos t)
    #   0 -> horizontal, 45 -> "\" , 90 -> vertical, 135 -> "/"
    thetas = [0.0, 45.0, 90.0, 135.0]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)
    sig = 1.0
    for o, th in enumerate(thetas):
        t = math.radians(th)
        dr, dc = math.sin(t), math.cos(t)
        k = np.zeros((5, 5))
        for v in range(-2, 3):          # row offset
            for u in range(-2, 3):      # col offset
                d = abs(v * dc - u * dr)  # perpendicular distance to the line
                k[v + 2, u + 2] = math.exp(-d * d / (2 * sig * sig))
        k -= k.mean()                   # zero-mean: flat ink -> 0
        k /= k[k > 0].sum()             # aligned stroke -> ~1
        conv1_w[o, 0] = k
        conv1_b[o] = -0.15              # suppress weak responses
    # channels 4..7 unused (all zero -> output 0)

    # ---------------- conv2: routing taps ----------------
    # channel ch = o*4 + k, offset k -> (oy, ox) in {0,4}^2 ; single tap weight 1
    offsets = [(0, 0), (0, 4), (4, 0), (4, 4)]
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros((16,), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            conv2_w[o * 4 + k, o, oy, ox] = 1.0

    # ---------------- digit stroke descriptions ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n),
                 cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]

    # normalised coords: x right in [-1,1], y down in [-1,1]
    strokes = {
        0: [ellipse(0, 0, 0.75, 1.0)],
        1: [[(0.15, -1), (-0.15, 1)]],
        2: [[(-0.7, -0.55), (-0.45, -0.9), (0, -1), (0.45, -0.9), (0.7, -0.55),
             (0.55, -0.1), (-0.75, 1), (0.8, 1)]],
        3: [[(-0.6, -0.85), (0, -1), (0.55, -0.85), (0.6, -0.4), (0.05, -0.05), (-0.25, -0.05)],
            [(0.05, -0.05), (0.6, 0.25), (0.65, 0.7), (0.1, 1), (-0.65, 0.85)]],
        4: [[(-0.3, -1), (-0.75, 0.3), (0.8, 0.3)],
            [(0.45, -0.8), (0.4, 1)]],
        5: [[(0.7, -1), (-0.45, -1), (-0.6, -0.15), (0, -0.3), (0.6, -0.05),
             (0.7, 0.45), (0.4, 0.9), (0, 1), (-0.65, 0.85)]],
        6: [[(0.5, -1), (-0.1, -0.6), (-0.55, 0), (-0.6, 0.5), (-0.3, 0.95), (0.2, 1),
             (0.6, 0.65), (0.55, 0.2), (0.1, -0.05), (-0.3, 0.05), (-0.55, 0.35)]],
        7: [[(-0.7, -1), (0.75, -1), (0.35, -0.2), (0, 1)]],
        8: [ellipse(0, -0.5, 0.55, 0.5), ellipse(0, 0.5, 0.65, 0.5)],
        9: [ellipse(0, -0.45, 0.6, 0.5), [(0.6, -0.45), (0.35, 1)]],
    }

    # ---------------- templates in (orientation, 6x6 bin) space ----------------
    centers = np.array([4 * b + 3.5 for b in range(6)])  # bin centres in input pixels
    sp = 2.0                                             # spatial smear
    T = np.zeros((10, 4, 6, 6))
    for d in range(10):
        for poly in strokes[d]:
            pts = [(14 + 9.5 * y, 14 + 7.0 * x) for (x, y) in poly]  # (row, col)
            for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
                L = math.hypot(r1 - r0, c1 - c0)
                if L < 1e-6:
                    continue
                phi = math.atan2(r1 - r0, c1 - c0)
                ow = [max(0.0, math.cos(2 * (phi - math.radians(th)))) ** 2 for th in thetas]
                n = max(1, int(L / 0.5))
                for s in range(n):
                    a = (s + 0.5) / n
                    r = r0 + a * (r1 - r0)
                    c = c0 + a * (c1 - c0)
                    gr = np.exp(-(centers - r) ** 2 / (2 * sp * sp))
                    gc = np.exp(-(centers - c) ** 2 / (2 * sp * sp))
                    g = np.outer(gr, gc) * (L / n)
                    for o in range(4):
                        T[d, o] += ow[o] * g
    for d in range(10):
        T[d] /= np.linalg.norm(T[d]) + 1e-9
    W = T - T.mean(axis=0, keepdims=True)   # discriminative part of each template

    # ---------------- fc: map 6x6 bins onto the 256 duplicated features ----------------
    cnt = np.array([1, 1, 2, 2, 1, 1], dtype=float)   # how often each bin row/col appears
    scale = 5.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros((10,), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            ch = o * 4 + k
            for i in range(4):
                for j in range(4):
                    br, bc = i + oy // 2, j + ox // 2
                    idx = ch * 16 + i * 4 + j
                    fc_w[:, idx] = scale * W[:, o, br, bc] / (cnt[br] * cnt[bc])

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
