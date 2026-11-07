# Step 8: hand-drawn "anti-strokes" for the most-confused pairs

**What I learned from step 7.** Shear-blurring the templates helped a little, to 67.9% accuracy and 1.012 loss. Prediction counts are now fairly balanced, so the remaining errors are about shape rather than class bias. The largest confusions are:

- 3→5 (236) and 8→9 (203);
- 5→6 (154), 3→8 (129) and 2→8 (110);
- 4→1 (101), 2→3 (99) and 9→0 (98).

Correlation templates penalise ink in every empty cell equally. They do not specifically punish the one stroke that tells two similar digits apart.

**What changes in this step.** For each digit I hand-draw anti-strokes. These are places where a commonly confused rival has a stroke but this digit does not. They are rendered exactly like normal strokes and subtracted from the template with weight 0.7, before centring and normalising.

| Digit | Anti-strokes (the rival stroke being penalised) |
|---|---|
| 0 | horizontal bar through the centre (the loop tops and bottoms of 6 and 9) |
| 3 | left vertical at the upper left (5's stem), and a left-side segment at the lower left (8's lower loop) |
| 5 | right side at the upper right (3's upper arc), and the left gap of the bowl (6's closed loop) |
| 6 | upper-right shoulder (0), and the right part of a top bar (5) |
| 9 | lower-left side and bottom-left arc (0 and 8) |
| 4 | closed top bar (9) |
| 7 | left side of a top loop (9) |
| 2 | lower-right arc (3 and 8) |
| 1 | side horizontals (the crossbar of 4) |

**Unchanged.** The features, the positive strokes and the shear blur are all as in step 7. The bias accumulates one more term, 0.5·log(true count / predicted count), using step 7's counts.

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
                d = v * dy - u * dx
                K[i, j] = math.exp(-d * d / (2 * sig_line ** 2))
        K -= K.mean()
        K /= K[K > 0].sum()
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

    # ---------------- stroke primitives (unsheared, x=col, y=row) ----------------
    def line(p, q, step=0.5):
        p = np.array(p, float); q = np.array(q, float)
        L = np.hypot(*(q - p))
        n = max(2, int(math.ceil(L / step)) + 1)
        return [tuple(p + (q - p) * t) for t in np.linspace(0, 1, n)]

    def poly(pts):
        out = []
        for a in range(len(pts) - 1):
            out += line(pts[a], pts[a + 1])
        return out

    def arc(cx, cy, rx, ry, t0, t1, n=120):
        return [(cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t)))
                for t in np.linspace(t0, t1, n)]

    # Positive strokes (what the digit has)
    digits = {
        0: [arc(14, 13.5, 5.5, 8.5, 0, 360)],
        1: [line((15, 4.5), (13, 22.5))],
        2: [arc(14, 9, 5, 4.5, 160, -30),
            line((18.33, 11.25), (9, 22)),
            line((9, 22), (19.5, 22))],
        3: [arc(13.5, 9, 5, 4.5, 135, -90),
            line((13.5, 13.5), (11, 13.5)),
            arc(13.5, 18, 5.5, 4.5, 90, -150)],
        4: [line((10.5, 5), (8, 15)),
            line((8, 15), (20, 15)),
            line((17, 6.5), (16, 22.5))],
        5: [line((11, 5), (19, 5)),
            line((11, 5), (10.5, 13)),
            arc(13.5, 17.5, 5.5, 4.5, 140, -150)],
        6: [poly([(17.5, 4), (13.5, 6.5), (11, 10), (9.5, 14), (9.5, 18)]),
            arc(14, 18, 4.7, 4.7, 0, 360)],
        7: [line((8.5, 5), (19.5, 5)),
            line((19.5, 5), (12.5, 22.5))],
        8: [arc(14.5, 8.8, 3.8, 4.3, 0, 360),
            arc(13.5, 18, 4.8, 4.5, 0, 360)],
        9: [arc(14.5, 9, 4.5, 4.5, 0, 360),
            line((19, 9), (17, 22.5))],
    }
    # Anti-strokes (where a confusable rival has ink but this digit should not)
    anti = {
        0: [line((10.5, 13.5), (17.5, 13.5))],                       # 6/9 loop crossing
        1: [line((7.5, 14.5), (11, 14.5)), line((17, 14.5), (20, 14.5))],  # 4 crossbar
        2: [line((19, 15.5), (18.5, 20))],                           # 3/8 lower-right arc
        3: [line((10.5, 5.5), (10, 12)),                             # 5 left stem
            line((9, 15.5), (9, 18.5))],                             # 8 lower-left
        4: [line((11, 4.5), (17, 4.5))],                             # 9 closed top
        5: [line((18.5, 7), (18.5, 11)),                             # 3/9 upper-right
            line((9, 15.5), (9.5, 18.5))],                           # 6 closed left
        6: [arc(14, 13.5, 5.5, 8.5, 20, 80),                         # 0 upper-right shoulder
            line((14.5, 5), (19.5, 5))],                             # 5 top bar
        7: [line((10, 8), (10, 12))],                                # 9 loop left side
        8: [],
        9: [line((9.5, 15), (10, 20)),                               # 0/8 lower-left
            line((10, 22), (14, 22.5))],                             # 0/8 bottom-left
    }
    lam_anti = 0.7

    base_shear = {d: 0.12 for d in range(10)}
    base_shear[8] = 0.22
    shear_spread = [-0.2, 0.0, 0.2]           # slant blur

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 3.0

    def render(strokes, shear):
        T = np.zeros((4, 8, 8))
        for pts in strokes:
            pts = np.asarray(pts, float).copy()
            pts[:, 0] = pts[:, 0] + shear * (13.5 - pts[:, 1])
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
                    T[k] = np.maximum(T[k], g * dot ** 4)
        return T

    def blurred(strokes, d):
        if len(strokes) == 0:
            return np.zeros((4, 8, 8))
        return np.mean([render(strokes, base_shear[d] + ds) for ds in shear_spread], axis=0)

    # ---------------- fc: centred unit-norm templates + cumulative class bias ----------------
    beta = 3.0
    Wf = np.zeros((10, 256), np.float32)
    true_cnt = np.array([1000, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    preds = [
        [1153, 1439, 1368, 567, 251, 687, 1668, 1524, 423, 920],   # step 3
        [1312, 1420, 942, 687, 976, 877, 1017, 1397, 701, 675],    # step 4
        [1198, 1491, 1022, 751, 916, 808, 1015, 1137, 768, 896],   # step 5
        [1129, 1380, 881, 826, 838, 731, 967, 1057, 1257, 934],    # step 6
        [1122, 1388, 960, 855, 881, 852, 929, 970, 1050, 994],     # step 7
    ]
    bf = np.zeros(10)
    for p in preds:
        bf += 0.5 * np.log(true_cnt / np.array(p, float))
    bf = bf.astype(np.float32)

    for d in range(10):
        T = blurred(digits[d], d) - lam_anti * blurred(anti[d], d)
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
