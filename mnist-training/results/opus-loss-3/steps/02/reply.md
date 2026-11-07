## Step 2 plan

Step 1 reached 54.6% accuracy. The predictions are lopsided: 8, 6 and 9 are predicted far too often (2170, 1360 and 1406 times), while 7, 5 and 4 are predicted far too rarely (163, 413 and 433 times).

This step changes only the fc biases. Everything else stays the same, so the effect of the biases can be measured on its own.
- Each bias is −0.8 × log(times predicted / times true).
- The true counts are the MNIST test-set class counts, which I assume the validation set matches.
- The factor 0.8 is a partial step, to avoid overshooting.

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
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            ch = o * 4 + k
            for i in range(4):
                for j in range(4):
                    br, bc = i + oy // 2, j + ox // 2
                    idx = ch * 16 + i * 4 + j
                    fc_w[:, idx] = scale * W[:, o, br, bc] / (cnt[br] * cnt[bc])

    # class biases: -0.8*log(predicted/true) from step-1 confusion matrix
    fc_b = np.array([-0.05, 0.15, -0.035, 0.016, 0.655,
                     0.616, -0.28, 1.47, -0.64, -0.266], dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
