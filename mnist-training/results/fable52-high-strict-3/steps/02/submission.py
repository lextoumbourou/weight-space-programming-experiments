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
        conv1_b[o] = -0.08

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
        conv1_b[4 + i] = -0.10

    # =====================================================================
    # conv2: 16 channels = 8 feature types x 2 vertical offsets.
    # Each kernel sums one conv1 feature over a 2(rows) x 3(cols) patch of
    # pooled cells.  After the 2nd max-pool, channel (type t, offset a),
    # cell (k,l) is a soft window centred at image row 6.5+2*(2k+a),
    # image col 7.5+4*l  -> an 8-row x 4-col grid per feature type.
    # =====================================================================
    conv2_w = np.zeros((16, 8, 5, 5), np.float32)
    conv2_b = np.zeros(16, np.float32)
    colk = np.array([0.0, 0.5, 1.0, 0.5, 0.0])
    for t in range(8):
        for a in range(2):
            rowk = np.zeros(5); rowk[1 + a] = 1.0; rowk[2 + a] = 1.0
            s = (1.0 / 2.4) if t < 4 else 0.8          # normalise so "full" feature ~1
            conv2_w[2 * t + a, t] = s * np.outer(rowk, colk)

    # =====================================================================
    # fc templates, drawn directly in feature space from pen strokes
    # (unit box, x right, y down, height 1 = 17px centreline).
    # =====================================================================
    Hpx = 17.0
    yc = 6.5 + 2.0 * np.arange(8)      # window centres (rows)
    xc = 7.5 + 4.0 * np.arange(4)      # window centres (cols)

    def wr(d):
        return np.clip((4.0 - np.abs(d)) / 1.5, 0.0, 1.0)

    def wc(d):
        return np.clip((4.75 - np.abs(d)) / 3.0, 0.0, 1.0)

    edirs = [180.0, 0.0, 90.0, 270.0]  # outward direction of free end: L, R, U, D (y up)

    def template(strokes, slant):
        # strokes: list of (points, free_start, free_end, weight)
        segs = []; ends = []
        for pts, fs, fe, wt in strokes:
            P = [((x + slant * (0.5 - y)) * Hpx, y * Hpx) for (x, y) in pts]
            for i in range(len(P) - 1):
                segs.append((P[i], P[i + 1], wt))
            if fs:
                ends.append((P[0], P[1], wt))
            if fe:
                ends.append((P[-1], P[-2], wt))
        # centre of mass of the pen path -> image centre (13.5, 13.5), like MNIST
        tot = 0.0; cx = 0.0; cy = 0.0
        for (p, q, wt) in segs:
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            tot += L * wt
            cx += L * wt * (p[0] + q[0]) / 2.0
            cy += L * wt * (p[1] + q[1]) / 2.0
        dx = 13.5 - cx / tot; dy = 13.5 - cy / tot
        # orientation maps: stroke length falling in each window, per orientation
        A = np.zeros((4, 8, 4))
        for (p, q, wt) in segs:
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            n = max(1, int(L / 0.25)); ds = L / n
            th = math.atan2(-(q[1] - p[1]), q[0] - p[0])
            rs = [max(0.0, math.cos(2.0 * (th - math.radians(a)))) for a in odeg]
            for i in range(n):
                f = (i + 0.5) / n
                x = p[0] + f * (q[0] - p[0]) + dx
                y = p[1] + f * (q[1] - p[1]) + dy
                sp = np.outer(wr(y - yc), wc(x - xc))
                for o in range(4):
                    A[o] += wt * ds * rs[o] * sp / 5.0
        To = np.minimum(A, 1.0)
        # ending maps
        E = np.zeros((4, 8, 4))
        for (p, q, wt) in ends:
            x = p[0] + dx; y = p[1] + dy
            phi = math.atan2(-(p[1] - q[1]), p[0] - q[0])   # outward direction
            sp = np.outer(wr(y - yc), wc(x - xc))
            for e in range(4):
                r = max(0.0, math.cos(phi - math.radians(edirs[e]))) ** 2
                E[e] = np.maximum(E[e], wt * r * sp)
        return np.concatenate([To, E], 0)                    # (8 types, 8 rows, 4 cols)

    # ---- pen strokes for each digit (upright; a common right-slant is added) ----
    ell0 = [(0.5 + 0.33 * math.sin(2 * math.pi * i / 24), 0.5 - 0.5 * math.cos(2 * math.pi * i / 24))
            for i in range(25)]
    loop9 = [(0.46 + 0.23 * math.cos(2 * math.pi * i / 20), 0.27 - 0.27 * math.sin(2 * math.pi * i / 20))
             for i in range(21)]
    digits = {
        0: ([(ell0, False, False, 1.0)], 0.15),
        1: ([([(0.5, 0.0), (0.5, 1.0)], True, True, 1.0)], 0.20),
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
        7: ([([(0.18, 0.03), (0.80, 0.0), (0.62, 0.45), (0.48, 1.0)], True, True, 1.0)], 0.10),
        8: ([([(0.50, 0.48), (0.66, 0.36), (0.72, 0.20), (0.64, 0.05), (0.50, 0.0), (0.36, 0.05),
               (0.29, 0.20), (0.35, 0.36), (0.50, 0.48), (0.67, 0.62), (0.75, 0.79), (0.66, 0.95),
               (0.50, 1.0), (0.34, 0.95), (0.25, 0.79), (0.33, 0.62), (0.50, 0.48)], False, False, 1.0)], 0.15),
        9: ([(loop9, False, False, 1.0),
             ([(0.69, 0.27), (0.69, 0.60), (0.62, 1.0)], False, True, 1.0)], 0.15),
    }
    T_all = [template(*digits[d]) for d in range(10)]        # each (8,8,4)

    # ---- "coverage": template spread to neighbouring rows/cols/orientations ----
    # Used to decide where a feature would be UNEXPECTED for a class.
    adj_or = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}    # neighbouring orientations
    adj_en = {0: [2, 3], 1: [2, 3], 2: [0, 1], 3: [0, 1]}    # neighbouring end directions

    def coverage(T4, adj):
        cov = np.zeros_like(T4)
        for o in range(4):
            srcs = [(T4[o], 1.0)] + [(T4[a], 0.7) for a in adj[o]]
            for src, wo in srcs:
                for dm in (-1, 0, 1):
                    for dl, wl in ((0, 1.0), (-1, 0.6), (1, 0.6)):
                        for m in range(8):
                            mm = m + dm
                            if mm < 0 or mm > 7:
                                continue
                            for l in range(4):
                                ll = l + dl
                                if ll < 0 or ll > 3:
                                    continue
                                v = wo * wl * src[mm, ll]
                                if v > cov[o, m, l]:
                                    cov[o, m, l] = v
        return cov

    # G: how much ANY digit uses each feature (only diagnostic features get penalties)
    G = np.max(np.stack(T_all, 0), axis=0)                   # (8,8,4)

    alpha = 3.0      # logit scale (temperature)
    omega_e = 1.5    # importance of ending features relative to orientation features
    mu_o = 0.5       # strength of "unexpected stroke" penalty
    mu_e = 0.25      # strength of "unexpected ending" penalty (endings are noisier)

    norms = []
    for d in range(10):
        T = T_all[d]
        norms.append(math.sqrt((T[:4] ** 2).sum() + omega_e * (T[4:] ** 2).sum()))
    nbar = sum(norms) / 10.0

    fc_w = np.zeros((10, 256), np.float32)
    for d in range(10):
        T = T_all[d]
        cov = np.concatenate([coverage(T[:4], adj_or), coverage(T[4:], adj_en)], 0)
        U = np.clip(1.0 - cov / 0.35, 0.0, 1.0)              # 1 where class d expects nothing nearby
        Wd = np.zeros(256)
        for t in range(8):
            om = 1.0 if t < 4 else omega_e
            mu = mu_o if t < 4 else mu_e
            for m in range(8):
                for l in range(4):
                    ch = 2 * t + (m % 2)      # conv2 channel = (type, row offset)
                    k = m // 2                # pooled row cell
                    pos = om * T[t, m, l] / norms[d]               # cosine-style template match
                    neg = mu * U[t, m, l] * G[t, m, l] / nbar      # negative evidence
                    Wd[ch * 16 + k * 4 + l] = alpha * (pos - neg)
        fc_w[d] = Wd.astype(np.float32)

    # class biases from the step-1 confusion matrix: broad templates (8,3,9,6,0) were
    # over-predicted, 2 and 7 under-predicted.
    fc_b = np.array([-0.3, 0.0, 0.3, -0.8, 0.0, 0.0, -0.4, 0.3, -1.3, -0.7], np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
