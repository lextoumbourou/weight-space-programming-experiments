**Step 1 approach:** a baseline built from oriented-stroke features matched against hand-drawn stroke templates.

- **conv1:** four line detectors at 0°, 45°, 90° and 135°. Each is zero-sum across the stroke, so blank and solid regions give 0. The other four filters are left at zero for later steps.
- **conv2:** for each orientation, a 3x3 box sum over the pooled map gives roughly the stroke length of that orientation in a cell. Each orientation uses two channels with different thresholds, so the final layer can form a clipped "is this stroke present" feature in [0,1] by subtracting one from the other.
- **fc:** each digit is described by hand as a few strokes (lines and arcs). A formula turns these strokes directly into a 4x4x4 table of how likely each orientation is in each cell. The weights are the log-odds of that table, scaled down by a temperature.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # Knobs (to be tuned from feedback in later steps)
    # ------------------------------------------------------------------
    S_TEMP = 0.2      # global scale (temperature) of the logits
    T0 = 0.25         # conv2 noise threshold on summed orientation response
    CLIP = 1.2        # conv2 saturation level (feature = min(relu(S-T0),CLIP)/CLIP)
    C1_BIAS = -0.1    # conv1 bias (suppresses weak / off-orientation responses)
    L0 = 3.0          # px of aligned stroke giving ~63% "presence" in a template cell
    P_LO, P_HI = 0.08, 0.92   # template probabilities are squeezed into this range
    SKEL = 17.5       # skeleton size in px (20px ink box minus stroke thickness)
    CEN = 13.5        # centre of mass position (pixel-index coordinates)

    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors (0=horizontal, 45="/", 90=vertical, 135="\")
    # profile across the stroke: +2 on the centre line, 0 at distance 1, -1 further
    # out; negatives rescaled so each filter sums to zero; max response = 1.
    # ------------------------------------------------------------------
    def line_filter(theta_deg):
        th = math.radians(theta_deg)
        f = np.zeros((5, 5), dtype=np.float64)
        for r in range(5):
            for c in range(5):
                y = r - 2
                x = c - 2
                u = abs(x * math.sin(th) + y * math.cos(th))  # distance to the line
                f[r, c] = np.interp(u, [0.0, 1.0, 2.0, 3.0], [2.0, 0.0, -1.0, -1.0])
        pos = f[f > 0].sum()
        neg = -f[f < 0].sum()
        f[f < 0] *= pos / neg          # zero-sum filter
        return f / pos                 # ideal stroke -> response 1

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS
    # filters 4..7 unused for now (zero)

    # ------------------------------------------------------------------
    # conv2: channel k   = relu(boxsum3x3(orientation k) - T0)
    #        channel k+4 = relu(boxsum3x3(orientation k) - T0 - CLIP)
    # (channel k - channel k+4)/CLIP is a clipped presence feature in [0,1]
    # (max-pooling commutes with these monotone functions).
    # channels 8..15 unused for now.
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # ------------------------------------------------------------------
    # Hand-drawn digit skeletons. Coordinates (x, y): y from 0 (top) to 1 (bottom),
    # x in the same units. Each stroke = (weight, polyline); weight < 1 marks an
    # optional stroke (style variant).
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        # ellipse arc, angles in degrees, 0=right, 90=top (y axis points down)
        t = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], axis=1)

    def poly(*pts):
        return np.array(pts, dtype=np.float64)

    digits = {}
    # 0: ellipse
    digits[0] = ([(1.0, arc(0.37, 0.5, 0.34, 0.5, 0, 360, 48))], 0.10)
    # 1: single stroke, three slant variants
    digits[1] = ([(0.4, poly((0.0, 0.0), (0.0, 1.0))),
                  (0.5, poly((0.10, 0.0), (-0.10, 1.0))),
                  (0.3, poly((0.22, 0.0), (-0.22, 1.0)))], 0.0)
    # 2: top arc, diagonal down to bottom-left, base bar
    digits[2] = ([(1.0, np.vstack([arc(0.33, 0.25, 0.28, 0.25, 160, -30, 20),
                                   poly((0.03, 1.0), (0.72, 1.0))]))], 0.10)
    # 3: two right-bulging arcs
    digits[3] = ([(1.0, arc(0.30, 0.235, 0.30, 0.235, 150, -90, 24)),
                  (1.0, arc(0.30, 0.735, 0.36, 0.265, 90, -150, 24))], 0.10)
    # 4: left stroke, cross bar, right stem (open top)
    digits[4] = ([(1.0, poly((0.20, 0.0), (0.02, 0.58))),
                  (1.0, poly((0.02, 0.58), (0.80, 0.58))),
                  (1.0, poly((0.63, 0.0), (0.52, 1.0)))], 0.0)
    # 5: top bar, short down stroke, bowl
    digits[5] = ([(1.0, np.vstack([poly((0.72, 0.0), (0.20, 0.0), (0.10, 0.42)),
                                   arc(0.30, 0.69, 0.36, 0.31, 130, -150, 28)]))], 0.10)
    # 6: sweep from top-right down the left side, closed loop at the bottom
    digits[6] = ([(1.0, np.vstack([poly((0.62, 0.0), (0.40, 0.12), (0.20, 0.33),
                                        (0.07, 0.55), (0.03, 0.72)),
                                   arc(0.33, 0.72, 0.30, 0.28, 180, 540, 40)]))], 0.10)
    # 7: top bar, long diagonal; optional cross bar and optional left serif
    digits[7] = ([(1.0, poly((0.0, 0.02), (0.72, 0.0))),
                  (1.0, poly((0.72, 0.0), (0.30, 1.0))),
                  (0.2, poly((0.25, 0.52), (0.70, 0.52))),
                  (0.3, poly((0.0, 0.02), (0.0, 0.18)))], 0.0)
    # 8: figure-eight (crossing in the middle), upper lobe slightly narrower
    t8 = np.linspace(0.0, 2.0 * math.pi, 64)
    x8 = 0.33 + (0.29 - 0.03 * np.sin(t8)) * np.sin(2 * t8)
    y8 = 0.5 - 0.5 * np.sin(t8)
    digits[8] = ([(1.0, np.stack([x8, y8], axis=1))], 0.10)
    # 9: loop at the top, stem down the right side
    digits[9] = ([(1.0, arc(0.33, 0.27, 0.28, 0.27, 0, 360, 40)),
                  (1.0, poly((0.61, 0.20), (0.60, 0.50), (0.50, 1.0)))], 0.10)

    def place(strokes, shear):
        # apply slant, scale the skeleton to SKEL px, put centre of mass at CEN
        sh = []
        for w, pts in strokes:
            p = np.array(pts, dtype=np.float64).copy()
            p[:, 0] += shear * (0.5 - p[:, 1])
            sh.append((w, p))
        main = np.vstack([p for w, p in sh if w >= 0.35])
        size = max(main[:, 0].max() - main[:, 0].min(),
                   main[:, 1].max() - main[:, 1].min())
        scale = SKEL / size
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

    # ------------------------------------------------------------------
    # Draw the template of each digit directly in feature space:
    # P[k, a, b] = "probability" that orientation k is present in final cell (a, b).
    # Final cell (a, b) looks at input pixels around (4a+7.5, 4b+7.5), ~ +-4.5 px.
    # ------------------------------------------------------------------
    cell_c = 4.0 * np.arange(4) + 7.5

    def win(t):
        # soft spatial window of a cell: 1 within 3 px, fading to 0 at 6 px
        return np.clip((6.0 - np.abs(t)) / 3.0, 0.0, 1.0)

    def render(strokes):
        notp = np.ones((4, 4, 4), dtype=np.float64)
        for w, pts in strokes:
            L = np.zeros((4, 4, 4), dtype=np.float64)  # aligned stroke length per cell
            for i in range(len(pts) - 1):
                x0, y0 = pts[i]
                x1, y1 = pts[i + 1]
                seglen = math.hypot(x1 - x0, y1 - y0)
                if seglen < 1e-9:
                    continue
                phi = math.atan2(-(y1 - y0), x1 - x0)  # stroke orientation
                n = max(1, int(math.ceil(seglen / 0.5)))
                for j in range(n):
                    f = (j + 0.5) / n
                    x = x0 + f * (x1 - x0)
                    y = y0 + f * (y1 - y0)
                    sp = np.outer(win(y - cell_c), win(x - cell_c))  # (row, col)
                    for k in range(4):
                        # orientation tuning of the line filters
                        tun = (0.5 + 0.5 * math.cos(2.0 * (phi - math.radians(45.0 * k)))) ** 2
                        L[k] += (seglen / n) * tun * sp
            q = w * (1.0 - np.exp(-L / L0))
            notp *= (1.0 - q)
        return 1.0 - notp

    # ------------------------------------------------------------------
    # fc: Bernoulli log-odds template matching on the clipped presence features
    # logit_d = S_TEMP * ( sum_f y_f * log(p/(1-p)) + sum_f log(1-p) )
    # ------------------------------------------------------------------
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for d in range(10):
        strokes, shear = digits[d]
        P = render(place(strokes, shear))
        P = P_LO + (P_HI - P_LO) * P
        lo = np.log(P / (1.0 - P))
        fc_b[d] = S_TEMP * np.log(1.0 - P).sum()
        for k in range(4):
            for a in range(4):
                for b in range(4):
                    wgt = S_TEMP * lo[k, a, b] / CLIP
                    fc_w[d, k * 16 + a * 4 + b] = wgt            # relu(S - T0)
                    fc_w[d, (k + 4) * 16 + a * 4 + b] = -wgt     # minus relu(S - T0 - CLIP)
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
