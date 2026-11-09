import numpy as np
import math


def build_weights():
    ANG = [0.0, 45.0, 90.0, 135.0]   # orientation index: 0=H "-", 1=D1 "/", 2=V "|", 3=D2 "\"
    H, D1, V, D2 = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # conv1: 4 oriented bar detectors (zero-mean Mexican-hat profile across
    # the bar), each used with two biases.  After ReLU+maxpool,
    #   S_o = chan(2o) - chan(2o+1) = clip((resp - T0)/(T1 - T0), 0, 1)
    # is a saturated "stroke of orientation o is here" map (12x12).
    # ------------------------------------------------------------------
    T0, T1 = 1.5, 3.5          # ideal stroke gives raw response ~4-4.5
    sig = 1.2
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    for o in range(4):
        th = math.radians(ANG[o])
        k = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                u = c - 2.0
                v = r - 2.0
                d = abs(u * math.sin(th) + v * math.cos(th))   # distance from the bar axis
                k[r, c] = (1.0 - d * d / (sig * sig)) * math.exp(-d * d / (2 * sig * sig))
        k = k - k.mean()
        c1w[2 * o, 0] = k / (T1 - T0)
        c1w[2 * o + 1, 0] = k / (T1 - T0)
        c1b[2 * o] = -T0 / (T1 - T0)
        c1b[2 * o + 1] = -T1 / (T1 - T0)

    # ------------------------------------------------------------------
    # conv2
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    def put(ch, o, a, b, val):
        # weight 'val' on the saturated orientation map S_o at kernel tap (a,b)
        c2w[ch, 2 * o, a, b] += val
        c2w[ch, 2 * o + 1, a, b] -= val

    # channels 0-11: blurred orientation maps, 3 banks with different kernel centres
    # (bank centre (ca,cb) -> pooled cell (i,j) is centred at pixel
    #  row 4i+2ca+3.5, col 4j+2cb+3.5)
    BANKS = [(2, 2), (1, 2), (3, 2)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            for a in range(5):
                for b in range(5):
                    put(4 * bi + o, o, a, b,
                        0.32 * math.exp(-((a - ca) ** 2 + (b - cb) ** 2) / 2.0))

    # channels 12-15: stroke-ending detectors (stroke on one side, nothing beyond)
    # 12: tip pointing up, tip at kernel tap (1,2)
    ch = 12
    put(ch, V, 1, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 1, 2, 0.6); put(ch, D1, 2, 1, 0.4)     # "/" continues down-left
    put(ch, D2, 1, 2, 0.6); put(ch, D2, 2, 3, 0.4)     # "\" continues down-right
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 0, b, -1.0)                      # nothing may continue above
        put(ch, H, 1, b, -0.7)                          # no horizontal bar at the tip (corner)
    # 13: tip pointing down, tip at (3,2)
    ch = 13
    put(ch, V, 3, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 3, 2, 0.6); put(ch, D1, 2, 3, 0.4)     # "/" continues up-right
    put(ch, D2, 3, 2, 0.6); put(ch, D2, 2, 1, 0.4)     # "\" continues up-left
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 4, b, -1.0)
        put(ch, H, 3, b, -0.7)
    # 14: tip pointing left, tip at (2,1)
    ch = 14
    put(ch, H, 2, 1, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 0, -1.0)
        put(ch, V, a, 1, -0.7)
    # 15: tip pointing right, tip at (2,3)
    ch = 15
    put(ch, H, 2, 3, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 4, -1.0)
        put(ch, V, a, 3, -0.7)
    TIP_TAP = {12: (1, 2), 13: (3, 2), 14: (2, 1), 15: (2, 3)}

    # ------------------------------------------------------------------
    # Hand-drawn digit prototypes: strokes in a nominal frame
    # (x to the right, y downwards, digit height 0..20, x centred near 0).
    # Each stroke: (polyline points, weight, tip_at_start, tip_at_end)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1):
        # elliptical arc, angles in degrees, y down (-90 = top, 0 = right, 90 = bottom)
        n = max(2, int(abs(a1 - a0) / 6.0) + 1)
        pts = []
        for k in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        return pts

    protos = {}
    # 0: ellipse
    protos[0] = [(arc(0, 10, 6.5, 10, -180, 180), 1.0, False, False)]
    # 1: vertical stroke plus a fainter, more slanted variant
    protos[1] = [([(0, 0), (0, 20)], 1.0, True, True),
                 ([(3, 0), (-3, 20)], 0.5, True, True)]
    # 2: top arc, diagonal down to bottom-left, bottom bar
    a2 = arc(0, 5.5, 5, 5.5, -170, 40)
    protos[2] = [(a2, 1.0, True, False),
                 ([a2[-1], (-5.5, 20)], 1.0, False, False),
                 ([(-5.5, 20), (6, 20)], 1.0, False, True)]
    # 3: two arcs open to the left
    protos[3] = [(arc(-0.5, 5, 5, 5, -150, 90), 1.0, True, False),
                 (arc(-0.5, 15, 5.5, 5, -90, 150), 1.0, False, True)]
    # 4: left stroke, cross bar, right vertical
    protos[4] = [([(-3, 0), (-5.5, 11)], 1.0, True, False),
                 ([(-5.5, 11), (6.5, 11)], 1.0, False, True),
                 ([(2.5, 0), (2.5, 20)], 1.0, True, True)]
    # 5: top bar, short vertical, belly
    protos[5] = [([(5.5, 0), (-3.5, 0)], 1.0, True, False),
                 ([(-3.5, 0), (-4.5, 8.5)], 1.0, False, False),
                 (arc(-0.5, 13.5, 5.5, 6.5, -135, 150), 1.0, False, True)]
    # 6: spine from top-right down the left side, loop at the bottom
    protos[6] = [([(3.5, 0), (0.5, 3.5), (-2.5, 7.5), (-4.3, 11.5), (-5, 14.5)], 1.0, True, False),
                 (arc(0, 14.5, 5, 5.5, -180, 180), 1.0, False, False)]
    # 7: top bar, diagonal stem
    protos[7] = [([(-6, 0), (5.5, 0)], 1.0, True, False),
                 ([(5.5, 0), (-1, 20)], 1.0, False, True)]
    # 8: figure-eight (diagonals crossing in the middle), smaller top lobe
    eight = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        a8 = 4.2 if math.cos(t) > 0 else 5.0
        eight.append((a8 * math.sin(2 * t), 10 - 10 * math.cos(t)))
    protos[8] = [(eight, 1.0, False, False)]
    # 9: loop on top, stem on the right
    protos[9] = [(arc(-0.5, 5.5, 4.5, 5.5, -180, 180), 1.0, False, False),
                 ([(4.2, 3), (3, 20)], 1.0, False, True)]

    def prep(strokes, shear=0.15):
        # slant to the right, scale so the centre-line box is 17.5 px (ink box ~20),
        # move the centre of mass to (13.5, 13.5) -- same normalisation as MNIST.
        S = []
        xs = []
        ys = []
        for (pts, w, t0, t1) in strokes:
            P = [(x + shear * (10.0 - y), y) for (x, y) in pts]
            S.append((P, w, t0, t1))
            xs += [p[0] for p in P]
            ys += [p[1] for p in P]
        scale = 17.5 / max(max(xs) - min(xs), max(ys) - min(ys))
        samples = []   # [x, y, orientation(deg), weight*length]
        tips = []      # [x, y, outward dx, outward dy, weight]
        for (P, w, t0, t1) in S:
            P = [(x * scale, y * scale) for (x, y) in P]
            for k in range(len(P) - 1):
                xa, ya = P[k]
                xb, yb = P[k + 1]
                L = math.hypot(xb - xa, yb - ya)
                if L < 1e-9:
                    continue
                n = max(1, int(math.ceil(L / 0.5)))
                th = math.degrees(math.atan2(-(yb - ya), xb - xa)) % 180.0
                for q in range(n):
                    f = (q + 0.5) / n
                    samples.append([xa + (xb - xa) * f, ya + (yb - ya) * f, th, w * L / n])
            if t0:
                tips.append([P[0][0], P[0][1], P[0][0] - P[1][0], P[0][1] - P[1][1], w])
            if t1:
                tips.append([P[-1][0], P[-1][1], P[-1][0] - P[-2][0], P[-1][1] - P[-2][1], w])
        tot = sum(s[3] for s in samples)
        mx = sum(s[0] * s[3] for s in samples) / tot
        my = sum(s[1] * s[3] for s in samples) / tot
        for s in samples:
            s[0] += 13.5 - mx
            s[1] += 13.5 - my
        for t in tips:
            t[0] += 13.5 - mx
            t[1] += 13.5 - my
        return np.array(samples, dtype=np.float64), tips

    # ------------------------------------------------------------------
    # Paint a prototype directly into the 16x4x4 feature space (by formula)
    # ------------------------------------------------------------------
    sigT = 2.6                                     # effective blur of a pooled cell, px
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))     # long stroke through a cell centre -> 1

    def clip01(x):
        return min(1.0, max(0.0, x))

    def template(samples, tips):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        x = samples[:, 0]
        y = samples[:, 1]
        th = samples[:, 2]
        wl = samples[:, 3]
        tune = []
        for o in range(4):
            d = np.abs(th - ANG[o])
            d = np.minimum(d, 180.0 - d)
            tune.append(np.clip(1.3 * (1.0 - (d / 42.0) ** 2), 0.0, 1.0))  # orientation tuning
        for bi, (ca, cb) in enumerate(BANKS):
            for i in range(4):
                cy = 4 * i + 2 * ca + 3.5
                for j in range(4):
                    cx = 4 * j + 2 * cb + 3.5
                    g = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigT * sigT))
                    for o in range(4):
                        T[4 * bi + o, i, j] = cT * float(np.sum(wl * tune[o] * g))
        # stroke endings
        for (tx, ty, dx, dy, w) in tips:
            phi = math.degrees(math.atan2(abs(dy), abs(dx)))   # 0 = horizontal tip direction
            hw = clip01((50.0 - phi) / 25.0)
            vw = clip01((phi - 20.0) / 20.0)
            lst = []
            if vw > 0:
                lst.append((12 if dy < 0 else 13, vw))
            if hw > 0:
                lst.append((14 if dx < 0 else 15, hw))
            for (chn, ww) in lst:
                ta, tb = TIP_TAP[chn]
                for i in range(4):
                    cy = 4 * i + 2 * ta + 3.5
                    for j in range(4):
                        cx = 4 * j + 2 * tb + 3.5
                        T[chn, i, j] += w * ww * math.exp(
                            -((tx - cx) ** 2 + (ty - cy) ** 2) / (2 * 2.0 * 2.0))
        return T

    # ------------------------------------------------------------------
    # fc: unit-norm template per class (cosine matching), no bias
    # ------------------------------------------------------------------
    ALPHA = 3.0
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for dgt in range(10):
        samples, tips = prep(protos[dgt])
        T = template(samples, tips).reshape(-1)     # (channel, row, col) order
        fcw[dgt] = ALPHA * T / (np.linalg.norm(T) + 1e-9)

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
