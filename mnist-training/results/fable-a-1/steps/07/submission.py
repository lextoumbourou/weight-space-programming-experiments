import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: tournament between hand-drawn variants of "2" and "3".
    #   outputs 0..4 : "2" variants (base, wider, bottom loop, big round top, narrow upright)
    #   outputs 5..9 : "3" variants (base, wider, flat top, long middle bar, narrow upright)
    # ------------------------------------------------------------------
    S_TEMP = 0.2
    T0 = 0.25
    CLIP = 1.2
    C1_BIAS = -0.1
    L0 = 3.0
    P_LO, P_HI = 0.08, 0.92
    CEN = 13.5
    SKEL = 17.5
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
    # hand-drawn shapes (x, y), y from 0 (top) to 1 (bottom)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        t = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], axis=1)

    def poly(*pts):
        return np.array(pts, dtype=np.float64)

    # "2": hooked top arc, curved neck to bottom-left, flat wide base
    two_A = [(1.0, np.vstack([arc(0.36, 0.27, 0.30, 0.27, 175, -35, 22),
                              poly((0.45, 0.62), (0.22, 0.82), (0.05, 0.98),
                                   (0.85, 0.98))]))]
    # "2": same top, small loop at the bottom-left, base swinging out to the right
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
    # "3": flat top bar, diagonal to the waist, round lower bowl
    three_F = [(1.0, poly((0.05, 0.02), (0.62, 0.0), (0.30, 0.42))),
               (1.0, arc(0.30, 0.71, 0.36, 0.29, 90, -150, 24))]
    # "3": small upper bowl, middle bar reaching left, big lower bowl
    three_M = [(1.0, np.vstack([arc(0.34, 0.20, 0.26, 0.20, 160, -90, 20),
                                poly((0.15, 0.40))])),
               (1.0, arc(0.30, 0.70, 0.38, 0.30, 90, -160, 24))]

    # variants: (strokes, x-stretch, shear)
    variants = [
        (two_A, 1.0, 0.20),     # 0: "2" base
        (two_A, 1.2, 0.20),     # 1: "2" wider
        (two_L, 1.0, 0.20),     # 2: "2" with bottom loop
        (two_R, 1.0, 0.20),     # 3: "2" big round top
        (two_A, 0.8, 0.05),     # 4: "2" narrow, upright
        (three_A, 1.0, 0.20),   # 5: "3" base
        (three_A, 1.25, 0.20),  # 6: "3" wider
        (three_F, 1.0, 0.20),   # 7: "3" flat top
        (three_M, 1.0, 0.20),   # 8: "3" long middle bar
        (three_A, 0.8, 0.05),   # 9: "3" narrow, upright
    ]

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

    # fc: log-odds template matching where the 10 "classes" are the 10 variants
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for d in range(10):
        strokes, wx, shear = variants[d]
        P = render(place(strokes, wx, shear))
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
