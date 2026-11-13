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
    CORNER_BIAS = -0.9   # conv1 bias of inner-corner filters
    BLANK_W = -0.5       # "must be blank" weight inside a corner filter
    THETA = 1.5          # conv2 threshold of the loop detector
    GAMMA = 0.7          # trust factor for the loop evidence
    HOLE_GAIN = 1.3      # extra gain on loop slopes (only 4 loop sizes are left)
    S_C = 0.40           # scale of the corner-map logits  (was 0.25)
    C_T0 = 0.15          # threshold on corner maps (removes weak diagonal-edge responses)
    C_TYP = 0.35         # typical corner response after threshold (feature = y / C_TYP)
    PC_LO, PC_HI = 0.04, 0.85  # corner template probabilities squeezed into this range
    # per-class offsets from the prediction-count imbalance
    BIAS_ADJ = np.array([-0.2, -0.25, 0.3, 0.0, 0.2, 0.0, 0.15, -0.25, 0.25, 0.1])
    # Loop evidence (from the step-4 diagnostic of the detector)
    HOLE_UP = np.array([-1.5, -3.0, -0.5, 0.4, 0.1, -0.1, -2.5, -1.7, 3.1, 2.6])
    HOLE_LO = np.array([-1.3, -3.0, 1.35, -0.6, 0.0, -0.1, 2.9, -1.9, 3.7, -1.2])
    HOLE_NONE = np.array([-0.13, 0.0, -0.39, -0.29, -0.30, -0.22, -0.95, -0.07, -1.78, -0.77])

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
    # conv2, channels 12..15: corner maps passed through (single centre tap).
    # ------------------------------------------------------------------
    for t in range(4):
        conv2_w[12 + t, 4 + t, 2, 2] = 1.0
        conv2_b[12 + t] = -C_T0

    # ------------------------------------------------------------------
    # Hand-drawn digit shapes. Coordinates (x, y): y from 0 (top) to 1 (bottom).
    # A shape = (strokes, corners)
    #   strokes: list of (weight, polyline); weight < 1 marks an optional stroke
    #   corners: list of (type, x, y, strength) = hand annotation of where an
    #            inner corner / tight concavity of that type sits and how
    #            reliably it should show up (types: 0=TL, 1=TR, 2=BL, 3=BR)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        t = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], axis=1)

    def poly(*pts):
        return np.array(pts, dtype=np.float64)

    def zero(rx):
        cx = rx + 0.03
        strokes = [(1.0, arc(cx, 0.5, rx, 0.5, 0, 360, 48))]
        corners = [(0, cx - 0.45 * rx, 0.2, 0.3), (1, cx + 0.45 * rx, 0.2, 0.3),
                   (2, cx - 0.45 * rx, 0.8, 0.3), (3, cx + 0.45 * rx, 0.8, 0.3)]
        return (strokes, corners)

    def one(angle_deg):
        dx = 0.5 * math.tan(math.radians(angle_deg))
        return ([(1.0, poly((dx, 0.0), (-dx, 1.0)))], [])

    # "2": hooked top arc, curved neck to bottom-left, flat wide base
    two_A = ([(1.0, np.vstack([arc(0.36, 0.27, 0.30, 0.27, 175, -35, 22),
                               poly((0.45, 0.62), (0.22, 0.82), (0.05, 0.98),
                                    (0.85, 0.98))]))],
             [(0, 0.21, 0.14, 0.5), (1, 0.51, 0.14, 0.7),
              (3, 0.51, 0.40, 0.4),
              (2, 0.19, 0.86, 0.6)])
    # "2": small loop at the bottom-left, base swinging out to the right
    two_L = ([(1.0, np.vstack([arc(0.36, 0.27, 0.30, 0.27, 175, -35, 22),
                               poly((0.45, 0.62), (0.25, 0.82), (0.08, 0.96),
                                    (0.02, 0.88), (0.08, 0.78), (0.20, 0.78),
                                    (0.30, 0.86), (0.45, 0.95), (0.65, 1.0),
                                    (0.88, 0.95))]))],
             [(0, 0.21, 0.14, 0.5), (1, 0.51, 0.14, 0.7), (3, 0.51, 0.40, 0.4),
              (0, 0.12, 0.86, 0.4), (1, 0.12, 0.86, 0.4),
              (2, 0.12, 0.86, 0.4), (3, 0.12, 0.86, 0.4)])
    # "2": big round top reaching below mid-height, straight neck, flat base
    two_R = ([(1.0, np.vstack([arc(0.38, 0.33, 0.32, 0.33, 180, -45, 24),
                               poly((0.05, 0.98), (0.85, 0.98))]))],
             [(0, 0.22, 0.17, 0.4), (1, 0.54, 0.17, 0.6), (3, 0.54, 0.50, 0.4),
              (2, 0.19, 0.86, 0.6)])
    # "3": two round bowls
    three_A = ([(1.0, arc(0.30, 0.235, 0.30, 0.235, 150, -90, 24)),
                (1.0, arc(0.30, 0.735, 0.36, 0.265, 90, -150, 24))],
               [(0, 0.15, 0.12, 0.35), (1, 0.45, 0.12, 0.8), (3, 0.45, 0.35, 0.8),
                (1, 0.48, 0.60, 0.7), (3, 0.48, 0.87, 0.7), (2, 0.12, 0.87, 0.3)])
    # "3": small upper bowl, middle bar reaching left, big lower bowl
    three_M = ([(1.0, np.vstack([arc(0.34, 0.20, 0.26, 0.20, 160, -90, 20),
                                 poly((0.15, 0.40))])),
                (1.0, arc(0.30, 0.70, 0.38, 0.30, 90, -160, 24))],
               [(0, 0.21, 0.10, 0.35), (1, 0.47, 0.10, 0.8), (3, 0.47, 0.30, 0.8),
                (1, 0.49, 0.55, 0.7), (3, 0.49, 0.85, 0.7), (2, 0.11, 0.85, 0.3)])
    # "4": left stroke, cross bar, right stem (open top)
    four = ([(1.0, poly((0.20, 0.0), (0.02, 0.58))),
             (1.0, poly((0.02, 0.58), (0.80, 0.58))),
             (1.0, poly((0.63, 0.0), (0.52, 1.0)))],
            [(2, 0.16, 0.46, 0.8),
             (3, 0.43, 0.46, 0.8),
             (1, 0.43, 0.72, 0.7),
             (2, 0.70, 0.47, 0.4),
             (0, 0.68, 0.70, 0.4)])
    # "5": top bar, short down stroke, bowl
    five = ([(1.0, np.vstack([poly((0.78, 0.0), (0.22, 0.04), (0.12, 0.42)),
                              arc(0.30, 0.69, 0.36, 0.31, 130, -150, 28)]))],
            [(0, 0.34, 0.16, 0.8),
             (2, 0.24, 0.33, 0.6),
             (1, 0.48, 0.535, 0.7), (3, 0.48, 0.845, 0.7),
             (0, 0.14, 0.55, 0.3), (2, 0.12, 0.845, 0.3)])
    # "6": steep stem down the left side, closed loop at the bottom
    six = ([(1.0, np.vstack([poly((0.50, 0.0), (0.36, 0.15), (0.22, 0.33),
                                  (0.12, 0.52), (0.08, 0.72)),
                             arc(0.34, 0.73, 0.26, 0.26, 180, 540, 40)]))],
           [(0, 0.21, 0.60, 0.7), (1, 0.47, 0.60, 0.7),
            (2, 0.21, 0.86, 0.7), (3, 0.47, 0.86, 0.7),
            (2, 0.30, 0.38, 0.5)])
    # "7": top bar, long diagonal; optional cross bar and optional left serif
    seven = ([(1.0, poly((0.0, 0.02), (0.72, 0.0))),
              (1.0, poly((0.72, 0.0), (0.30, 1.0))),
              (0.2, poly((0.25, 0.52), (0.70, 0.52))),
              (0.3, poly((0.0, 0.02), (0.0, 0.18)))],
             [(1, 0.56, 0.14, 0.8),
              (0, 0.12, 0.14, 0.25)])
    # "8": figure-eight
    t8 = np.linspace(0.0, 2.0 * math.pi, 64)
    x8 = 0.33 + (0.29 - 0.03 * np.sin(t8)) * np.sin(2 * t8)
    y8 = 0.5 - 0.5 * np.sin(t8)
    eight = ([(1.0, np.stack([x8, y8], axis=1))],
             [(0, 0.21, 0.14, 0.7), (1, 0.45, 0.14, 0.7),
              (2, 0.23, 0.34, 0.6), (3, 0.43, 0.34, 0.6),
              (0, 0.20, 0.66, 0.6), (1, 0.46, 0.66, 0.6),
              (2, 0.19, 0.86, 0.7), (3, 0.47, 0.86, 0.7),
              (1, 0.12, 0.50, 0.3), (3, 0.12, 0.50, 0.3),
              (0, 0.54, 0.50, 0.3), (2, 0.54, 0.50, 0.3)])
    # "9": loop at the top, stem down the right side
    nine = ([(1.0, arc(0.33, 0.27, 0.28, 0.27, 0, 360, 40)),
             (1.0, poly((0.61, 0.20), (0.60, 0.50), (0.50, 1.0)))],
            [(0, 0.19, 0.135, 0.7), (1, 0.47, 0.135, 0.7),
             (2, 0.19, 0.405, 0.7), (3, 0.47, 0.405, 0.7),
             (1, 0.42, 0.68, 0.6)])

    def generic(shape, base_shear):
        # untested digits: narrow-upright / medium / wide-slanted versions
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

    def place(shape, wx, shear):
        # stretch x, apply slant, scale skeleton to SKEL px, centre of mass at CEN;
        # the corner annotations go through the same mapping
        strokes, corners = shape
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
        placed_strokes = [(w, (p - com) * scale + CEN) for w, p in sh]
        placed_corners = []
        for (t, x, y, s) in corners:
            xx = x * wx + shear * (0.5 - y)
            placed_corners.append((t, (xx - com[0]) * scale + CEN,
                                   (y - com[1]) * scale + CEN, s))
        return placed_strokes, placed_corners

    # ------------------------------------------------------------------
    # Templates drawn directly in feature space.
    # ------------------------------------------------------------------
    cell_c = 4.0 * np.arange(4) + 7.5

    def win(t):
        # orientation cells: full weight within 3 px, fading to 0 at 6 px
        return np.clip((6.0 - np.abs(t)) / 3.0, 0.0, 1.0)

    def cwin(t):
        # corner cells (4 px wide): full weight within 2 px, fading to 0 at 5 px
        return np.clip((5.0 - np.abs(t)) / 3.0, 0.0, 1.0)

    def render(strokes):
        # P[k, a, b] = "probability" that orientation k is present in cell (a, b)
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

    def render_corners(corners):
        # PC[t, a, b] = "probability" that a corner of type t shows up in cell (a, b)
        notp = np.ones((4, 4, 4), dtype=np.float64)
        for (t, x, y, s) in corners:
            notp[t] *= (1.0 - s * np.outer(cwin(y - cell_c), cwin(x - cell_c)))
        return 1.0 - notp

    # ------------------------------------------------------------------
    # fc: log-odds template matching on orientation features (channels 0..7)
    # and on corner maps (channels 12..15). Class template = mix of its variants.
    # ------------------------------------------------------------------
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    fc_bc = np.zeros((10,), dtype=np.float64)
    for d in range(10):
        P = np.zeros((4, 4, 4), dtype=np.float64)
        PC = np.zeros((4, 4, 4), dtype=np.float64)
        tot = 0.0
        for pi, shape, wx, shear in digit_variants[d]:
            ps, pc = place(shape, wx, shear)
            P += pi * render(ps)
            PC += pi * render_corners(pc)
            tot += pi
        P /= tot
        PC /= tot
        # orientation part
        P = P_LO + (P_HI - P_LO) * P
        lo = np.log(P / (1.0 - P))
        fc_b[d] = S_TEMP * np.log(1.0 - P).sum()
        # corner part
        PC = PC_LO + (PC_HI - PC_LO) * PC
        loc = np.log(PC / (1.0 - PC))
        fc_bc[d] = S_C * np.log(1.0 - PC).sum()
        for k in range(4):
            for a in range(4):
                for b in range(4):
                    wgt = S_TEMP * lo[k, a, b] / CLIP
                    fc_w[d, k * 16 + a * 4 + b] = wgt
                    fc_w[d, (k + 4) * 16 + a * 4 + b] = -wgt
                    fc_w[d, (12 + k) * 16 + a * 4 + b] = S_C * loc[k, a, b] / C_TYP
    fc_b -= fc_b.mean()
    fc_bc -= fc_bc.mean()
    fc_b += fc_bc + BIAS_ADJ

    # ------------------------------------------------------------------
    # fc: loop features (channels 8..11). Final rows 0,1 = loop in the upper half,
    # rows 2,3 = loop in the lower half.
    # logit_d += GAMMA * (HOLE_NONE[d] + HOLE_GAIN*(HOLE_UP[d]*H_up + HOLE_LO[d]*H_lo))
    # ------------------------------------------------------------------
    for d in range(10):
        for ch in range(8, 12):
            for a in range(4):
                for b in range(4):
                    v = HOLE_UP[d] if a < 2 else HOLE_LO[d]
                    fc_w[d, ch * 16 + a * 4 + b] = GAMMA * HOLE_GAIN * v
        fc_b[d] += GAMMA * HOLE_NONE[d]

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
