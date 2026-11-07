## Step 5 results

Step 5 did not help: loss 0.964, accuracy 68.5%. Broadening the orientation tuning only moved errors between classes (for example 6 → 4 went up to 304). I think the real limit is the conv1 detectors themselves.

## Diagnosis: thick strokes vanish

The zero-mean ridge kernel has flanks of about −0.36 at ±2 px from its centre line. I worked out its response to strokes of different widths, aligned with the detector:

| Stroke width | Response |
|---|---|
| 3 px | ≈ 1 |
| 4 px | ≈ 0.5 |
| 5 px | ≈ 0 |

Many MNIST digits are drawn with 3–5 px strokes. So thick digits produce weak or missing features.

## Step 6 change: edge detectors instead of line detectors

A step edge looks the same whatever the stroke width, so edge detectors avoid this problem.

- **conv1 (all 8 channels):** 4 edge orientations × 2 polarities. Each kernel is antisymmetric across the edge with weights [−0.4, −0.6, 0, 0.6, 0.4], scaled so a 0→1 step gives about 1. The bias is −0.15.
- **conv2:** each routed channel adds the + and − polarity of the same orientation with weight 0.5 each. This gives the rectified edge strength |∂I/∂n| for that orientation, with the same 4-offset routing as before, so the 6×6×4 feature grid keeps the same meaning.
- **Templates:** each stroke counts as edges along its own direction. Orientation tuning is set to ((1 + cos 2Δ)/2)³, between the two earlier settings.
- **Scale and biases:** amplitude A = 0.6 and γ = 4.5. The class corrections go back to the step-4 values, which belonged to the best configuration so far.

## Code

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 oriented EDGE detectors (4 orientations x 2 polarities) ----
    # theta = edge direction: 0 horizontal edge, 45 "\", 90 vertical edge, 135 "/"
    # signed perpendicular coordinate t = v*cos(theta) - u*sin(theta)  (v=row, u=col offset)
    # channel 2*o   : +edge (ink on +t side)
    # channel 2*o+1 : -edge (ink on -t side)
    thetas = [0.0, 45.0, 90.0, 135.0]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)
    for o, th in enumerate(thetas):
        t0 = math.radians(th)
        k = np.zeros((5, 5))
        for v in range(-2, 3):
            for u in range(-2, 3):
                t = v * math.cos(t0) - u * math.sin(t0)
                # antisymmetric profile: ~0.6 at |t|=1, ~0.4 at |t|=2, 0 at centre
                if abs(t) < 0.3:
                    w = 0.0
                else:
                    w = math.copysign(min(abs(t), 2.5) * math.exp(-(abs(t) - 1.0) ** 2 / 2.0), t)
                k[v + 2, u + 2] = w
        k /= k[k > 0].sum()          # ideal step edge -> ~1
        conv1_w[2 * o, 0] = k
        conv1_w[2 * o + 1, 0] = -k
        conv1_b[2 * o] = -0.15
        conv1_b[2 * o + 1] = -0.15

    # ---------------- conv2: routing taps, |edge| = 0.5*(+edge) + 0.5*(-edge) ----------
    # channel o*4+k = orientation o at offset k; after pool2 -> 6x6 bin grid
    offsets = [(0, 0), (0, 4), (4, 0), (4, 4)]
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros((16,), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            conv2_w[o * 4 + k, 2 * o, oy, ox] = 0.5
            conv2_w[o * 4 + k, 2 * o + 1, oy, ox] = 0.5

    # ---------------- hand-drawn digit strokes ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n),
                 cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]

    strokes = {
        0: [ellipse(0, 0, 0.8, 1.0)],
        1: [[(0.1, -1), (-0.1, 1)]],
        2: [[(-0.65, -0.6), (-0.4, -0.92), (0.05, -1), (0.5, -0.85), (0.65, -0.5),
             (0.45, -0.05), (-0.1, 0.5), (-0.7, 1), (0.0, 0.95), (0.8, 1)]],
        3: [[(-0.6, -0.85), (0, -1), (0.55, -0.85), (0.6, -0.4), (0.05, -0.05), (-0.25, -0.05)],
            [(0.05, -0.05), (0.6, 0.25), (0.65, 0.7), (0.1, 1), (-0.65, 0.85)]],
        4: [[(-0.45, -0.9), (-0.6, 0.2), (0.75, 0.2)],
            [(0.35, -0.9), (0.3, 1)]],
        5: [[(0.7, -1), (-0.45, -1), (-0.6, -0.15), (0, -0.3), (0.6, -0.05),
             (0.7, 0.45), (0.4, 0.9), (0, 1), (-0.65, 0.85)]],
        6: [[(0.5, -1), (-0.1, -0.6), (-0.55, 0), (-0.6, 0.5), (-0.3, 0.95), (0.2, 1),
             (0.6, 0.65), (0.55, 0.2), (0.1, -0.05), (-0.3, 0.05), (-0.55, 0.35)]],
        7: [[(-0.7, -0.95), (0.75, -1), (0.4, -0.3), (0.05, 1)]],
        8: [ellipse(0.05, -0.5, 0.5, 0.5), ellipse(0, 0.5, 0.65, 0.5)],
        9: [ellipse(0, -0.45, 0.65, 0.5), [(0.62, -0.5), (0.45, 1)]],
    }

    centers = np.array([4 * b + 3.5 for b in range(6)])   # bin centres (input px)
    sp = 2.5
    A, C0 = 0.6, 3.0

    MU = np.zeros((10, 4, 6, 6))
    for d in range(10):
        samples = []
        for poly in strokes[d]:
            pts = [(14 + 10.0 * y, 14 + 8.0 * x - 1.5 * y) for (x, y) in poly]
            for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
                L = math.hypot(r1 - r0, c1 - c0)
                if L < 1e-6:
                    continue
                phi = math.atan2(r1 - r0, c1 - c0)
                n = max(1, int(L / 0.5))
                for s in range(n):
                    a = (s + 0.5) / n
                    samples.append((r0 + a * (r1 - r0), c0 + a * (c1 - c0), L / n, phi))
        wsum = sum(s[2] for s in samples)
        mr = sum(s[0] * s[2] for s in samples) / wsum
        mc = sum(s[1] * s[2] for s in samples) / wsum
        C = np.zeros((4, 6, 6))
        for (r, c, w, phi) in samples:
            r += 14 - mr
            c += 14 - mc
            ow = [((1 + math.cos(2 * (phi - math.radians(th)))) / 2) ** 3 for th in thetas]
            gr = np.exp(-(centers - r) ** 2 / (2 * sp * sp))
            gc = np.exp(-(centers - c) ** 2 / (2 * sp * sp))
            g = np.outer(gr, gc) * w
            for o in range(4):
                C[o] += ow[o] * g
        MU[d] = A * (1 - np.exp(-C / C0))

    # ---------------- fc: nearest-centroid scoring + class corrections ----------------
    gamma = 4.5
    cnt = np.array([1, 1, 2, 2, 1, 1], dtype=float)
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            ch = o * 4 + k
            for i in range(4):
                for j in range(4):
                    br, bc = i + oy // 2, j + ox // 2
                    fc_w[:, ch * 16 + i * 4 + j] = gamma * MU[:, o, br, bc] / (cnt[br] * cnt[bc])
    fc_b = -0.5 * gamma * (MU ** 2).reshape(10, -1).sum(axis=1)
    corr = np.array([0.14, -0.27, 0.54, -0.23, 0.78, 0.13, -0.04, -0.22, 0.38, -0.25])
    fc_b = (fc_b + corr).astype(np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
