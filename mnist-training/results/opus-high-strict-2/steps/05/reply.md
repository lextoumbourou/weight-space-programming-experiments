# Step 5: blurrier templates, broader orientation tuning, cumulative biases

**What I learned from step 4.** Slant and class balance helped: accuracy went from 60% to 65% and loss from 1.17 to 1.07.

My guess at the main remaining error source is that the templates are sharper than the real class means. The step-1 pattern points to this: the broadest templates (8 and 6) attracted the most images, which suggests real feature maps are more diffuse than my strokes. Real handwriting varies by a few pixels in stroke position and angle. The average feature map of a class is therefore a blurred version of my clean strokes, both in space and in orientation.

**What changes in this step.**

1. **Spatial blur.** The template blur rises from σ = 2.5 px to 3.0 px.
2. **Orientation tuning.** It changes from max(0, cos 2Δ) to cos⁴Δ.
   - A stroke 45° away from a detector now contributes 0.25 instead of 0.
   - This mimics the leakage of real 5×5 line detectors and the angle variation in handwriting.
3. **Biases.** They accumulate: step 4's bias plus 0.5·log(true count / predicted count), using step 4's counts. This trims over-predicted 0, 1 and 7, and boosts 9, 8 and 3.

Everything else is unchanged from step 4: the features, the stroke shapes, the 0.12 shear and β = 3.

```python
import numpy as np
import math

def build_weights():
    s2 = 1.0 / math.sqrt(2.0)
    # Orientation unit vectors (dx, dy), x = column, y = row (DOWN)
    # k=0 horizontal, k=1 "\" diagonal, k=2 vertical, k=3 "/" diagonal
    dirs = [(1.0, 0.0), (s2, s2), (0.0, 1.0), (s2, -s2)]

    # ---------------- conv1: oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    c1 = 2.5
    sig_line = 0.8
    for k, (dx, dy) in enumerate(dirs):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                u = i - c1; v = j - c1
                d = v * dy - u * dx               # distance to ridge through kernel centre
                K[i, j] = math.exp(-d * d / (2 * sig_line ** 2))
        K -= K.mean()                            # zero mean
        K /= K[K > 0].sum()                      # ~3px stroke -> ~1
        W1[k, 0] = K
        b1[k] = -0.1
    # channels 4..7 unused

    # ---------------- conv2: pass-through at 4 sub-offsets ----------------
    # ch = k*4 + oa*2 + ob ; feature (ch,r,col) = grid cell s=2r+oa, t=2col+ob of orientation k
    # grid cell centre: input row 2s+6, col 2t+6
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for k in range(4):
        for oa in range(2):
            for ob in range(2):
                W2[k * 4 + oa * 2 + ob, k, 1 + oa, 1 + ob] = 1.0

    # ---------------- digit templates drawn as strokes ----------------
    shear = 0.12   # rightward slant: x += shear*(13.5 - y)

    def sh(p):
        return (p[0] + shear * (13.5 - p[1]), p[1])

    def line(p, q, step=0.5):
        p = np.array(p, float); q = np.array(q, float)
        L = np.hypot(*(q - p))
        n = max(2, int(math.ceil(L / step)) + 1)
        return [sh(tuple(p + (q - p) * t)) for t in np.linspace(0, 1, n)]

    def arc(cx, cy, rx, ry, t0, t1, n=120):
        return [sh((cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t))))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [arc(14, 13.5, 5.5, 8.5, 0, 360)],
        1: [line((15, 4.5), (13, 22.5))],
        2: [arc(14, 9, 5, 4.5, 160, -30),
            line((18.33, 11.25), (9, 22)),
            line((9, 22), (19.5, 22))],
        3: [arc(13.5, 9, 5, 4.5, 150, -90),
            arc(13.5, 18, 5.5, 4.5, 90, -150)],
        4: [line((10.5, 5), (8, 15)),
            line((8, 15), (20, 15)),
            line((17, 6.5), (16, 22.5))],
        5: [line((11, 5), (19, 5)),
            line((11, 5), (10.5, 12.5)),
            arc(13.5, 17, 5.5, 5, 140, -150)],
        6: [line((17, 4.5), (12, 10)),
            line((12, 10), (9.5, 16)),
            arc(14, 18, 4.5, 4.5, 0, 360)],
        7: [line((8.5, 5), (19.5, 5)),
            line((19.5, 5), (12.5, 22.5))],
        8: [arc(14, 9, 4.5, 4.3, 0, 360),
            arc(14, 18, 5, 4.5, 0, 360)],
        9: [arc(14.5, 9, 4.5, 4.5, 0, 360),
            line((19, 9), (17, 22.5))],
    }

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 3.0        # blurrier templates (closer to real class means)

    def render(strokes):
        T = np.zeros((4, 8, 8))
        for pts in strokes:
            pts = np.asarray(pts, float)
            for a in range(len(pts) - 1):
                p, q = pts[a], pts[a + 1]
                dv = q - p
                L = math.hypot(dv[0], dv[1])
                if L < 1e-9:
                    continue
                ux, uy = dv / L
                mx, my = (p + q) / 2
                g = np.exp(-((Xg - mx) ** 2 + (Yg - my) ** 2) / (2 * sig_t ** 2))
                for k, (dx, dy) in enumerate(dirs):
                    dot = ux * dx + uy * dy
                    tune = dot ** 4               # broader orientation tuning (45deg -> 0.25)
                    T[k] = np.maximum(T[k], g * tune)
        return T

    # ---------------- fc: centred unit-norm templates + cumulative class bias ----------------
    beta = 3.0
    Wf = np.zeros((10, 256), np.float32)
    true_cnt = np.array([1000, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    pred3 = np.array([1153, 1439, 1368, 567, 251, 687, 1668, 1524, 423, 920], float)
    pred4 = np.array([1312, 1420, 942, 687, 976, 877, 1017, 1397, 701, 675], float)
    bf = (0.5 * np.log(true_cnt / pred3) + 0.5 * np.log(true_cnt / pred4)).astype(np.float32)
    for d in range(10):
        T = render(digits[d])
        T = T - T.mean()
        T = T / (np.linalg.norm(T) + 1e-9)
        for k in range(4):
            for oa in range(2):
                for ob in range(2):
                    ch = k * 4 + oa * 2 + ob
                    for r in range(4):
                        for col in range(4):
                            Wf[d, ch * 16 + r * 4 + col] = beta * T[k, 2 * r + oa, 2 * col + ob]

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wf.astype(np.float32),
        'fc.bias': bf.astype(np.float32),
    }
```
