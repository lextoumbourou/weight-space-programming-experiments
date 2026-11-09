import numpy as np, math

def build_weights():
    # =====================================================================
    # conv1: 8 hand-designed 5x5 filters
    #   ch0..3 : oriented bar (stroke) detectors  H(0deg), "/"(45), V(90), "\"(135)
    #   ch4..7 : stroke-ending detectors: free end pointing Left, Right, Up, Down
    # =====================================================================
    conv1_w = np.zeros((8, 1, 5, 5), np.float32)
    conv1_b = np.zeros(8, np.float32)

    def prof(v):
        # cross-stroke profile: positive ridge ~3px wide, negative flanks
        v = abs(v)
        if v <= 1.0:
            return 1.0 - 0.4 * v
        if v <= 2.0:
            return 0.6 - 1.7 * (v - 1.0)
        return -1.1

    odeg = [0.0, 45.0, 90.0, 135.0]
    for o, deg in enumerate(odeg):
        th = math.radians(deg)
        g = np.zeros((5, 5)); p = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                x = c - 2; y = r - 2                    # y is down
                u = x * math.cos(th) - y * math.sin(th)  # along the stroke
                v = x * math.sin(th) + y * math.cos(th)  # across the stroke
                g[r, c] = math.exp(-u * u / (2 * 2.5 ** 2))
                p[r, c] = prof(v)
        pbar = (g * p).sum() / g.sum()                  # make filter zero-sum
        w = g * (p - pbar)
        w = w / (0.8 * w[w > 0].sum())                  # typical stroke -> ~1
        conv1_w[o, 0] = w
        conv1_b[o] = -0.15                              # suppress weak off-orientation leak

    # ending detector: "end pointing left" = ink to the right of centre (3px thick bar),
    # background to the left, above and below.  Zero/negative for through-strokes and edges.
    prof3 = [0.5, 1.0, 0.5]
    EL = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            x = c - 2; y = r - 2
            if x >= 0:
                EL[r, c] = prof3[y + 1] if abs(y) <= 1 else -1.0
            else:
                EL[r, c] = -1.5 * prof3[y + 1] if abs(y) <= 1 else -0.5
    EL = EL / 4.0
    ER = EL[:, ::-1].copy()       # ink to the left  -> end pointing right
    EU = EL.T.copy()              # ink below        -> end pointing up
    ED = EU[::-1, :].copy()       # ink above        -> end pointing down
    for i, E in enumerate([EL, ER, EU, ED]):
        conv1_w[4 + i, 0] = E
        conv1_b[4 + i] = -0.25                          # corners give weak responses: cut them

    # =====================================================================
    # conv2: 16 channels = 8 feature types x 2 vertical offsets (a = 0, 1).
    # Channel (t, a) = ReLU(theta_t - S), S = sum of conv1 feature t over a
    # 4(rows) x 3(cols) patch of pooled cells.  After max-pool this equals
    # theta - min(S over the 4 shifted patches), clipped at 0: a SATURATED
    # "feature t is absent" indicator in [0, theta] for the window centred at
    # image row 6.5 + 2*m (m = 2k + a), image col 7.5 + 4*l.
    # =====================================================================
    theta_o = 1.2     # ~2.5-3 px of clear stroke saturates an orientation feature
    theta_e = 0.45    # one clear stroke end saturates an ending feature
    conv2_w = np.zeros((16, 8, 5, 5), np.float32)
    conv2_b = np.zeros(16, np.float32)
    for t in range(8):
        for a in range(2):
            k = np.zeros((5, 5))
            k[a:a + 4, 1:4] = -1.0
            conv2_w[2 * t + a, t] = k
            conv2_b[2 * t + a] = theta_o if t < 4 else theta_e

    # =====================================================================
    # fc: Bernoulli naive Bayes with hand-specified presence probabilities.
    # Probabilities come from pen strokes drawn in a unit box (x right, y down,
    # height 1 = 17px centreline), centred by centre of mass like MNIST.
    # Grid: rows m=0..7 at image rows 6.5,8.5,...,20.5 ; cols l=0..3 at 7.5,11.5,15.5,19.5
    # =====================================================================
    Hpx = 17.0
    yc = 6.5 + 2.0 * np.arange(8)
    xc = 7.5 + 4.0 * np.arange(4)

    def wr(d):   # row window of a feature: full within +-2.5px, zero beyond 4px
        return np.clip((4.0 - np.abs(d)) / 1.5, 0.0, 1.0)

    def wc(d):   # column window: full within +-1.75px, zero beyond 3.25px
        return np.clip((3.25 - np.abs(d)) / 1.5, 0.0, 1.0)

    edirs = [180.0, 0.0, 90.0, 270.0]  # outward direction of free end: L, R, U, D (y up)

    def presence_maps(strokes, slant):
        # strokes: list of (points, free_start, free_end, weight); weight = how often
        # this stroke is actually written (1 = always).
        tr = []
        tot = 0.0; cx = 0.0; cy = 0.0
        for pts, fs, fe, wt in strokes:
            P = [((x + slant * (0.5 - y)) * Hpx, y * Hpx) for (x, y) in pts]
            tr.append((P, fs, fe, wt))
            for i in range(len(P) - 1):
                L = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
                tot += L * wt
                cx += L * wt * (P[i][0] + P[i + 1][0]) / 2.0
                cy += L * wt * (P[i][1] + P[i + 1][1]) / 2.0
        dx = 13.5 - cx / tot; dy = 13.5 - cy / tot      # centre of mass -> (13.5, 13.5)
        notB = np.ones((4, 8, 4)); notE = np.ones((4, 8, 4))
        for P, fs, fe, wt in tr:
            # effective stroke length (px) of each orientation inside each window
            A = np.zeros((4, 8, 4))
            for i in range(len(P) - 1):
                p = P[i]; q = P[i + 1]
                L = math.hypot(q[0] - p[0], q[1] - p[1])
                n = max(1, int(L / 0.25)); ds = L / n
                th = math.atan2(-(q[1] - p[1]), q[0] - p[0])
                rs = [max(0.0, math.cos(2.0 * (th - math.radians(a)))) for a in odeg]
                for j in range(n):
                    f = (j + 0.5) / n
                    x = p[0] + f * (q[0] - p[0]) + dx
                    y = p[1] + f * (q[1] - p[1]) + dy
                    sp = np.outer(wr(y - yc), wc(x - xc))
                    for o in range(4):
                        A[o] += ds * rs[o] * sp
            B = np.clip((A - 0.75) / 1.75, 0.0, 1.0) * wt   # present if >= ~2.5px in window
            notB *= (1.0 - B)
            E = np.zeros((4, 8, 4))
            ends = []
            if fs:
                ends.append((P[0], P[1]))
            if fe:
                ends.append((P[-1], P[-2]))
            for (p, q) in ends:
                x = p[0] + dx; y = p[1] + dy
                phi = math.atan2(-(p[1] - q[1]), p[0] - q[0])   # outward direction
                sp = np.outer(wr(y - yc), wc(x - xc))
                for e in range(4):
                    r = max(0.0, math.cos(phi - math.radians(edirs[e]))) ** 2
                    E[e] = np.maximum(E[e], r * sp)
            notE *= (1.0 - wt * E)
        return 1.0 - notB, 1.0 - notE

    def blur(Bm):
        # writing-variation blur over neighbouring rows (2px) and columns (4px)
        R = 0.6 * Bm
        R[:, 1:, :] += 0.2 * Bm[:, :-1, :]; R[:, 0, :] += 0.2 * Bm[:, 0, :]
        R[:, :-1, :] += 0.2 * Bm[:, 1:, :]; R[:, -1, :] += 0.2 * Bm[:, -1, :]
        C = 0.7 * R
        C[:, :, 1:] += 0.15 * R[:, :, :-1]; C[:, :, 0] += 0.15 * R[:, :, 0]
        C[:, :, :-1] += 0.15 * R[:, :, 1:]; C[:, :, -1] += 0.15 * R[:, :, -1]
        return C

    # ---- pen strokes for each digit ----
    ell0 = [(0.5 + 0.33 * math.sin(2 * math.pi * i / 24), 0.5 - 0.5 * math.cos(2 * math.pi * i / 24))
            for i in range(25)]
    loop9 = [(0.46 + 0.23 * math.cos(2 * math.pi * i / 20), 0.27 - 0.27 * math.sin(2 * math.pi * i / 20))
             for i in range(21)]
    digits = {
        0: ([(ell0, False, False, 1.0)], 0.15),
        # 1: a fan of three hand-drawn strokes (nearly upright, slanted, strongly slanted)
        1: ([([(0.525, 0.0), (0.475, 1.0)], True, True, 0.7),
             ([(0.65, 0.0), (0.35, 1.0)], True, True, 0.8),
             ([(0.80, 0.0), (0.20, 1.0)], True, True, 0.4)], 0.0),
        2: ([([(0.20, 0.25), (0.27, 0.10), (0.45, 0.0), (0.63, 0.04), (0.74, 0.20), (0.70, 0.38),
               (0.56, 0.56), (0.38, 0.76), (0.20, 0.95), (0.50, 0.93), (0.82, 0.97)], True, True, 1.0)], 0.15),
        3: ([([(0.22, 0.10), (0.38, 0.01), (0.58, 0.02), (0.72, 0.14), (0.68, 0.32), (0.42, 0.46),
               (0.66, 0.56), (0.77, 0.74), (0.68, 0.92), (0.46, 1.0), (0.22, 0.92)], True, True, 1.0)], 0.15),
        4: ([([(0.30, 0.0), (0.20, 0.55), (0.55, 0.56), (0.90, 0.54)], True, True, 1.0),
             ([(0.66, 0.05), (0.66, 1.0)], True, True, 1.0)], 0.10),
        5: ([([(0.78, 0.0), (0.36, 0.02), (0.30, 0.42), (0.50, 0.37), (0.70, 0.46), (0.78, 0.66),
               (0.68, 0.88), (0.46, 1.0), (0.20, 0.92)], True, True, 1.0)], 0.15),
        6: ([([(0.68, 0.0), (0.48, 0.14), (0.34, 0.36), (0.27, 0.62), (0.31, 0.85), (0.47, 1.0),
               (0.66, 0.94), (0.75, 0.77), (0.68, 0.60), (0.50, 0.53), (0.31, 0.64)], True, False, 1.0)], 0.15),
        # 7: bar + stem, plus an optional crossbar through the stem
        7: ([([(0.18, 0.03), (0.80, 0.0), (0.62, 0.45), (0.48, 1.0)], True, True, 1.0),
             ([(0.42, 0.50), (0.82, 0.48)], False, False, 0.3)], 0.10),
        8: ([([(0.50, 0.48), (0.66, 0.36), (0.72, 0.20), (0.64, 0.05), (0.50, 0.0), (0.36, 0.05),
               (0.29, 0.20), (0.35, 0.36), (0.50, 0.48), (0.67, 0.62), (0.75, 0.79), (0.66, 0.95),
               (0.50, 1.0), (0.34, 0.95), (0.25, 0.79), (0.33, 0.62), (0.50, 0.48)], False, False, 1.0)], 0.15),
        9: ([(loop9, False, False, 1.0),
             ([(0.69, 0.27), (0.69, 0.60), (0.62, 1.0)], False, True, 1.0)], 0.15),
    }

    Temp = 12.0       # temperature: naive Bayes over-counts correlated features
    fc_w = np.zeros((10, 256), np.float32)
    fc_b = np.zeros(10, np.float64)
    for d in range(10):
        B, E = presence_maps(*digits[d])
        # presence probabilities: strokes are reliable (0.12..0.88), endings less so (0.12..0.67)
        P_or = 0.12 + 0.76 * blur(B)
        P_en = 0.12 + 0.55 * blur(E)
        Pm = np.concatenate([P_or, P_en], 0)            # (8 types, 8 rows, 4 cols)
        Wd = np.zeros(256)
        bias = 0.0
        for t in range(8):
            th = theta_o if t < 4 else theta_e
            for m in range(8):
                for l in range(4):
                    pp = Pm[t, m, l]
                    ch = 2 * t + (m % 2)      # conv2 channel = (type, row offset)
                    k = m // 2                # pooled row cell
                    # network feature n = absence amount in [0, th];
                    # log-lik = log p + (n/th) * (log(1-p) - log p)
                    Wd[ch * 16 + k * 4 + l] = (math.log(1.0 - pp) - math.log(pp)) / (th * Temp)
                    bias += math.log(pp) / Temp
        fc_w[d] = Wd.astype(np.float32)
        fc_b[d] = bias
    fc_b = (fc_b - fc_b.mean()).astype(np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
