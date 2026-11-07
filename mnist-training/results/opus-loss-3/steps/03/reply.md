## Step 3 plan

Step 2's per-class bias fix gave only a small gain, so the main limit is how the classifier scores templates. This step replaces that scoring.

**Scoring rule: nearest centroid.** Each template now estimates the expected feature value μ_d[o, b] for a digit, where o is the orientation and b is the 6×6 cell. The logit is a Euclidean nearest-centroid score:

logit_d = γ · (μ_d·f − ½‖μ_d‖²)

This is −γ/2 · ‖f − μ_d‖² plus a term that is the same for every class. It therefore penalises ink where the template expects none and removes the advantage that big templates such as 8 had before.

**Expected feature values.** Each μ value is the saturated stroke coverage, 0.7 · (1 − e^(−C/3)), where C is the accumulated stroke coverage. The spatial blur is wider (σ = 2.5) to stand in for variation between writers.

**Better geometry.**
- Digits are wider: the x scale goes from 7 to 8 px.
- A rightward slant typical of MNIST is added.
- Each drawn template is shifted so its own centre of mass sits at (14, 14), as MNIST does. This is computed from my drawing alone, not from network outputs.
- The 2, 4, 7 and 9 shapes are refined.

Biases are reset to 0, because the new templates change the class balance.

## Code

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    # theta: 0 horizontal, 45 "\", 90 vertical, 135 "/"; line dir (row,col)=(sin,cos)
    thetas = [0.0, 45.0, 90.0, 135.0]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)
    sig = 1.0
    for o, th in enumerate(thetas):
        t = math.radians(th)
        dr, dc = math.sin(t), math.cos(t)
        k = np.zeros((5, 5))
        for v in range(-2, 3):
            for u in range(-2, 3):
                d = abs(v * dc - u * dr)          # distance from line through centre
                k[v + 2, u + 2] = math.exp(-d * d / (2 * sig * sig))
        k -= k.mean()                             # zero mean
        k /= k[k > 0].sum()                       # aligned stroke -> ~1
        conv1_w[o, 0] = k
        conv1_b[o] = -0.15
    # channels 4..7 unused

    # ---------------- conv2: routing taps ----------------
    # channel o*4+k = orientation o shifted by offset k; after pool2 -> 6x6 bin grid
    offsets = [(0, 0), (0, 4), (4, 0), (4, 4)]
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros((16,), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            conv2_w[o * 4 + k, o, oy, ox] = 1.0

    # ---------------- hand-drawn digit strokes ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n),
                 cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]

    # normalised coords: x right, y down, box [-1,1]^2
    strokes = {
        0: [ellipse(0, 0, 0.8, 1.0)],
        1: [[(0.1, -1), (-0.1, 1)]],
        2: [[(-0.65, -0.6), (-0.4, -0.92), (0.05, -1), (0.5, -0.85), (0.65, -0.5),
             (0.45, -0.05), (-0.1, 0.5), (-0.7, 1), (0.0, 0.95), (0.8, 1)]],
        3: [[(-0.6, -0.85), (0, -1), (0.55, -0.85), (0.6, -0.4), (0.05, -0.05), (-0.25, -0.05)],
            [(0.05, -0.05), (0.6, 0.25), (0.65, 0.7), (0.1, 1), (-0.65, 0.85)]],
        4: [[(-0.35, -1), (-0.65, 0.25), (0.8, 0.25)],
            [(0.45, -1), (0.4, 1)]],
        5: [[(0.7, -1), (-0.45, -1), (-0.6, -0.15), (0, -0.3), (0.6, -0.05),
             (0.7, 0.45), (0.4, 0.9), (0, 1), (-0.65, 0.85)]],
        6: [[(0.5, -1), (-0.1, -0.6), (-0.55, 0), (-0.6, 0.5), (-0.3, 0.95), (0.2, 1),
             (0.6, 0.65), (0.55, 0.2), (0.1, -0.05), (-0.3, 0.05), (-0.55, 0.35)]],
        7: [[(-0.7, -0.95), (0.75, -1), (0.4, -0.3), (0.05, 1)]],
        8: [ellipse(0.05, -0.5, 0.5, 0.5), ellipse(0, 0.5, 0.65, 0.5)],
        9: [ellipse(0, -0.45, 0.65, 0.5), [(0.62, -0.5), (0.45, 1)]],
    }

    centers = np.array([4 * b + 3.5 for b in range(6)])   # bin centres (input px)
    sp = 2.5                                              # spatial blur ~ writer variation
    A, C0 = 0.7, 3.0                                      # saturation: mu = A*(1-exp(-C/C0))

    MU = np.zeros((10, 4, 6, 6))
    for d in range(10):
        # sample points along strokes in pixel coords (with slant), with orientation
        samples = []   # (row, col, weight, phi)
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
        # shift drawing so its centre of mass is at (14,14), like MNIST
        wsum = sum(s[2] for s in samples)
        mr = sum(s[0] * s[2] for s in samples) / wsum
        mc = sum(s[1] * s[2] for s in samples) / wsum
        C = np.zeros((4, 6, 6))
        for (r, c, w, phi) in samples:
            r += 14 - mr
            c += 14 - mc
            ow = [max(0.0, math.cos(2 * (phi - math.radians(th)))) ** 2 for th in thetas]
            gr = np.exp(-(centers - r) ** 2 / (2 * sp * sp))
            gc = np.exp(-(centers - c) ** 2 / (2 * sp * sp))
            g = np.outer(gr, gc) * w
            for o in range(4):
                C[o] += ow[o] * g
        MU[d] = A * (1 - np.exp(-C / C0))               # expected feature value

    # ---------------- fc: nearest-centroid scoring ----------------
    # logit_d = gamma * (mu_d . f - 0.5*||mu_d||^2)
    gamma = 4.0
    cnt = np.array([1, 1, 2, 2, 1, 1], dtype=float)     # duplicates of bin rows/cols
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for o in range(4):
        for k, (oy, ox) in enumerate(offsets):
            ch = o * 4 + k
            for i in range(4):
                for j in range(4):
                    br, bc = i + oy // 2, j + ox // 2
                    fc_w[:, ch * 16 + i * 4 + j] = gamma * MU[:, o, br, bc] / (cnt[br] * cnt[bc])
    fc_b = (-0.5 * gamma * (MU ** 2).reshape(10, -1).sum(axis=1)).astype(np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
