import numpy as np
import math

def build_weights():
    # ================= conv1 =================
    # ch0-3: oriented line detectors; ch4: ink blur; ch5-7 unused
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros(8, dtype=np.float64)
    thetas = [0.0, 45.0, 90.0, 135.0]   # stroke direction (x=col right, y=row down)
    for k, th in enumerate(thetas):
        t_rad = math.radians(th)
        ker = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                y, x = r - 2, c - 2
                n = -x * math.sin(t_rad) + y * math.cos(t_rad)   # across line
                t = x * math.cos(t_rad) + y * math.sin(t_rad)    # along line
                ker[r, c] = math.exp(-n * n / 2.0) * math.exp(-t * t / (2 * 2.5 ** 2))
        ker -= ker.mean()
        ker /= ker[ker > 0].sum()
        conv1_w[k, 0] = ker
        conv1_b[k] = -0.2
    g = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            g[r, c] = math.exp(-((r - 2) ** 2 + (c - 2) ** 2) / 2.0)
    conv1_w[4, 0] = g / g.sum()          # ink blur
    conv1_b[4] = 0.0

    # ================= conv2 =================
    # (conv1 input channel, feature id, sy, sx, box size h)
    specs = []
    for (sy, sx) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        specs.append((4, 'ink', sy, sx, 2))          # ch 0-3: ink map
    for o in range(4):
        for (sy, sx) in [(1, 1), (2, 2), (1, 2)]:
            specs.append((o, o, sy, sx, 3))          # ch 4-15: orientation density
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros(16, dtype=np.float64)
    for c, (ic, fid, sy, sx, h) in enumerate(specs):
        conv2_w[c, ic, sy:sy + h, sx:sx + h] = 1.0 / (h * h)
    # receptive-field centre (input px) of pool2 cell a: 4a + 2*s + h + 2.5

    # ================= digit prototypes (x=col, y=row) =================
    def ell(cx, cy, rx, ry, n=48, tilt=0.0):
        pts = []
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            x, y = rx * math.cos(a), ry * math.sin(a)
            pts.append((cx + x - tilt * y, cy + y))
        return pts

    variants = {
        0: [[ell(14, 14, 6, 9)],
            [ell(14, 14, 5, 9, tilt=0.3)],
            [ell(14, 14, 7, 8.5)]],
        1: [[[(16, 4), (12, 23)]],
            [[(14, 4), (14, 23)]],
            [[(18, 4), (10, 23)]]],
        2: [[[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17), (8, 22)],
             [(8, 22), (21, 22)]],
            [[(8, 7), (12, 4), (17, 4), (19, 8), (16, 14), (10, 20), (8, 22), (10, 19),
              (13, 20), (17, 22), (21, 22)]]],
        3: [[[(8, 6), (12, 4), (17, 4), (19, 7), (18, 10), (13, 13)],
             [(13, 13), (18, 15), (20, 18), (18, 22), (13, 23), (8, 21)]],
            [[(9, 5), (14, 4), (18, 6), (17, 10), (12, 13)],
             [(12, 13), (17, 14), (19, 18), (16, 22), (10, 23), (7, 20)]]],
        4: [[[(11, 4), (7, 16), (21, 16)], [(17, 5), (17, 24)]],
            [[(8, 5), (8, 15), (21, 15)], [(18, 5), (18, 24)]],
            [[(12, 4), (6, 16), (21, 15)], [(19, 6), (16, 24)]]],
        5: [[[(20, 4), (10, 4)], [(10, 4), (9, 13)],
             [(9, 13), (14, 11), (19, 13), (20, 18), (17, 22), (12, 23), (7, 21)]],
            [[(21, 5), (12, 5)], [(12, 5), (10, 13)],
             [(10, 13), (15, 12), (18, 15), (18, 19), (14, 23), (8, 22)]]],
        6: [[[(17, 4), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23), (18, 21),
              (19, 17), (16, 14), (12, 14), (9, 17)]],
            [[(18, 4), (14, 7), (11, 12), (10, 17), (12, 22), (16, 23), (19, 20),
              (18, 16), (14, 15), (11, 18)]]],
        7: [[[(7, 5), (21, 5)], [(21, 5), (12, 24)]],
            [[(7, 5), (20, 5)], [(20, 5), (16, 14), (15, 24)]],
            [[(8, 6), (21, 4)], [(21, 4), (10, 24)]]],
        8: [[ell(14, 9, 5, 4.5), ell(14, 18.5, 6, 5)],
            [ell(15, 9, 4.5, 4.5, tilt=0.2), ell(13, 18.5, 5, 5, tilt=0.2)]],
        # larger loops for 9, stem leaving the right side of the loop
        9: [[ell(14, 10, 6, 5.5), [(20, 10), (18, 24)]],
            [ell(13.5, 9.5, 5.5, 5), [(19, 10), (19, 24)]],
            [ell(15, 9.5, 5.5, 5, tilt=0.2), [(20, 10), (15, 24)]]],
    }

    def sample(polys):
        pts, ws, ths = [], [], []
        for poly in polys:
            for p, q in zip(poly[:-1], poly[1:]):
                dx, dy = q[0] - p[0], q[1] - p[1]
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                m = max(1, int(L / 0.5))
                th = math.atan2(dy, dx)
                for i in range(m):
                    f = (i + 0.5) / m
                    pts.append((p[0] + dx * f, p[1] + dy * f))
                    ws.append(L / m)
                    ths.append(th)
        return np.array(pts), np.array(ws), np.array(ths)

    th_o = np.radians(np.array(thetas))

    def feature_template(polys):
        pts, ws, ths = sample(polys)
        dth = ths[:, None] - th_o[None, :]
        tune = np.clip((np.cos(dth) ** 2 - 0.25) / 0.75, 0, None)
        T = np.zeros((16, 4, 4))
        for c, (ic, fid, sy, sx, h) in enumerate(specs):
            if fid == 'ink':
                wpt, sig = ws, 2.5
            else:
                wpt, sig = ws * tune[:, fid], 3.0
            for a in range(4):
                for b in range(4):
                    cy = 4 * a + 2 * sy + h + 2.5
                    cx = 4 * b + 2 * sx + h + 2.5
                    d2 = (pts[:, 0] - cx) ** 2 + (pts[:, 1] - cy) ** 2
                    T[c, a, b] = np.sum(wpt * np.exp(-d2 / (2 * sig ** 2)))
        return T

    ink_idx = np.arange(0, 4)
    ori_idx = np.arange(4, 16)

    def group_norm(T):
        T = T.copy()
        for idx in (ink_idx, ori_idx):
            T[idx] /= (np.linalg.norm(T[idx]) + 1e-9)
        return T

    temps = np.zeros((10, 16, 4, 4))
    for d in range(10):
        acc = np.zeros((16, 4, 4))
        for var in variants[d]:
            acc += group_norm(feature_template(var))
        temps[d] = group_norm(acc)

    # ================= fc =================
    Tn = temps.reshape(10, 256)
    U = Tn - Tn.mean(axis=0, keepdims=True)

    # pairwise discriminative correction from step-8 confusion (rows true, cols pred)
    C = np.array([
        [956,   4,  16,   0,   0,   0,   4,   1,  10,   0],
        [  0, 939,  96,   1,   0,  15,   7,   6,   0,   0],
        [ 58,   5, 636,  19,   5,  10,  75,   2, 179,   1],
        [  5,   4,  14, 621,   1, 271,   2,   6, 104,   2],
        [  7,  28,  14,   0, 771,   3,  47,   3, 103,   7],
        [ 11,   7,   8,  44,   1, 568,  99,   2, 175,   0],
        [ 95,  11,   1,   0,  43,  14, 770,   0,  33,   0],
        [ 36,  17,  37,  25,  24,  41,   1, 422,  59, 428],
        [ 23,  60, 116,   3,   4,  36,  61,  15, 677,  14],
        [ 74,  35,   2,   2, 280,  89,  25,  20, 295, 139]], dtype=np.float64)
    eta = 1.5
    rows = C.sum(axis=1)
    for t in range(10):
        for p in range(10):
            if t == p:
                continue
            r = C[t, p] / rows[t]
            diff = Tn[t] - Tn[p]
            U[t] += eta * r * diff
            U[p] -= eta * r * diff

    U = U.reshape(10, 16, 4, 4)
    s_ink, s_ori = 8.0, 10.0
    U[:, ink_idx] *= s_ink
    U[:, ori_idx] *= s_ori
    fc_w = U.reshape(10, 256)
    #                  0      1     2     3     4      5      6     7      8     9
    fc_b = np.array([-0.25, -0.05, 0.17, 0.79, -0.05, -0.18, -0.04, 1.02, -0.84, 0.76])

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
