# Step 3: centred (Pearson-style) template weights

**What I learned from step 2.** The biases helped accuracy, from 57% to 61%, but they overshot badly. Now 4 is predicted 1,823 times and 8 only 145 times. That means the template scores barely differ between classes, so a bias of about 1.7 logits swamps them.

The underlying weakness is that all fc weights are non-negative. Ink in places where a digit has no stroke is never penalised, so templates with broad coverage like 8 and 6 win by default.

**What changes in this step.**

- **Centred weights.** Each digit's 256-dim template now has its own global mean subtracted, and is then renormalised to unit length. The logit becomes a correlation coefficient instead of a cosine.
  - Cells where a digit has no stroke now get negative weight. For example, horizontal ink now counts against "1", and ink on the left side counts against "3".
  - Each class gets its own penalty on total ink, so broad templates like 8 no longer win just by covering more area.
- **Biases reset to 0.** The score distribution is completely different now, so the old biases would no longer fit.
- **Temperature raised.** β goes from 2 to 3, because the old logits looked too flat.
- **Unchanged.** The features (conv1, conv2) and the stroke templates are the same as in step 1.

```python
import numpy as np
import math

def build_weights():
    s2 = 1.0 / math.sqrt(2.0)
    # Orientation unit vectors (dx, dy) in image coords (x = column, y = row, y DOWN)
    # k=0 horizontal, k=1 "\" diagonal, k=2 vertical, k=3 "/" diagonal
    dirs = [(1.0, 0.0), (s2, s2), (0.0, 1.0), (s2, -s2)]

    # ---------------- conv1: oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    c1 = 2.5          # ridge centre inside the 5x5 kernel
    sig_line = 0.8    # ridge width (px)
    for k, (dx, dy) in enumerate(dirs):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                u = i - c1; v = j - c1
                d = v * dy - u * dx               # perpendicular distance to the ridge
                K[i, j] = math.exp(-d * d / (2 * sig_line ** 2))
        K -= K.mean()                            # zero mean
        K /= K[K > 0].sum()                      # ~3px stroke -> ~1
        W1[k, 0] = K
        b1[k] = -0.1
    # channels 4..7 unused

    # ---------------- conv2: pass-through at 4 sub-offsets ----------------
    # ch = k*4 + oa*2 + ob copies orientation k at kernel pos (1+oa, 1+ob)
    # -> feature (ch, r, col) = grid cell s=2r+oa, t=2col+ob (centre row 2s+6, col 2t+6)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for k in range(4):
        for oa in range(2):
            for ob in range(2):
                W2[k * 4 + oa * 2 + ob, k, 1 + oa, 1 + ob] = 1.0

    # ---------------- digit templates drawn as strokes ----------------
    def line(p, q, step=0.5):
        p = np.array(p, float); q = np.array(q, float)
        L = np.hypot(*(q - p))
        n = max(2, int(math.ceil(L / step)) + 1)
        return [tuple(p + (q - p) * t) for t in np.linspace(0, 1, n)]

    def arc(cx, cy, rx, ry, t0, t1, n=120):
        return [(cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t)))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [arc(14, 13.5, 5.5, 8.5, 0, 360)],
        1: [line((16, 4.5), (12.5, 22.5))],
        2: [arc(14, 9, 5, 4.5, 160, -30),
            line((18.33, 11.25), (9, 22)),
            line((9, 22), (19.5, 22))],
        3: [arc(13.5, 9, 5, 4.5, 150, -90),
            arc(13.5, 18, 5.5, 4.5, 90, -150)],
        4: [line((11, 5), (8.5, 15.5)),
            line((8.5, 15.5), (19.5, 15.5)),
            line((16.5, 6), (16.5, 22.5))],
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
        9: [arc(14, 9.5, 5, 5, 0, 360),
            line((19, 10), (17.5, 22.5))],
    }

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 2.5

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
                    tune = max(0.0, 2 * dot * dot - 1)
                    T[k] = np.maximum(T[k], g * tune)
        return T

    # ---------------- fc: Pearson-style (centred, unit-norm) templates ----------------
    beta = 3.0
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        T = render(digits[d])
        T = T - T.mean()                          # centre: absent strokes get negative weight
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
