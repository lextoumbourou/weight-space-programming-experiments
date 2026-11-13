**Step 18 approach:** make the corner-zone features saturate, so the evidence depends on whether a corner is present and not on how strong it happens to be.

Steps 16 and 17 bracketed the problem. With the assumed typical response at 0.6, 8 was badly under-predicted; at 0.33 it was badly over-predicted (1308 predictions for 1009 true 8s), and the loss got worse. The corner response varies too much from image to image for an unclipped sum to work as evidence; it needs clipping, as the orientation features did.

I had thought clipping needed a second channel per feature, but there is a one-channel way. The corner maps are never negative, so a channel computing relu(c − S) carries the clipped value: min(S, c) = c − relu(c − S). It codes absence rather than presence, and the final layer can flip the sign.

Changes this step:
- Channels 12–15 now compute relu(0.25 − 3x3 sum of the corner map), which reports presence or absence over the same 4x4 px cells as before.
- The 0.15 threshold that used to sit in conv2 moves into the conv1 corner bias, with the loop threshold lowered from 1.5 to 0.9 to compensate.
- The zone evidence becomes the measured log-odds times the number of cells in the zone that fire, divided by 1.5, which is my estimate of how many cells one corner typically lights.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # Knobs
    # ------------------------------------------------------------------
    S_TEMP = 0.2      # scale (temperature) of the orientation-template logits
    T0 = 0.25         # conv2 noise threshold on summed orientation response
    CLIP = 1.2        # conv2 saturation level (feature = min(relu(S-T0),CLIP)/CLIP)
    C1_BIAS = -0.1    # conv1 bias of line filters
    L0 = 3.0          # px of aligned stroke giving ~63% "presence" in a template cell
    P_LO, P_HI = 0.08, 0.92   # orientation template probabilities squeezed into this range
    SKEL = 17.5       # skeleton size in px
    CEN = 13.5        # centre of mass position
    CORNER_BIAS = -1.05  # conv1 bias of inner-corner filters (was -0.9 plus 0.15 in conv2)
    BLANK_W = -0.5       # "must be blank" weight inside a corner filter
    THETA = 0.9          # conv2 threshold of the loop detector (1.5 - 4*0.15)
    GAMMA = 0.5          # trust factor for the loop evidence
    HOLE_GAIN = 1.3      # extra gain on loop slopes (only 4 loop sizes)
    CC = 0.25            # saturation level of the corner cell feature
    NBAR = 1.5           # typical number of cells lit by one corner in a zone
    GAMMA_C = 0.6        # trust factor for the corner-zone evidence
    ZP_LO, ZP_HI = 0.03, 0.97   # clip for measured corner-zone rates
    BIAS_ADJ = np.array([0.0, -0.1, 0.2, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0])

    # Loop evidence (from the step-4 diagnostic; consistent with the step-15 re-check)
    HOLE_UP = np.array([-1.5, -3.0, -0.5, 0.4, 0.1, -0.1, -2.5, -1.7, 3.1, 2.6])
    HOLE_LO = np.array([-1.3, -3.0, 1.35, -0.6, 0.0, -0.1, 2.9, -1.9, 3.7, -1.2])
    HOLE_NONE = np.array([-0.13, 0.0, -0.39, -0.29, -0.30, -0.22, -0.95, -0.07, -1.78, -0.77])

    # Measured rate (steps 13-15) at which each corner type fires in the upper /
    # lower half of the 4x4 grid, per true digit 0..9.
    # index: [corner type 0..3 = TL, TR, BL, BR][zone 0 = upper, 1 = lower]
    ZONE_P = {
        (0, 0): [.95, .16, .39, .59, .34, .93, .62, .38, .94, .93],     # TL upper
        (0, 1): [.44, .20, .79, .15, .65, .14, .79, .38, .945, .25],    # TL lower
        (1, 0): [.97, .05, .97, .98, .16, .14, .22, .985, .86, .90],    # TR upper
        (1, 1): [.09, .02, .51, .94, .99, .91, .76, .145, .92, .95],    # TR lower
        (2, 0): [.15, .02, .10, .63, .71, .80, .575, .15, .915, .745],  # BL upper
        (2, 1): [.99, .06, .94, .49, .67, .47, .98, .08, .88, .47],     # BL lower
        (3, 0): [.40, .20, .66, .91, .73, .24, .22, .30, .86, .74],     # BR upper
        (3, 1): [.97, .18, .805, .96, .64, .93, .88, .42, .91, .44],    # BR lower
    }

    # ------------------------------------------------------------------
    # conv1, filters 0..3: oriented line detectors
    # (0=horizontal, 45="/", 90=vertical, 135="\"), zero-sum, max response 1.
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
        f[f < 0] *= pos / neg
        return f / pos

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS

    # ------------------------------------------------------------------
    # conv1, filters 4..7: inner-corner detectors, types 0..3 = TL, TR, BL, BR.
    # TL = ink along the top AND along the left, blank just below-right of centre.
    # ------------------------------------------------------------------
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0    # top arm
    TL[2:5, 0:2] = 1.0 / 6.0    # left arm
    TL[2:4, 2:4] = BLANK_W      # inside of the concavity must be blank
    conv1_w[4, 0] = TL                  # type 0: TL
    conv1_w[5, 0] = TL[:, ::-1]         # type 1: TR
    conv1_w[6, 0] = TL[::-1, :]         # type 2: BL
    conv1_w[7, 0] = TL[::-1, ::-1]      # type 3: BR
    conv1_b[4:8] = CORNER_BIAS

    # ------------------------------------------------------------------
    # conv2, channels 0..7: clipped orientation presence
    #   channel k   = relu(boxsum3x3(orientation k) - T0)
    #   channel k+4 = relu(boxsum3x3(orientation k) - T0 - CLIP)
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # ------------------------------------------------------------------
    # conv2, channels 8..11: closed-loop detectors for 4 loop sizes.
    # relu(TL(upper-left) + TR(upper-right) + BL(lower-left) + BR(lower-right) - THETA)
    # ------------------------------------------------------------------
    sizes = [(1, 1), (2, 2), (2, 1), (1, 2)]
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
    # conv2, channels 12..15: saturating corner features, coded as ABSENCE:
    #   A = relu(CC - boxsum3x3(corner map t))
    # The corner maps are >= 0, so min(S, CC) = CC - A: one channel gives a
    # clipped feature. After the 2x2 max-pool, A is small only if the corner
    # response lies in the 4x4 px block common to the pooled windows, i.e. the
    # same cells as before. Presence of a corner in a cell = 1 - A/CC.
    # ------------------------------------------------------------------
    for t in range(4):
        conv2_w[12 + t, 4 + t, 1:4, 1:4] = -1.0
        conv2_b[12 + t] = CC

    # ------------------------------------------------------------------
    # Hand-drawn digit shapes. Coordinates (x, y): y from 0 (top) to 1 (bottom).
    # A shape = list of (weight, polyline); weight < 1 marks an optional stroke.
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

    # "2": hooked top arc, curved neck to bottom-left, flat wide base
    two_A = [(1.0, np.vstack([arc(0.36, 0.27, 0.30, 0.27, 175, -35, 22),
                              poly((0.45, 0.62), (0.22, 0.82), (0.05, 0.98),
                                   (0.85, 0.98))]))]
    # "2": small loop at the bottom-left, base swinging out to the right
    two_L = [(1.0, np.vstack([arc(0.36, 0.27, 0.30, 0.27, 175, -35, 22),
                              poly((0.45, 0.62), (0.25, 0.82), (0.08, 0.96),
                                   (0.02, 0.88), (0.08, 0.78), (0.20, 0.78),
                                   (0.30, 0.86), (0.45, 0.95), (0.65, 1.0),
                                   (0.88, 0.95))]))]
    # "2": big round top reaching below mid-height, straight neck, flat base
    two_R = [(1.0, np.vstack([arc(0.38, 0.33, 0.32, 0.33, 180, -45, 24),
                              poly((0.05, 0.98), (0.85, 0.98))]))]
    # "3": two round bowls
    three_A = [(1.0, arc(0.30, 0.235, 0.30, 0.235, 150, -90, 24)),
               (1.0, arc(0.30, 0.735, 0.36, 0.265, 90, -150, 24))]
    # "3": small upper bowl, middle bar reaching left, big lower bowl
    three_M = [(1.0, np.vstack([arc(0.34, 0.20, 0.26, 0.20, 160, -90, 20),
                                poly((0.15, 0.40))])),
               (1.0, arc(0.30, 0.70, 0.38, 0.30, 90, -160, 24))]
    # "4": left stroke, cross bar, right stem (open top)
    four = [(1.0, poly((0.20, 0.0), (0.02, 0.58))),
            (1.0, poly((0.02, 0.58), (0.80, 0.58))),
            (1.0, poly((0.63, 0.0), (0.52, 1.0)))]
    # "5": top bar, short down stroke, bowl
    five = [(1.0, np.vstack([poly((0.78, 0.0), (0.22, 0.04), (0.12, 0.42)),
                             arc(0.30, 0.69, 0.36, 0.31, 130, -150, 28)]))]
    # "6": steep stem down the left side, closed loop at the bottom
    six = [(1.0, np.vstack([poly((0.50, 0.0), (0.36, 0.15), (0.22, 0.33),
                                 (0.12, 0.52), (0.08, 0.72)),
                            arc(0.34, 0.73, 0.26, 0.26, 180, 540, 40)]))]
    # "7": top bar, long diagonal; optional cross bar and optional left serif
    seven = [(1.0, poly((0.0, 0.02), (0.72, 0.0))),
             (1.0, poly((0.72, 0.0), (0.30, 1.0))),
             (0.2, poly((0.25, 0.52), (0.70, 0.52))),
             (0.3, poly((0.0, 0.02), (0.0, 0.18)))]
    # "8": figure-eight
    t8 = np.linspace(0.0, 2.0 * math.pi, 64)
    x8 = 0.33 + (0.29 - 0.03 * np.sin(t8)) * np.sin(2 * t8)
    y8 = 0.5 - 0.5 * np.sin(t8)
    eight = [(1.0, np.stack([x8, y8], axis=1))]
    # "9": loop at the top, stem down the right side
    nine = [(1.0, arc(0.33, 0.27, 0.28, 0.27, 0, 360, 40)),
            (1.0, poly((0.61, 0.20), (0.60, 0.50), (0.50, 1.0)))]

    def generic(shape, base_shear):
        # narrow-upright / medium / wide-slanted versions
        return [(0.35, shape, 0.8, base_shear - 0.15),
                (0.25, shape, 1.0, base_shear),
                (0.40, shape, 1.2, base_shear)]

    # Each digit = mixture of variants (weight, shape, x-stretch, shear).
    digit_variants = {
        0: [(0.50, zero(0.42), 1.0, 0.18),
            (0.20, zero(0.34), 1.0, 0.18),
            (0.30, zero(0.27), 1.0, 0.18)],
        1: [(0.30, one(0.0), 1.0, 0.0),
            (0.22, one(12.0), 1.0, 0.0),
            (0.38, one(25.0), 1.0, 0.0),
            (0.04, one(38.0), 1.0, 0.0),
            (0.06, one(-12.0), 1.0, 0.0)],
        2: [(0.25, two_L, 1.0, 0.20),
            (0.15, two_L, 0.8, 0.05),
            (0.15, two_L, 1.2, 0.20),
            (0.20, two_A, 0.8, 0.05),
            (0.15, two_A, 1.2, 0.20),
            (0.10, two_R, 1.0, 0.20)],
        3: [(0.35, three_M, 1.0, 0.20),
            (0.20, three_M, 1.2, 0.20),
            (0.20, three_M, 0.8, 0.05),
            (0.15, three_A, 1.25, 0.20),
            (0.10, three_A, 0.8, 0.05)],
        4: generic(four, 0.10),
        5: generic(five, 0.20),
        6: generic(six, 0.20),
        7: generic(seven, 0.10),
        8: generic(eight, 0.20),
        9: generic(nine, 0.20),
    }

    def place(strokes, wx, shear):
        # stretch x, apply slant, scale skeleton to SKEL px, centre of mass at CEN
        sh = []
        for w, pts in strokes:
            p = np.array(pts, dtype=np.float64).copy()
            p[:, 0] *= wx
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
    # Orientation template of a shape drawn directly in feature space:
    # P[k, a, b] = "probability" that orientation k is present in final cell (a, b).
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # fc part 1: log-odds template matching on orientation features (channels 0..7)
    # ------------------------------------------------------------------
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for d in range(10):
        P = np.zeros((4, 4, 4), dtype=np.float64)
        tot = 0.0
        for pi, shape, wx, shear in digit_variants[d]:
            P += pi * render(place(shape, wx, shear))
            tot += pi
        P /= tot
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
    fc_b += BIAS_ADJ

    # ------------------------------------------------------------------
    # fc part 2: loop features (channels 8..11). Rows 0,1 = upper half, 2,3 = lower.
    # logit_d += GAMMA * (HOLE_NONE[d] + HOLE_GAIN*(HOLE_UP[d]*H_up + HOLE_LO[d]*H_lo))
    # ------------------------------------------------------------------
    for d in range(10):
        for ch in range(8, 12):
            for a in range(4):
                for b in range(4):
                    v = HOLE_UP[d] if a < 2 else HOLE_LO[d]
                    fc_w[d, ch * 16 + a * 4 + b] = GAMMA * HOLE_GAIN * v
        fc_b[d] += GAMMA * HOLE_NONE[d]

    # ------------------------------------------------------------------
    # fc part 3: corner-zone evidence (channels 12..15, absence-coded).
    # N = number of cells of the zone (8 cells: 2 rows x 4 columns) in which the
    #     corner type is present = sum over cells of (1 - A/CC).
    # With measured firing rate p of the zone for class d:
    #   logit_d += GAMMA_C * ( log(p/(1-p)) * N / NBAR + log(1-p) )
    # ------------------------------------------------------------------
    zb = np.zeros((10,), dtype=np.float64)
    for (t, z), plist in ZONE_P.items():
        p = np.clip(np.array(plist, dtype=np.float64), ZP_LO, ZP_HI)
        lo = np.log(p / (1.0 - p))
        rows = (0, 1) if z == 0 else (2, 3)
        for d in range(10):
            for a in rows:
                for b in range(4):
                    fc_w[d, (12 + t) * 16 + a * 4 + b] = -GAMMA_C * lo[d] / (CC * NBAR)
            zb[d] += GAMMA_C * (lo[d] * 8.0 / NBAR + math.log(1.0 - p[d]))
    zb -= zb.mean()
    fc_b += zb

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
