**Step 6 approach:** another diagnostic step, this time checking the geometric assumptions behind my hand-drawn templates rather than classifying.

The remaining errors (2→8, 3→5, 0→2, 6→4 and so on) point to templates that do not sit where the real strokes are. Two assumptions affect all ten templates and I have never tested them: how large the skeleton is, and how slanted the writing is. So the ten outputs this step are ten hand-drawn variants of the two simplest digits, and the winning variant shows which drawing real digits resemble most.

| Output | Variant | True-digit row to read |
|---|---|---|
| 0 | "0", current drawing | 0 |
| 1 | "0", smaller | 0 |
| 2 | "0", larger | 0 |
| 3 | "0", narrower | 0 |
| 4 | "0", wider | 0 |
| 5 | "1", vertical | 1 |
| 6 | "1", slanted 12° | 1 |
| 7 | "1", slanted 25° | 1 |
| 8 | "1", slanted 38° | 1 |
| 9 | "1", slanted −12° (leaning left) | 1 |

The loss will be poor again; this step is only for calibration. I will use the result to redraw all templates at the right scale and slant.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: tournament between hand-drawn variants of "0" and "1"
    # to calibrate the template geometry (scale, width, slant).
    #   outputs 0..4 : "0" variants  (base, smaller, larger, narrower, wider)
    #   outputs 5..9 : "1" variants  (slant 0, 12, 25, 38, -12 degrees)
    # ------------------------------------------------------------------
    S_TEMP = 0.2
    T0 = 0.25
    CLIP = 1.2
    C1_BIAS = -0.1
    L0 = 3.0
    P_LO, P_HI = 0.08, 0.92
    CEN = 13.5
    CORNER_BIAS = -0.9
    BLANK_W = -0.5
    THETA = 1.5

    # conv1, filters 0..3: oriented line detectors (0, 45 "/", 90, 135 "\")
    def line_filter(theta_deg):
        th = math.radians(theta_deg)
        f = np.zeros((5, 5), dtype=np.float64)
        for r in range(5):
            for c in range(5):
                y = r - 2
                x = c - 2
                u = abs(x * math.sin(th) + y * math.cos(th))
                f[r, c] = np.interp(u, [0.0, 1.0, 2.0, 3.0], [2.0, 0.0, -1.0, -1.0])
        pos = f[f > 0].sum()
        neg = -f[f < 0].sum()
        f[f < 0] *= pos / neg
        return f / pos

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS

    # conv1, filters 4..7: inner-corner detectors (kept; not read out in this step)
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0
    TL[2:5, 0:2] = 1.0 / 6.0
    TL[2:4, 2:4] = BLANK_W
    conv1_w[4, 0] = TL
    conv1_w[5, 0] = TL[:, ::-1]
    conv1_w[6, 0] = TL[::-1, :]
    conv1_w[7, 0] = TL[::-1, ::-1]
    conv1_b[4:8] = CORNER_BIAS

    # conv2, channels 0..7: clipped orientation presence
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # conv2, channels 8..15: loop detectors (kept; fc weights are zero in this step)
    sizes = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (3, 3)]
    for i, (sy, sx) in enumerate(sizes):
        ch = 8 + i
        r0 = (4 - sy) // 2
        c0 = (4 - sx) // 2
        conv2_w[ch, 4, r0, c0] += 1.0
        conv2_w[ch, 5, r0, c0 + sx] += 1.0
        conv2_w[ch, 6, r0 + sy, c0] += 1.0
        conv2_w[ch, 7, r0 + sy, c0 + sx] += 1.0
        conv2_b[ch] = -THETA

    # ------------------------------------------------------------------
    # hand-drawn variants: (strokes, shear, skeleton size in px)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        t = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], axis=1)

    def poly(*pts):
        return np.array(pts, dtype=np.float64)

    def zero(rx):
        return [(1.0, arc(rx + 0.03, 0.5, rx, 0.5, 0, 360, 48))]

    def one(angle_deg):
        dx = 0.5 * math.tan(math.radians(angle_deg))
        return [(1.0, poly((dx, 0.0), (-dx, 1.0)))]

    variants = [
        (zero(0.34), 0.18, 17.5),   # 0: "0" base
        (zero(0.34), 0.18, 15.5),   # 1: "0" smaller
        (zero(0.34), 0.18, 19.5),   # 2: "0" larger
        (zero(0.27), 0.18, 17.5),   # 3: "0" narrower
        (zero(0.42), 0.18, 17.5),   # 4: "0" wider
        (one(0.0), 0.0, 17.5),      # 5: "1" vertical
        (one(12.0), 0.0, 17.5),     # 6: "1" slant 12 deg
        (one(25.0), 0.0, 17.5),     # 7: "1" slant 25 deg
        (one(38.0), 0.0, 17.5),     # 8: "1" slant 38 deg
        (one(-12.0), 0.0, 17.5),    # 9: "1" leaning left 12 deg
    ]

    def place(strokes, shear, skel):
        sh = []
        for w, pts in strokes:
            p = np.array(pts, dtype=np.float64).copy()
            p[:, 0] += shear * (0.5 - p[:, 1])
            sh.append((w, p))
        main = np.vstack([p for w, p in sh if w >= 0.35])
        size = max(main[:, 0].max() - main[:, 0].min(),
                   main[:, 1].max() - main[:, 1].min())
        scale = skel / size
        tot = 0.0
        com = np.zeros(2)
        for w, p in sh:
            seg = p[1:] - p[:-1]
            ln = np.sqrt((seg ** 2).sum(axis=1))
            mid = 0.5 * (p[1:] + p[:-1])
            com += w * (ln[:, None] * mid).sum(axis=0)
            tot += w * ln.sum()
        com /= tot
        return [(w, (p - com) * scale + CEN) for w, p in sh]

    cell_c = 4.0 * np.arange(4) + 7.5

    def win(t):
        return np.clip((6.0 - np.abs(t)) / 3.0, 0.0, 1.0)

    def render(strokes):
        notp = np.ones((4, 4, 4), dtype=np.float64)
        for w, pts in strokes:
            L = np.zeros((4, 4, 4), dtype=np.float64)
            for i in range(len(pts) - 1):
                x0, y0 = pts[i]
                x1, y1 = pts[i + 1]
                seglen = math.hypot(x1 - x0, y1 - y0)
                if seglen < 1e-9:
                    continue
                phi = math.atan2(-(y1 - y0), x1 - x0)
                n = max(1, int(math.ceil(seglen / 0.5)))
                for j in range(n):
                    f = (j + 0.5) / n
                    x = x0 + f * (x1 - x0)
                    y = y0 + f * (y1 - y0)
                    sp = np.outer(win(y - cell_c), win(x - cell_c))
                    for k in range(4):
                        tun = (0.5 + 0.5 * math.cos(2.0 * (phi - math.radians(45.0 * k)))) ** 2
                        L[k] += (seglen / n) * tun * sp
            q = w * (1.0 - np.exp(-L / L0))
            notp *= (1.0 - q)
        return 1.0 - notp

    # fc: same log-odds template matching as the classifier, but the 10 "classes"
    # are the 10 variants above.
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for d in range(10):
        strokes, shear, skel = variants[d]
        P = render(place(strokes, shear, skel))
        P = P_LO + (P_HI - P_LO) * P
        lo = np.log(P / (1.0 - P))
        fc_b[d] = S_TEMP * np.log(1.0 - P).sum()
        for k in range(4):
            for a in range(4):
                for b in range(4):
                    wgt = S_TEMP * lo[k, a, b] / CLIP
                    fc_w[d, k * 16 + a * 4 + b] = wgt
                    fc_w[d, (k + 4) * 16 + a * 4 + b] = -wgt
    fc_b -= fc_b.mean()

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
