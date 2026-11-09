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
    ch = 12   # tip pointing up, tip at kernel tap (1,2)
    put(ch, V, 1, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 1, 2, 0.6); put(ch, D1, 2, 1, 0.4)
    put(ch, D2, 1, 2, 0.6); put(ch, D2, 2, 3, 0.4)
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 0, b, -1.0)
        put(ch, H, 1, b, -0.7)
    ch = 13   # tip pointing down, tip at (3,2)
    put(ch, V, 3, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 3, 2, 0.6); put(ch, D1, 2, 3, 0.4)
    put(ch, D2, 3, 2, 0.6); put(ch, D2, 2, 1, 0.4)
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 4, b, -1.0)
        put(ch, H, 3, b, -0.7)
    ch = 14   # tip pointing left, tip at (2,1)
    put(ch, H, 2, 1, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 0, -1.0)
        put(ch, V, a, 1, -0.7)
    ch = 15   # tip pointing right, tip at (2,3)
    put(ch, H, 2, 3, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 4, -1.0)
        put(ch, V, a, 3, -0.7)
    TIP_TAP = {12: (1, 2), 13: (3, 2), 14: (2, 1), 15: (2, 3)}

    # ------------------------------------------------------------------
    # Hand-drawn digit prototypes: strokes in a nominal frame
    # (x right, y down, digit height 0..20, x centred near 0).
    # Each stroke: (polyline points, weight, tip_at_start, tip_at_end)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1):
        n = max(2, int(abs(a1 - a0) / 6.0) + 1)
        pts = []
        for k in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        return pts

    protos = {}
    protos[0] = [(arc(0, 10, 6.5, 10, -180, 180), 1.0, False, False)]
    protos[1] = [([(0, 0), (0, 20)], 1.0, True, True),
                 ([(3, 0), (-3, 20)], 0.5, True, True)]
    a2 = arc(0, 5.5, 5, 5.5, -170, 40)
    protos[2] = [(a2, 1.0, True, False),
                 ([a2[-1], (-5.5, 20)], 1.0, False, False),
                 ([(-5.5, 20), (6, 20)], 1.0, False, True)]
    protos[3] = [(arc(-0.5, 5, 5, 5, -150, 90), 1.0, True, False),
                 (arc(-0.5, 15, 5.5, 5, -90, 150), 1.0, False, True)]
    protos[4] = [([(-3, 0), (-5.5, 11)], 1.0, True, False),
                 ([(-5.5, 11), (6.5, 11)], 1.0, False, True),
                 ([(2.5, 0), (2.5, 20)], 1.0, True, True)]
    protos[5] = [([(5.5, 0), (-3.5, 0)], 1.0, True, False),
                 ([(-3.5, 0), (-4.5, 8.5)], 1.0, False, False),
                 (arc(-0.5, 13.5, 5.5, 6.5, -135, 150), 1.0, False, True)]
    protos[6] = [([(3.5, 0), (0.5, 3.5), (-2.5, 7.5), (-4.3, 11.5), (-5, 14.5)], 1.0, True, False),
                 (arc(0, 14.5, 5, 5.5, -180, 180), 1.0, False, False)]
    protos[7] = [([(-6, 0), (5.5, 0)], 1.0, True, False),
                 ([(5.5, 0), (-1, 20)], 1.0, False, True)]
    eight = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        a8 = 4.2 if math.cos(t) > 0 else 5.0
        eight.append((a8 * math.sin(2 * t), 10 - 10 * math.cos(t)))
    protos[8] = [(eight, 1.0, False, False)]
    protos[9] = [(arc(-0.5, 5.5, 4.5, 5.5, -180, 180), 1.0, False, False),
                 ([(4.2, 3), (3, 20)], 1.0, False, True)]

    def densify(P, w, out, oris=None):
        # turn a polyline into samples [x, y, orientation(deg), weight*length]
        # oris: optional list of orientations to paint instead of the geometric one
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
                x = xa + (xb - xa) * f
                y = ya + (yb - ya) * f
                if oris is not None:
                    for a in oris:
                        out.append([x, y, a, w * L / n])
                else:
                    out.append([x, y, th, w * L / n])

    def prep(strokes, shear=0.15):
        # slant right, scale centre-line box to 17.5 px, centre of mass to (13.5,13.5)
        S = []
        xs = []
        ys = []
        for (pts, w, t0, t1) in strokes:
            P = [(x + shear * (10.0 - y), y) for (x, y) in pts]
            S.append((P, w, t0, t1))
            xs += [p[0] for p in P]
            ys += [p[1] for p in P]
        scale = 17.5 / max(max(xs) - min(xs), max(ys) - min(ys))
        samples = []
        tips = []
        for (P, w, t0, t1) in S:
            P = [(x * scale, y * scale) for (x, y) in P]
            densify(P, w, samples)
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
    # Paint strokes directly into the 16x4x4 feature space (by formula)
    # ------------------------------------------------------------------
    sigT = 2.6
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))

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
            tune.append(np.clip(1.3 * (1.0 - (d / 42.0) ** 2), 0.0, 1.0))
        for bi, (ca, cb) in enumerate(BANKS):
            for i in range(4):
                cy = 4 * i + 2 * ca + 3.5
                for j in range(4):
                    cx = 4 * j + 2 * cb + 3.5
                    g = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigT * sigT))
                    for o in range(4):
                        T[4 * bi + o, i, j] = cT * float(np.sum(wl * tune[o] * g))
        for (tx, ty, dx, dy, w) in tips:
            phi = math.degrees(math.atan2(abs(dy), abs(dx)))
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

    # base weights: unit-norm template per class (cosine matching)
    W = np.zeros((10, 256), dtype=np.float64)
    B = np.zeros(10, dtype=np.float64)
    for dgt in range(10):
        samples, tips = prep(protos[dgt])
        T = template(samples, tips).reshape(-1)
        W[dgt] = T / (np.linalg.norm(T) + 1e-9)

    # ------------------------------------------------------------------
    # Evidence strokes in absolute pixel coordinates (x=col, y=row),
    # painted into feature space, unit-normalised, and added to classes
    # with signed weights.  Positive weight g (bonus) is paired with a
    # bias of -KAPPA*g so that absence of the stroke counts against the
    # class; negative weights are plain vetoes.
    # ------------------------------------------------------------------
    def stroke_feat(pts, oris=None):
        smp = []
        densify(pts, 1.0, smp, oris)
        T = template(np.array(smp, dtype=np.float64), []).reshape(-1)
        return T / (np.linalg.norm(T) + 1e-9)

    def tip_feat(chn, pts):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        ta, tb = TIP_TAP[chn]
        for (tx, ty) in pts:
            for i in range(4):
                cy = 4 * i + 2 * ta + 3.5
                for j in range(4):
                    cx = 4 * j + 2 * tb + 3.5
                    T[chn, i, j] += math.exp(-((tx - cx) ** 2 + (ty - cy) ** 2) / (2 * 2.0 * 2.0))
        T = T.reshape(-1)
        return T / (np.linalg.norm(T) + 1e-9)

    KS = 1.0     # bias compensation factor for stroke bonuses (present response ~2)
    KT = 0.35    # bias compensation factor for tip bonuses (present response ~0.7)

    EVID = [
        # horizontal closure at the top centre (9 has it, 4 does not)
        (stroke_feat([(11, 5.5), (15.5, 5.5)]), KS, {9: 0.2, 4: -0.2}),
        # vertical on the upper-left side (loop of 9, stem of 5; not 7/3)
        (stroke_feat([(9.7, 7.5), (9.7, 12)]), KS,
         {9: 0.2, 5: 0.15, 7: -0.15, 3: -0.2, 2: -0.1}),
        # horizontal at mid-left (bottom of the 9 loop)
        (stroke_feat([(9.5, 13.5), (13.5, 13.5)]), KS, {9: 0.15, 7: -0.1, 0: -0.15}),
        # horizontal at the bottom (not for digits ending in a tip)
        (stroke_feat([(9, 21.8), (16, 21.8)]), KS, {9: -0.25, 4: -0.2, 7: -0.2, 2: 0.15}),
        # horizontal at the bottom right (end of the 2's base)
        (stroke_feat([(16.5, 21.5), (20.5, 21.5)]), KS,
         {2: 0.15, 3: -0.15, 5: -0.15, 9: -0.1, 8: -0.1}),
        # "/" diagonal in the lower left (2's diagonal)
        (stroke_feat([(12.5, 16), (9, 20.5)]), KS,
         {3: -0.2, 5: -0.15, 9: -0.1, 4: -0.1, 8: -0.1}),
        # vertical on the lower right (belly of 3/5)
        (stroke_feat([(17.7, 15.5), (17.7, 19.5)]), KS, {3: 0.2, 5: 0.1, 2: -0.2, 7: -0.1}),
        # vertical on the upper right (not for 5/6; 3 has it)
        (stroke_feat([(17.5, 7.5), (17.5, 11.5)]), KS, {5: -0.25, 6: -0.2, 3: 0.15}),
        # non-vertical ink in the centre: veto for 0
        (stroke_feat([(13.5, 11.5), (13.5, 15.5)], oris=[0.0, 45.0, 135.0]), KS, {0: -0.25}),
        # upper-right arc of the 0
        (stroke_feat([(16.5, 6.5), (18.8, 11.5)]), KS, {0: 0.15}),
        # cross bar sticking out to the right at mid height (4)
        (stroke_feat([(17.5, 15), (20.5, 15)]), KS, {4: 0.15, 9: -0.15, 8: -0.1}),
        # horizontal bar at the top left (7)
        (stroke_feat([(8, 6.2), (12.5, 6.2)]), KS, {7: 0.2, 1: -0.1, 6: -0.15, 4: -0.1}),
        # top of the 6's loop
        (stroke_feat([(12, 13.3), (16, 13.3)]), KS, {6: 0.2}),
        # vertical on the lower left (closed loop of 6/8)
        (stroke_feat([(9.7, 14.5), (9.7, 18.5)]), KS,
         {6: 0.15, 8: 0.1, 3: -0.1, 5: -0.15, 9: -0.15, 7: -0.1}),
        # horizontal at the top right (5's bar)
        (stroke_feat([(15, 5), (19.5, 5)]), KS, {5: 0.1, 6: -0.1, 4: -0.1}),
        # stroke tips pointing up at the top centre/right
        (tip_feat(12, [(14, 5), (17, 5)]), KT,
         {1: 0.1, 4: 0.15, 6: 0.1, 9: -0.2, 7: -0.15, 2: -0.15, 3: -0.1, 5: -0.1, 0: -0.1, 8: -0.1}),
        # stroke tip pointing up at the top left (4)
        (tip_feat(12, [(10, 5.5)]), KT, {4: 0.15, 9: -0.2, 0: -0.1}),
        # stroke tips pointing down at the bottom
        (tip_feat(13, [(12, 22.5), (15, 22.5)]), KT,
         {1: 0.1, 4: 0.1, 7: 0.1, 9: 0.1,
          2: -0.15, 3: -0.15, 5: -0.15, 6: -0.15, 0: -0.15, 8: -0.15}),
    ]
    for (N, kap, wd) in EVID:
        for dgt, g in wd.items():
            W[dgt] += g * N
            if g > 0:
                B[dgt] -= kap * g      # bonus: its absence should cost the class

    ALPHA = 3.0
    fcw = ALPHA * W
    fcb = ALPHA * B

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
