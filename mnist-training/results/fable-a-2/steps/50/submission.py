import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1
    #   channels 0..3: oriented line detectors (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\")
    #   channels 4..7: polarity edge detectors
    #       4: ink to the RIGHT   5: ink to the LEFT   6: ink BELOW   7: ink ABOVE
    # ------------------------------------------------------------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    yy, xx = np.mgrid[-2:3, -2:3].astype(float)
    for k in range(4):
        phi = k * math.pi / 4.0
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))
        g = np.exp(-d ** 2 / 2.0)
        g = g - g.mean()
        g = g / g[g > 0].sum()
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05
    c = np.array([-0.5, -1.0, 0.0, 1.0, 0.5])   # derivative profile across the edge
    r = np.array([0.5, 1.0, 1.0, 1.0, 0.5])     # smoothing along the edge
    conv1_w[4, 0] = np.outer(r, c) / 6.0        # ink right
    conv1_w[5, 0] = -np.outer(r, c) / 6.0       # ink left
    conv1_w[6, 0] = np.outer(c, r) / 6.0        # ink below
    conv1_w[7, 0] = -np.outer(c, r) / 6.0       # ink above
    conv1_b[4:8] = -0.1

    # ------------------------------------------------------------------
    # conv2 channels 0..3: smoothed orientation maps (grid A)
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3

    # ------------------------------------------------------------------
    # Loci feature kernels, f = 0..5 (each stored as a pair ReLU(z), ReLU(z-CLIP)):
    #   0: wall on the right, left ray open        1: wall on the left, right ray open
    #   2: floor below, ray upwards open           3: ceiling above, ray downwards open
    #   4: walls left AND right                    5: walls above AND below
    # ------------------------------------------------------------------
    K = np.zeros((6, 8, 5, 5))
    KB = np.zeros(6)
    lat = (0.25, 0.5, 0.25)     # lateral smoothing across the ray
    KINH = 1.5                  # veto strength

    def block_R(f):
        for a, wl in zip((1, 2, 3), lat):
            for b in (2, 3, 4):
                K[f, 4, a, b] += wl

    def block_L(f):
        for a, wl in zip((1, 2, 3), lat):
            for b in (0, 1, 2):
                K[f, 5, a, b] += wl

    def block_D(f):
        for b, wl in zip((1, 2, 3), lat):
            for a in (2, 3, 4):
                K[f, 6, a, b] += wl

    def block_U(f):
        for b, wl in zip((1, 2, 3), lat):
            for a in (0, 1, 2):
                K[f, 7, a, b] += wl

    def veto(f, cells, chans, strength=1.0):
        for (a, b) in cells:
            for cc in chans:
                K[f, cc, a, b] -= KINH * strength

    LINES = (0, 1, 2, 3)
    block_R(0)
    veto(0, [(2, 0), (2, 1)], (2, 4, 5)); veto(0, [(2, 0), (2, 1)], (1, 3), 0.5)
    veto(0, [(2, 2)], LINES); veto(0, [(2, 2)], (5,))
    block_L(1)
    veto(1, [(2, 3), (2, 4)], (2, 4, 5)); veto(1, [(2, 3), (2, 4)], (1, 3), 0.5)
    veto(1, [(2, 2)], LINES); veto(1, [(2, 2)], (4,))
    block_D(2)
    veto(2, [(0, 2), (1, 2)], (0, 6, 7)); veto(2, [(0, 2), (1, 2)], (1, 3), 0.5)
    veto(2, [(2, 2)], LINES); veto(2, [(2, 2)], (7,))
    block_U(3)
    veto(3, [(3, 2), (4, 2)], (0, 6, 7)); veto(3, [(3, 2), (4, 2)], (1, 3), 0.5)
    veto(3, [(2, 2)], LINES); veto(3, [(2, 2)], (6,))
    KB[0:4] = -0.4
    block_L(4); block_R(4); veto(4, [(2, 2)], LINES)
    block_U(5); block_D(5); veto(5, [(2, 2)], LINES)
    KB[4:6] = -1.9

    CLIP = 0.4
    for f in range(6):
        conv2_w[4 + 2 * f] = K[f]
        conv2_b[4 + 2 * f] = KB[f]
        conv2_w[5 + 2 * f] = K[f]
        conv2_b[5 + 2 * f] = KB[f] - CLIP

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (unit coords: x right, y down, height = 1).
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=48):
        a = np.radians(np.linspace(a0, a1, n))
        return list(zip(cx + rx * np.cos(a), cy - ry * np.sin(a)))  # 90deg = top

    def eight():
        tt = np.linspace(0.0, 2.0 * math.pi, 97)
        return list(zip(0.25 * np.sin(2 * tt), 0.5 - 0.5 * np.cos(tt)))

    digits = {
        0: [(1.0, arc(0.0, 0.5, 0.33, 0.5, 0, 360, 72))],
        1: [(1.0, [(0.0, 0.0), (0.0, 1.0)]),
            (0.4, [(0.2, 0.0), (-0.2, 1.0)])],                  # slanted variant
        2: [(1.0, arc(0.0, 0.27, 0.27, 0.27, 160, -30)),         # top hook
            (1.0, [(0.234, 0.405), (-0.3, 0.97)]),               # diagonal sweep
            (1.0, [(-0.3, 0.97), (0.35, 0.97)])],                # base
        3: [(1.0, arc(0.0, 0.25, 0.27, 0.25, 150, -90)),         # upper bowl
            (1.0, arc(0.0, 0.74, 0.30, 0.26, 90, -150))],        # lower bowl
        4: [(1.0, [(-0.25, 0.0), (-0.30, 0.55)]),                # left stroke
            (1.0, [(-0.30, 0.55), (0.38, 0.55)]),                # crossbar
            (1.0, [(0.12, 0.0), (0.12, 1.0)])],                  # main vertical
        5: [(1.0, [(0.30, 0.0), (-0.20, 0.0)]),                  # top bar
            (1.0, [(-0.20, 0.0), (-0.22, 0.42)]),                # short vertical
            (1.0, arc(0.0, 0.68, 0.30, 0.30, 135, -150))],       # bowl
        6: [(1.0, arc(0.30, 0.62, 0.55, 0.62, 100, 180)),        # long left curve from top
            (1.0, arc(0.0, 0.72, 0.25, 0.27, 0, 360, 60))],      # bottom loop
        7: [(1.0, [(-0.30, 0.0), (0.30, 0.0)]),                  # top bar
            (1.0, [(0.30, 0.0), (0.0, 1.0)]),                    # diagonal
            (0.25, [(-0.05, 0.5), (0.30, 0.5)])],                # optional crossbar
        8: [(1.0, eight())],
        9: [(1.0, arc(0.0, 0.27, 0.24, 0.27, 0, 360, 60)),       # top loop
            (1.0, [(0.24, 0.25), (0.20, 1.0)])],                 # stem
    }

    SHEAR = 0.10          # typical right slant of handwriting
    BOX = 17.5            # centre-line extent in pixels (20px box minus stroke thickness)

    def raw(strokes):
        rec = []
        for w, pts in strokes:
            for a, b in zip(pts[:-1], pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                ln = math.hypot(dx, dy)
                if ln < 1e-9:
                    continue
                n = max(1, int(math.ceil(ln / 0.02)))
                for s in range(n):
                    tt = (s + 0.5) / n
                    x = a[0] + dx * tt
                    y = a[1] + dy * tt
                    rec.append((x + SHEAR * (0.5 - y), y,
                                math.atan2(-dy, dx - SHEAR * dy), w * ln / n))
        return np.array(rec, dtype=float).reshape(-1, 4)

    def foot(dist):
        return np.clip((6.0 - dist) / 4.0, 0.0, 1.0)

    centA = 7.5 + 4.0 * np.arange(4)     # pixel centres of grid A cells

    def deposit(X, Y, TH, L):
        T = np.zeros((16, 4, 4))
        fy = foot(np.abs(Y[:, None] - centA[None, :]))
        fx = foot(np.abs(X[:, None] - centA[None, :]))
        for k in range(4):
            rr = np.maximum(0.0, np.cos(2.0 * (TH - k * math.pi / 4.0)))  # orientation tuning
            T[k] = np.einsum('n,ni,nj->ij', L * rr, fy, fx) / 7.5
        return T

    # ------------------------------------------------------------------
    # Measured presence rates P(loci feature present in region | digit) from the probe steps.
    # (feature f, rows of region, rates for digits 0..9); region columns are always 1-2.
    # ------------------------------------------------------------------
    table = [
        (0, (0, 1), [.60, .995, .825, .37, .39, .19, .54, .63, .28, .11]),
        (1, (0, 1), [.48, .59, .083, .118, .20, .52, .83, .042, .08, .066]),
        (2, (0, 1), [.27, .09, .42, .07, .70, .38, .51, .76, .12, .44]),
        (3, (0, 1), [.725, .009, .428, .058, .0, .153, .037, .668, .006, .05]),
        (4, (0, 1), [.32, .0, .024, .004, .40, .001, .07, .038, .04, .10]),
        (5, (0, 1), [.06, .0, .43, .45, .006, .40, .09, .07, .26, .29]),
        (0, (2, 3), [.61, .945, .32, .74, .80, .60, .033, .95, .37, .90]),
        (1, (2, 3), [.69, .964, .21, .057, .44, .18, .074, .58, .42, .39]),
        (2, (2, 3), [.77, .027, .42, .31, .12, .26, .11, .08, .03, .053]),
        (3, (2, 3), [.14, .065, .50, .26, .84, .32, .16, .62, .12, .63]),
        (4, (2, 3), [.27, .0, .007, .002, .025, .008, .135, .023, .056, .019]),
        (5, (2, 3), [.21, .002, .14, .71, .008, .59, .14, .04, .16, .057]),
    ]

    # ------------------------------------------------------------------
    # Measured stroke-energy statistics (the step-42 set):
    # (orientation channel, rows, cols, class means for digits 0..9, common spread, weight)
    # ------------------------------------------------------------------
    line_stats = [
        # horizontal energy at top-centre
        (0, (0,), (1, 2), [1.04, 0.05, 1.09, 1.35, 0.05, 1.27, 0.22, 1.58, 1.19, 1.32], 0.40, 1.0),
        # vertical energy, lower-right quadrant
        (2, (2, 3), (2, 3), [1.39, 1.43, 1.17, 1.83, 1.83, 1.63, 1.38, 1.89, 1.56, 1.99], 0.52, 0.5),
        # horizontal energy at bottom-centre
        (0, (3,), (1, 2), [1.3, 0.1, 1.18, 1.09, 0.45, 1.085, 1.3, 0.1, 0.71, 0.21], 0.42, 0.7),
        # "\" energy at the centre (two rows)
        (3, (1, 2), (1, 2), [0.89, 0.53, 1.14, 1.64, 1.28, 1.85, 1.31, 1.03, 2.0, 1.39], 0.40, 0.3),
        # "/" energy at the centre (two rows)
        (1, (1, 2), (1, 2), [1.65, 1.74, 2.1, 2.4, 1.9, 1.47, 2.4, 1.8, 2.6, 2.4], 0.80, 0.3),
        # vertical energy at the centre (two rows)
        (2, (1, 2), (1, 2), [1.04, 2.2, 1.285, 1.29, 1.78, 1.38, 1.68, 1.52, 1.98, 1.74], 0.50, 0.5),
        # horizontal energy at bottom-right
        (0, (3,), (2, 3), [0.97, 0.05, 1.07, 0.72, 0.18, 0.67, 1.10, 0.05, 0.35, 0.05], 0.40, 1.0),
        # --- single-row terms ---
        # vertical energy, row 1, left  (upper-left segment)
        (2, (1,), (0, 1), [1.006, 0.42, 0.21, 0.124, 1.0, 0.803, 1.085, 0.356, 0.895, 1.01], 0.35, 1.0),
        # vertical energy, row 1, right (upper-right segment)
        (2, (1,), (2, 3), [0.926, 1.3, 1.146, 0.866, 1.3, 0.266, 0.441, 1.21, 0.764, 1.26], 0.35, 1.0),
        # vertical energy, row 2, left  (lower-left segment)
        (2, (2,), (0, 1), [1.216, 0.864, 0.364, 0.075, 0.78, 0.545, 1.415, 0.234, 0.804, 0.725], 0.35, 1.0),
        # vertical energy, row 2, right (lower-right segment; weak)
        (2, (2,), (2, 3), [0.861, 0.948, 0.793, 1.027, 1.106, 0.834, 0.828, 1.139, 0.783, 1.217], 0.35, 1.0),
        # horizontal energy, row 1, centre
        (0, (1,), (1, 2), [0.33, 0.05, 0.306, 1.045, 0.494, 0.992, 0.525, 0.963, 0.633, 0.741], 0.35, 0.6),
        # horizontal energy, row 2, centre
        (0, (2,), (1, 2), [0.056, 0.05, 0.829, 0.861, 1.28, 0.836, 0.783, 0.202, 0.677, 1.087], 0.35, 0.8),
        # "/" energy, row 1, right
        (1, (1,), (2, 3), [0.53, 0.629, 0.957, 1.078, 0.978, 0.473, 0.843, 0.895, 1.21, 1.03], 0.35, 1.0),
        # "/" energy, row 2, left
        (1, (2,), (0, 1), [0.825, 0.577, 0.945, 0.754, 0.774, 0.635, 0.82, 0.43, 1.035, 0.644], 0.35, 1.0),
        # "\" energy, row 1, left
        (3, (1,), (0, 1), [0.02, 0.02, 0.108, 0.344, 0.462, 0.625, 0.206, 0.169, 0.879, 0.642], 0.35, 1.0),
        # "\" energy, row 2, right
        (3, (2,), (2, 3), [0.056, 0.02, 0.556, 1.162, 0.426, 0.98, 0.727, 0.04, 0.777, 0.249], 0.35, 1.0),
        # "/" energy, row 2, right
        (1, (2,), (2, 3), [1.0, 0.58, 1.176, 0.644, 0.973, 0.456, 1.06, 1.12, 0.924, 0.985], 0.35, 1.0),
        # "/" energy, row 1, left
        (1, (1,), (0, 1), [1.286, 0.145, 0.517, 0.85, 0.911, 0.905, 1.06, 0.673, 0.64, 1.225], 0.35, 1.0),
        # vertical energy, row 0, left
        (2, (0,), (0, 1), [0.505, 0.299, 0.28, 0.174, 0.759, 0.529, 0.70, 0.214, 0.707, 0.39], 0.35, 1.0),
        # vertical energy, row 0, right
        (2, (0,), (2, 3), [0.77, 1.176, 1.076, 0.858, 1.045, 0.02, 0.377, 0.684, 0.753, 0.764], 0.35, 1.0),
        # vertical energy, row 3, centre (stems)
        (2, (3,), (1, 2), [0.367, 1.18, 0.368, 0.522, 1.011, 0.57, 0.685, 1.114, 1.117, 1.04], 0.35, 1.0),
        # "\" energy, row 1, right
        (3, (1,), (2, 3), [0.833, 0.02, 0.331, 0.80, 0.131, 0.682, 0.624, 0.59, 0.618, 0.609], 0.35, 1.0),
        # "\" energy, row 2, left
        (3, (2,), (0, 1), [0.34, 0.02, 0.385, 0.194, 0.804, 0.613, 0.666, 0.096, 0.689, 0.88], 0.35, 1.0),
        # horizontal energy, row 0, right
        (0, (0,), (2, 3), [1.069, 0.02, 0.735, 0.888, 0.065, 1.21, 0.248, 1.21, 1.087, 1.078], 0.35, 0.7),
        # horizontal energy, row 1, left
        (0, (1,), (0, 1), [0.269, 0.02, 0.30, 0.82, 0.454, 0.797, 0.024, 0.901, 0.366, 0.622], 0.35, 0.8),
        # horizontal energy, row 1, right
        (0, (1,), (2, 3), [0.22, 0.02, 0.152, 0.794, 0.291, 0.80, 0.705, 0.72, 0.597, 0.569], 0.35, 0.7),
        # "\" energy, row 0, right (rounded top-right corner)
        (3, (0,), (2, 3), [1.153, 0.02, 1.037, 0.855, 0.171, 0.201, 0.05, 0.641, 0.887, 0.948], 0.35, 1.0),
        # horizontal energy, row 3, left
        (0, (3,), (0, 1), [1.033, 0.02, 1.119, 0.889, 0.379, 0.889, 0.907, 0.05, 0.52, 0.289], 0.35, 0.8),
        # "/" energy, row 0, left (rounded top-left corner)
        (1, (0,), (0, 1), [1.176, 0.02, 0.84, 0.825, 0.759, 0.814, 0.986, 0.663, 0.954, 1.292], 0.35, 1.0),
        # horizontal energy, row 2, right
        (0, (2,), (2, 3), [0.163, 0.02, 0.695, 0.648, 0.916, 0.628, 0.897, 0.192, 0.43, 0.639], 0.35, 0.7),
        # horizontal energy, row 0, left
        (0, (0,), (0, 1), [0.514, 0.02, 0.799, 0.972, 0.02, 0.615, 0.02, 1.10, 0.651, 0.828], 0.35, 0.7),
        # "\" energy, row 3, left (rounded bottom-left)
        (3, (3,), (0, 1), [1.21, 0.02, 0.521, 0.695, 0.173, 0.793, 0.957, 0.02, 0.721, 0.187], 0.35, 1.0),
        # "/" energy, row 3, right (rounded bottom-right)
        (1, (3,), (2, 3), [1.405, 0.02, 0.757, 1.34, 0.595, 1.043, 1.23, 0.92, 0.772, 0.744], 0.35, 1.0),
        # "/" energy, row 3, left
        (1, (3,), (0, 1), [0.603, 0.61, 1.074, 0.509, 0.569, 0.568, 0.586, 0.654, 0.932, 0.534], 0.35, 1.0),
        # horizontal energy, row 2, left
        (0, (2,), (0, 1), [0.02, 0.02, 0.726, 0.676, 1.153, 0.71, 0.327, 0.178, 0.384, 1.017], 0.35, 0.8),
        # vertical energy, row 3, left
        (2, (3,), (0, 1), [0.957, 0.901, 0.569, 0.25, 0.489, 0.359, 0.901, 0.469, 1.087, 0.349], 0.35, 0.8),
    ]

    # ------------------------------------------------------------------
    # fc: stroke templates + loci log-odds table + calibrated stroke-energy terms
    # ------------------------------------------------------------------
    ALPHA = 4.85      # scale of the stroke-template match (5.0 in step 49)
    GAMMA = 0.52      # tempering of the loci log-odds (0.6 in step 49)
    GLINE = 0.6       # tempering of the stroke-energy terms
    NTYP = 1.6        # typical number of saturated cells when a loci feature is present
    SCALE = 0.445     # global confidence scale applied to all logits (fitted optimum)
    # class offsets (in units of scale 0.40), scaled along with the logits;
    # relative to step 49: class 2 slightly down, classes 0, 1 and 6 slightly up
    class_bias = np.array([0.67, 0.06, -0.08, -0.60, 1.17, -0.53, -0.36, 1.12, -1.13, -0.23])
    class_bias = class_bias * (SCALE / 0.40)
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros(10, dtype=np.float64)

    for d in range(10):
        P = raw(digits[d])
        ext = max(P[:, 0].max() - P[:, 0].min(), P[:, 1].max() - P[:, 1].min())
        sc = BOX / ext
        cx = (P[:, 0] * P[:, 3]).sum() / P[:, 3].sum()
        cy = (P[:, 1] * P[:, 3]).sum() / P[:, 3].sum()
        T = deposit((P[:, 0] - cx) * sc + 13.5, (P[:, 1] - cy) * sc + 13.5,
                    P[:, 2], P[:, 3] * sc)
        T = T / (np.linalg.norm(T) + 1e-9)
        fc_w[d] += ALPHA * T.reshape(-1)

    for (f, rows, rates) in table:
        p = np.clip(np.array(rates, dtype=float), 0.02, 0.98)
        lodds = np.log(p / (1.0 - p))
        lodds = lodds - lodds.mean()            # common shifts do not matter for softmax
        labs = np.log(1.0 - p)
        labs = labs - labs.mean()
        chA = 4 + 2 * f
        chB = 5 + 2 * f
        for d in range(10):
            w = GAMMA * lodds[d] / (CLIP * NTYP)
            for i in rows:
                for j in (1, 2):
                    fc_w[d, chA * 16 + i * 4 + j] += w     # + ReLU(z)
                    fc_w[d, chB * 16 + i * 4 + j] -= w     # - ReLU(z - CLIP)
            fc_b[d] += GAMMA * labs[d]

    for (ch, rows, cols, mus, sigma, mult) in line_stats:
        mu = np.array(mus, dtype=float)
        wl = mu / sigma ** 2                    # linear term of a Gaussian class model
        bl = -mu ** 2 / (2.0 * sigma ** 2)      # matching bias term
        wl = wl - wl.mean()
        bl = bl - bl.mean()
        for d in range(10):
            for i in rows:
                for j in cols:
                    fc_w[d, ch * 16 + i * 4 + j] += GLINE * mult * wl[d]
            fc_b[d] += GLINE * mult * bl[d]

    fc_w *= SCALE
    fc_b *= SCALE
    fc_b += class_bias

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
