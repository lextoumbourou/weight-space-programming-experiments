import numpy as np, math

def build_weights():
    # =====================================================================
    # conv1: 8 hand-designed 5x5 filters
    #   ch0..3 : oriented bar (stroke) detectors  H(0deg), "/"(45), V(90), "\"(135)
    #   ch4,5  : stroke-ending detectors: free end pointing Left, Right
    #   ch6    : "clear background" indicator  ReLU(1 - 3*local ink)   (saturated, in [0,1])
    #   ch7    : raw ink (centre pixel)                                 (in [0,1])
    # =====================================================================
    conv1_w = np.zeros((8, 1, 5, 5), np.float32)
    conv1_b = np.zeros(8, np.float32)

    def prof(v):
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
        conv1_b[o] = -0.15

    # ending detector "end pointing left": ink to the right of centre, background elsewhere
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
    ER = EL[:, ::-1].copy()
    conv1_w[4, 0] = EL; conv1_b[4] = -0.10
    conv1_w[5, 0] = ER; conv1_b[5] = -0.10

    # clear-background indicator: 1 where the pixel and its 4 neighbours have no ink
    kb = np.zeros((5, 5))
    kb[2, 2] = -1.5
    kb[1, 2] = kb[3, 2] = kb[2, 1] = kb[2, 3] = -0.375
    conv1_w[6, 0] = kb; conv1_b[6] = 1.0
    # raw ink
    ki = np.zeros((5, 5)); ki[2, 2] = 1.0
    conv1_w[7, 0] = ki; conv1_b[7] = 0.0
    # after max-pool: BS cell = 1 if the 2x2 cell contains a clear background pixel,
    #                 I  cell = ~1 if the 2x2 cell contains a stroke-core pixel.

    # =====================================================================
    # conv2
    #   ch0..7  : orientation t (0..3) x vertical offset a (0,1): window sums with
    #             cross-orientation inhibition  -> 8 rows x 4 cols grid per orientation
    #   ch8,9   : endings Left / Right, window sums -> 4x4 grid
    #   ch10,11 : HOLE detectors: clear-bg cell with ink on all 4 sides (~8px loop / narrow loop)
    #   ch12    : CORNER detector: clear-bg cell with ink above and to the right,
    #             nothing to the left or below (under the bar of a 7 / arc of a 2)
    #   ch13..15: BAY detectors: clear-bg cell with ink on 3 sides, 4th side open
    #             (open Left, open Right, open Up)
    # =====================================================================
    conv2_w = np.zeros((16, 8, 5, 5), np.float32)
    conv2_b = np.zeros(16, np.float32)
    colk = np.array([0.0, 0.5, 1.0, 0.5, 0.0])
    c_inh = 0.35
    for t in range(4):
        for a in range(2):
            rowk = np.zeros(5); rowk[1 + a] = 1.0; rowk[2 + a] = 1.0
            ker = np.outer(rowk, colk)
            s = 1.0 / 1.6
            conv2_w[2 * t + a, t] = s * ker
            conv2_w[2 * t + a, (t + 1) % 4] = -c_inh * s * ker
            conv2_w[2 * t + a, (t + 3) % 4] = -c_inh * s * ker
    ker4 = np.outer(colk, colk)
    conv2_w[8, 4] = 0.8 * ker4
    conv2_w[9, 5] = 0.8 * ker4

    gI = 1.25   # gain on ink cells; AND logic: response>0 only if ALL wall cells have ink

    def struct(ch, walls, opens):
        conv2_w[ch, 6, 2, 2] = 1.0                      # centre cell must be clear background
        for (r, c) in walls:
            conv2_w[ch, 7, r, c] = gI                   # these cells must contain ink
        for (r, c) in opens:
            conv2_w[ch, 7, r, c] = -1.5                 # these cells must be empty
        conv2_b[ch] = -(1.0 + (len(walls) - 1) * gI)    # all walls present -> 1.25, one missing -> 0

    UP2, DN2, LF2, RT2 = (0, 2), (4, 2), (2, 0), (2, 4)
    UP1, DN1, LF1, RT1 = (1, 2), (3, 2), (2, 1), (2, 3)
    struct(10, [UP2, DN2, LF2, RT2], [])                # hole, ~8px loop
    struct(11, [UP2, DN2, LF1, RT1], [])                # hole, narrow loop
    struct(12, [UP2, RT2], [LF1, LF2, DN1, DN2])        # corner: ink above + right only
    struct(13, [RT2, UP2, DN2], [LF1, LF2])             # bay open to the left  (3; bottom of 5)
    struct(14, [LF2, UP2, DN2], [RT1, RT2])             # bay open to the right (top of 5, 6)
    struct(15, [LF2, RT2, DN2], [UP1, UP2])             # bay open upwards      (4; lower inside of 0)

    # =====================================================================
    # fc part 1: stroke templates drawn in feature space from pen strokes
    # (unit box, x right, y down, height 1 = 17px centreline).
    # Orientation grid: rows m=0..7 at image rows 6.5+2m, cols l=0..3 at 7.5+4l
    # Ending grid:      rows k=0..3 at image rows 7.5+4k, cols l=0..3 at 7.5+4l
    # =====================================================================
    Hpx = 17.0
    yc = 6.5 + 2.0 * np.arange(8)
    xc = 7.5 + 4.0 * np.arange(4)
    yc4 = 7.5 + 4.0 * np.arange(4)

    def wr(d):
        return np.clip((4.0 - np.abs(d)) / 1.5, 0.0, 1.0)

    def wc(d):
        return np.clip((4.75 - np.abs(d)) / 3.0, 0.0, 1.0)

    edirs = [180.0, 0.0]   # outward direction of free end: Left, Right

    def template(strokes, slant):
        segs = []; ends = []
        for pts, fs, fe, wt in strokes:
            P = [((x + slant * (0.5 - y)) * Hpx, y * Hpx) for (x, y) in pts]
            for i in range(len(P) - 1):
                segs.append((P[i], P[i + 1], wt))
            if fs:
                ends.append((P[0], P[1], wt))
            if fe:
                ends.append((P[-1], P[-2], wt))
        tot = 0.0; cx = 0.0; cy = 0.0
        for (p, q, wt) in segs:
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            tot += L * wt
            cx += L * wt * (p[0] + q[0]) / 2.0
            cy += L * wt * (p[1] + q[1]) / 2.0
        dx = 13.5 - cx / tot; dy = 13.5 - cy / tot       # centre of mass -> image centre
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
        E = np.zeros((2, 4, 4))
        for (p, q, wt) in ends:
            x = p[0] + dx; y = p[1] + dy
            phi = math.atan2(-(p[1] - q[1]), p[0] - q[0])
            sp = np.outer(wc(y - yc4), wc(x - xc))
            for e in range(2):
                r = max(0.0, math.cos(phi - math.radians(edirs[e]))) ** 2
                E[e] = np.maximum(E[e], wt * r * sp)
        return To, E

    def ell(rx, sl):
        # closed oval outline of half-width rx, sheared to the right by sl
        pts = []
        for i in range(25):
            a = 2 * math.pi * i / 24
            y = 0.5 - 0.5 * math.cos(a)
            x = 0.5 + rx * math.sin(a) + sl * (0.5 - y)
            pts.append((x, y))
        return pts

    loop9 = [(0.46 + 0.23 * math.cos(2 * math.pi * i / 20), 0.27 - 0.27 * math.sin(2 * math.pi * i / 20))
             for i in range(21)]
    digits = {
        # 0: main oval + weaker narrow/tilted and round/upright outlines
        0: ([(ell(0.33, 0.15), False, False, 1.0),
             (ell(0.24, 0.40), False, False, 0.45),
             (ell(0.38, 0.00), False, False, 0.4)], 0.0),
        # 1: fan of three strokes (nearly upright, slanted, strongly slanted)
        #    + weak optional flag at the top and base stroke at the bottom
        1: ([([(0.525, 0.0), (0.475, 1.0)], True, True, 0.6),
             ([(0.65, 0.0), (0.35, 1.0)], True, True, 1.0),
             ([(0.80, 0.0), (0.20, 1.0)], True, True, 0.5),
             ([(0.60, 0.0), (0.38, 0.20)], False, True, 0.35),
             ([(0.22, 1.0), (0.72, 1.0)], True, True, 0.25)], 0.0),
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
        # 7: bar + stem, optional crossbar, optional serif tick hanging from the left end of the bar
        7: ([([(0.18, 0.03), (0.80, 0.0), (0.62, 0.45), (0.48, 1.0)], True, True, 1.0),
             ([(0.42, 0.50), (0.82, 0.48)], False, False, 0.3),
             ([(0.18, 0.03), (0.17, 0.20)], False, False, 0.4)], 0.10),
        8: ([([(0.50, 0.48), (0.66, 0.36), (0.72, 0.20), (0.64, 0.05), (0.50, 0.0), (0.36, 0.05),
               (0.29, 0.20), (0.35, 0.36), (0.50, 0.48), (0.67, 0.62), (0.75, 0.79), (0.66, 0.95),
               (0.50, 1.0), (0.34, 0.95), (0.25, 0.79), (0.33, 0.62), (0.50, 0.48)], False, False, 1.0)], 0.15),
        # 9: loop + straight tail, plus a weak alternative tail that curls to the left
        9: ([(loop9, False, False, 1.0),
             ([(0.69, 0.27), (0.69, 0.60), (0.62, 1.0)], False, True, 1.0),
             ([(0.66, 0.80), (0.56, 0.96), (0.40, 1.0), (0.27, 0.94)], False, True, 0.35)], 0.15),
    }
    TO = []; TE = []
    for d in range(10):
        To, E = template(*digits[d])
        TO.append(To); TE.append(E)

    # coverage of the orientation template (spread to neighbours) -> where strokes are UNEXPECTED
    adj_or = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}

    def coverage_or(T4):
        cov = np.zeros_like(T4)
        for o in range(4):
            srcs = [(T4[o], 1.0)] + [(T4[a], 0.7) for a in adj_or[o]]
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

    def coverage_en(E2):
        cov = np.zeros_like(E2)
        for e in range(2):
            for dk in (-1, 0, 1):
                for dl in (-1, 0, 1):
                    wn = 1.0 if (dk == 0 and dl == 0) else 0.6
                    for k in range(4):
                        kk = k + dk
                        if kk < 0 or kk > 3:
                            continue
                        for l in range(4):
                            ll = l + dl
                            if ll < 0 or ll > 3:
                                continue
                            v = wn * E2[e, kk, ll]
                            if v > cov[e, k, l]:
                                cov[e, k, l] = v
        return cov

    GO = np.max(np.stack(TO, 0), axis=0)     # how much any digit uses each feature
    GE = np.max(np.stack(TE, 0), axis=0)

    alpha = 3.0      # logit scale of the template part
    omega_e = 1.5    # importance of ending features
    mu_o = 0.5       # "unexpected stroke" penalty
    mu_e = 0.25      # "unexpected ending" penalty

    norms = [math.sqrt((TO[d] ** 2).sum() + omega_e * (TE[d] ** 2).sum()) for d in range(10)]
    nbar = sum(norms) / 10.0

    # ---- hand-written "must be empty" stroke rules ---------------------------
    # (class, orientation types, rows m, cols l, weight): weight forced to <= -weight
    Hh, D1, Vv, D2 = 0, 1, 2, 3
    rules = [
        (4, [Hh], [0, 1], [1, 2], 0.6),        # 4: no horizontal closing stroke at the top (9 has one)
        (3, [Vv], [1, 2, 3], [0], 0.5),        # 3: no vertical at far left, upper-middle (9 loop side)
        (3, [Vv, D1], [4, 5], [0], 0.5),       # 3: nothing at far left, lower-middle (2's diagonal)
        (0, [Hh], [3, 4], [1, 2], 0.5),        # 0: no horizontal stroke in the centre (6 loop top)
    ]
    # ---- hand-written ending rules: (class, ending type 0=L 1=R, rows k, cols l, weight)
    # only the row band of the 4's crossbar (k=2), below the widest point of a 9's loop
    erules = [
        (9, 1, [2], [2, 3], 0.5),
        (8, 1, [2], [2, 3], 0.4),
    ]

    # =====================================================================
    # fc part 2: hand-written weights for holes / corner / bays.
    # Lists give the weight for pooled rows k = 0..3 (centre rows 6-9, 10-13, 14-17, 18-21).
    # =====================================================================
    hole = {0: [-.1, .3, .1, -.2], 1: [-1.5, -1.5, -1.5, -1.5], 2: [-.3, -.5, -.3, 0.],
            3: [-.7, -.7, -.7, -.7], 4: [0., .1, -.4, -.6], 5: [-.6, -.6, -.4, -.4],
            6: [-.6, -.2, .7, .6], 7: [-.4, -.4, -.6, -.6], 8: [.6, .1, .1, .6],
            9: [.6, .9, -.2, -.6]}
    corner = {0: [.4, .3, -.2, -.3], 1: [-.6, -.6, -.6, -.6], 2: [.4, .4, 0., -.2],
              3: [0., 0., .2, .2], 4: [-.5, -.5, .1, .3], 5: [-.5, -.5, .2, .2],
              6: [-.5, -.3, 0., 0.], 7: [.6, .7, .2, -.2], 8: [-.5, -.5, -.3, -.3],
              9: [-.6, -.6, .1, .3]}
    bayL = {0: [-.5, -.5, -.5, -.5], 1: [-.3, -.3, -.3, -.3], 2: [.1, .1, -.4, -.4],
            3: [.7, .7, .7, .7], 4: [-.5, -.5, -.5, -.5], 5: [-.7, -.7, .3, .3],
            6: [-.6, -.6, -.6, -.6], 7: [0., 0., -.5, -.5], 8: [-.3, .1, .1, -.3],
            9: [-.5, -.5, .2, .2]}
    bayR = {0: [-.5, -.5, -.5, -.5], 1: [-.3, -.3, -.3, -.3], 2: [-.4, -.4, .4, .3],
            3: [-.7, -.5, -.5, -.7], 4: [-.4, -.4, -.4, -.4], 5: [.8, .6, -.3, -.5],
            6: [.5, .5, -.3, -.4], 7: [-.5, -.5, -.5, -.5], 8: [-.3, .1, .1, -.3],
            9: [-.5, -.5, -.5, -.5]}
    bayU = {0: [-.3, -.2, .4, .5], 1: [-.6, -.6, -.6, -.6], 2: [-.5, -.5, -.5, -.5],
            3: [-.5, -.5, -.5, -.5], 4: [.7, .8, .3, -.5], 5: [-.5, -.5, -.5, -.5],
            6: [-.5, -.5, .3, .3], 7: [-.5, -.5, -.5, -.5], 8: [-.6, -.5, 0., .1],
            9: [-.7, -.7, -.5, -.5]}

    fc_w = np.zeros((10, 256), np.float32)
    for d in range(10):
        Wd = np.zeros(256)
        # --- orientation templates (cosine-style match + automatic negative evidence) ---
        To = TO[d]
        U = np.clip(1.0 - coverage_or(To) / 0.35, 0.0, 1.0)
        Wo = np.zeros((4, 8, 4))
        for t in range(4):
            pos = To[t] / norms[d]
            neg = mu_o * U[t] * GO[t] / nbar
            Wo[t] = alpha * (pos - neg)
        for (cd, types, ms, ls, wgt) in rules:
            if cd != d:
                continue
            for t in types:
                for m in ms:
                    for l in ls:
                        Wo[t, m, l] = min(Wo[t, m, l], -wgt)
        if d == 1:
            # energy-dependent prior for "1": every unit of stroke energy counts slightly
            # against 1 (compensated by a higher constant bias below).
            Wo = Wo - 0.02
        for t in range(4):
            for m in range(8):
                for l in range(4):
                    ch = 2 * t + (m % 2); k = m // 2
                    Wd[ch * 16 + k * 4 + l] = Wo[t, m, l]
        # --- ending templates (4x4 grid) ---
        E = TE[d]
        Ue = np.clip(1.0 - coverage_en(E) / 0.35, 0.0, 1.0)
        We = np.zeros((2, 4, 4))
        for e in range(2):
            pos = omega_e * E[e] / norms[d]
            neg = mu_e * Ue[e] * GE[e] / nbar
            We[e] = alpha * (pos - neg)
        for (cd, e, ks, ls, wgt) in erules:
            if cd != d:
                continue
            for k in ks:
                for l in ls:
                    We[e, k, l] = min(We[e, k, l], -wgt)
        for e in range(2):
            for k in range(4):
                for l in range(4):
                    Wd[(8 + e) * 16 + k * 4 + l] = We[e, k, l]
        # --- holes, corner and bays ---
        for k in range(4):
            for l in range(4):
                h = hole[d][k]
                if d == 2 and k >= 2 and l <= 1:
                    h = 0.0                      # many 2s have a small loop at the bottom left
                if d in (6, 8) and k >= 2 and l == 0:
                    h *= 0.3                     # ... so a bottom-left loop is weak evidence for 6/8
                Wd[10 * 16 + k * 4 + l] = 0.4 * h
                Wd[11 * 16 + k * 4 + l] = 0.4 * h
                # corner: ignore the leftmost column (outside lower-left of round loops fires there)
                Wd[12 * 16 + k * 4 + l] = (0.8 * corner[d][k]) if l >= 1 else 0.0
                Wd[13 * 16 + k * 4 + l] = 0.8 * bayL[d][k]
                Wd[14 * 16 + k * 4 + l] = 0.8 * bayR[d][k]
                Wd[15 * 16 + k * 4 + l] = 0.8 * bayU[d][k]
        fc_w[d] = Wd.astype(np.float32)

    # class biases (base units): damped correction from the step-13 predicted-vs-true counts
    fc_b = np.array([-0.124, 0.52, -0.163, -0.555, 0.823, -0.231, -0.279, 0.806, -0.668, -0.075],
                    np.float32)

    # global logit scale: changes no prediction, only the confidence (1.2 helped the loss; try 1.6)
    scale = 1.6
    fc_w = (fc_w * scale).astype(np.float32)
    fc_b = (fc_b * scale).astype(np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
