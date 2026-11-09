import numpy as np
import math


def build_weights():
    ANG = [0.0, 45.0, 90.0, 135.0]   # orientation index: 0=H "-", 1=D1 "/", 2=V "|", 3=D2 "\"

    # ------------------------------------------------------------------
    # conv1: 4 oriented bar detectors, each with two biases, so that after
    # ReLU+maxpool  S_o = chan(2o) - chan(2o+1) = clip((resp-T0)/(T1-T0),0,1)
    # is a saturated "stroke of orientation o is here" map (12x12).
    # ------------------------------------------------------------------
    T0, T1 = 1.5, 3.5
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
                d = abs(u * math.sin(th) + v * math.cos(th))
                k[r, c] = (1.0 - d * d / (sig * sig)) * math.exp(-d * d / (2 * sig * sig))
        k = k - k.mean()
        c1w[2 * o, 0] = k / (T1 - T0)
        c1w[2 * o + 1, 0] = k / (T1 - T0)
        c1b[2 * o] = -T0 / (T1 - T0)
        c1b[2 * o + 1] = -T1 / (T1 - T0)

    # ------------------------------------------------------------------
    # conv2: 4 banks x 4 orientations, each channel a single tap on S_o.
    # After the 2x2 max-pool, cell (i,j) of a bank with tap (ca,cb) says
    # "a stroke of orientation o is present in the 4x4 px box centred at
    #  row 4i+2ca+3.5, col 4j+2cb+3.5"  (value in [0,1]).
    # The banks are shifted by half a cell against each other.
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    BANKS = [(1, 1), (3, 2), (2, 2), (2, 1)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            c2w[4 * bi + o, 2 * o, ca, cb] = 1.0
            c2w[4 * bi + o, 2 * o + 1, ca, cb] = -1.0

    # ------------------------------------------------------------------
    # Hand-drawn digit prototypes: strokes in a nominal frame
    # (x right, y down, digit height 0..20, x centred near 0).
    # Each stroke: (polyline points, weight).  Weight ~0.3-0.5 = optional
    # stroke (present in some writing styles only).
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1):
        n = max(2, int(abs(a1 - a0) / 6.0) + 1)
        pts = []
        for k in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        return pts

    protos = {}
    # 0: ellipse
    protos[0] = [(arc(0, 10, 6.5, 10, -180, 180), 1.0)]
    # 1: vertical stroke; optional: more slanted variant, flag at the top, base
    protos[1] = [([(0, 0), (0, 20)], 1.0),
                 ([(3, 0), (-3, 20)], 0.5),
                 ([(0, 0), (-3, 3.5)], 0.35),
                 ([(-3.5, 20), (3.5, 20)], 0.3)]
    # 2: top arc, diagonal to the bottom-left, base; optional up-curl at the end
    a2 = arc(0, 5.5, 5, 5.5, -170, 40)
    protos[2] = [(a2, 1.0),
                 ([a2[-1], (-5.5, 20)], 1.0),
                 ([(-5.5, 20), (6, 20)], 1.0),
                 ([(6, 20), (7, 17.5)], 0.4)]
    # 3: two arcs open to the left
    protos[3] = [(arc(-0.5, 5, 5, 5, -150, 90), 1.0),
                 (arc(-0.5, 15, 5.5, 5, -90, 150), 1.0)]
    # 4: left stroke, cross bar, right vertical
    protos[4] = [([(-3, 0), (-5.5, 11)], 1.0),
                 ([(-5.5, 11), (6.5, 11)], 1.0),
                 ([(2.5, 0), (2.5, 20)], 1.0)]
    # 5: top bar, short vertical, belly
    protos[5] = [([(5.5, 0), (-3.5, 0)], 1.0),
                 ([(-3.5, 0), (-4.5, 8.5)], 1.0),
                 (arc(-0.5, 13.5, 5.5, 6.5, -135, 150), 1.0)]
    # 6: spine from the top right down the left side, loop at the bottom
    protos[6] = [([(3.5, 0), (0.5, 3.5), (-2.5, 7.5), (-4.3, 11.5), (-5, 14.5)], 1.0),
                 (arc(0, 14.5, 5, 5.5, -180, 180), 1.0)]
    # 7: top bar, diagonal stem; optional: tick at the left end, cross bar
    protos[7] = [([(-6, 0), (5.5, 0)], 1.0),
                 ([(5.5, 0), (-1, 20)], 1.0),
                 ([(-6, 0), (-6, 3)], 0.4),
                 ([(-1.5, 10), (5, 10)], 0.35)]
    # 8: figure-eight (diagonals crossing in the middle), smaller top lobe
    eight = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        a8 = 4.2 if math.cos(t) > 0 else 5.0
        eight.append((a8 * math.sin(2 * t), 10 - 10 * math.cos(t)))
    protos[8] = [(eight, 1.0)]
    # 9: loop on top, stem on the right
    protos[9] = [(arc(-0.5, 5.5, 4.5, 5.5, -180, 180), 1.0),
                 ([(4.2, 3), (3, 20)], 1.0)]

    def densify(P, w, out):
        # polyline -> samples [x, y, orientation(deg), weight, length]
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
                out.append([xa + (xb - xa) * f, ya + (yb - ya) * f, th, w, L / n])

    def prep(strokes, shear=0.15):
        # slant right, scale centre-line box to 17.5 px (ink box ~20),
        # centre of mass to (13.5, 13.5) -- same normalisation as MNIST
        S = []
        xs = []
        ys = []
        for (pts, w) in strokes:
            P = [(x + shear * (10.0 - y), y) for (x, y) in pts]
            S.append((P, w))
            if w >= 0.99:                      # box from the main strokes only
                xs += [p[0] for p in P]
                ys += [p[1] for p in P]
        scale = 17.5 / max(max(xs) - min(xs), max(ys) - min(ys))
        samples = []
        for (P, w) in S:
            P = [(x * scale, y * scale) for (x, y) in P]
            densify(P, w, samples)
        tot = sum(s[3] * s[4] for s in samples)
        mx = sum(s[0] * s[3] * s[4] for s in samples) / tot
        my = sum(s[1] * s[3] * s[4] for s in samples) / tot
        for s in samples:
            s[0] += 13.5 - mx
            s[1] += 13.5 - my
        return np.array(samples, dtype=np.float64)

    # ------------------------------------------------------------------
    # Paint a prototype into the 16x4x4 feature space as an expected
    # presence map in [0,1] (by formula; a long stroke through a box centre
    # gives 1, falling off with distance like a Gaussian of sigma 2.6 px).
    # ------------------------------------------------------------------
    sigT = 2.6
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))

    def template(samples):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        x = samples[:, 0]
        y = samples[:, 1]
        th = samples[:, 2]
        wl = samples[:, 3] * samples[:, 4]
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
        return np.clip(T, 0.0, 1.0)

    # ------------------------------------------------------------------
    # fc: Bernoulli (naive-Bayes style) template per class.
    #   p = EPS + (1-2*EPS)*T   expected presence probability of each feature
    #   weight = log(p/(1-p)),  bias = sum(log(1-p))
    # so unexpected ink and missing expected strokes both count against a class;
    # T ~ 0.5 (optional strokes) is neutral.
    # ------------------------------------------------------------------
    EPS = 0.2
    ALPHA = 0.08
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for dgt in range(10):
        T = template(prep(protos[dgt])).reshape(-1)     # (channel, row, col) order
        p = EPS + (1.0 - 2.0 * EPS) * T
        fcw[dgt] = ALPHA * np.log(p / (1.0 - p))
        fcb[dgt] = ALPHA * float(np.sum(np.log(1.0 - p)))
    fcb = fcb - fcb.mean()

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
