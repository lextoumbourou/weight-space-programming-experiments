import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1
    #   ch0-3 oriented line detectors (0=horiz, 45='\', 90=vert, 135='/')
    #   ch4 ink (blur - 0.1)           -> used by stroke templates
    #   ch5 background ReLU(1-2.5*blur), bounded in [0,1]
    #   ch6 ReLU(3*blur-0.3), ch7 ReLU(3*blur-1.3): after pooling,
    #       ch6-ch7 = clip(3*maxblur-0.3, 0, 1) = saturated ink
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))
        w = w - w.mean()
        w = w / w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()
    W1[4, 0] = g;        b1[4] = -0.1
    W1[5, 0] = -2.5 * g; b1[5] = 1.0
    W1[6, 0] = 3.0 * g;  b1[6] = -0.3
    W1[7, 0] = 3.0 * g;  b1[7] = -1.3

    # ------------------------------------------------------------------
    # conv2
    #   ch0-4 : 3x3-blurred pass-through of conv1 ch0-4
    #   ch5 LOOP_s, ch6 LOOP_l, ch7 HB_s, ch8 VB_s, ch9 HB_l, ch10 VB_l,
    #   ch11 OPEN_L, ch12 OPEN_R, ch13 OPEN_U, ch14 OPEN_D
    # ------------------------------------------------------------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def sat(ch, r, c, w):
        # add w * saturated_ink(pool1 position r,c) to conv2 channel ch
        W2[ch, 6, r, c] += w
        W2[ch, 7, r, c] -= w

    near = {'U': (1, 2), 'D': (3, 2), 'L': (2, 1), 'R': (2, 3)}
    far = {'U': (0, 2), 'D': (4, 2), 'L': (2, 0), 'R': (2, 4)}

    def detector(ch, taps, sides_req, sides_forbid=(), theta=None):
        W2[ch, 5, 2, 2] = 1.0                       # background at centre
        for sd in sides_req:
            sat(ch, *taps[sd], 1.0)
        for sd in sides_forbid:
            sat(ch, *taps[sd], -1.0)
        n = len(sides_req)
        b2[ch] = -(n + 1 - 0.6) if theta is None else -theta

    detector(5, near, 'UDLR')            # LOOP_s
    detector(6, far, 'UDLR')             # LOOP_l
    detector(7, near, 'LR')              # HB_s
    detector(8, near, 'UD')              # VB_s
    detector(9, far, 'LR')               # HB_l
    detector(10, far, 'UD')              # VB_l
    detector(11, far, 'UDR', 'L')        # OPEN_L (cavity opening to the left)
    detector(12, far, 'UDL', 'R')        # OPEN_R
    detector(13, far, 'LRD', 'U')        # OPEN_U
    detector(14, far, 'LRU', 'D')        # OPEN_D

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (x=col, y=row); variants per digit
    # ------------------------------------------------------------------
    def ell(cx, cy, rx, ry, a0=0.0, a1=360.0, n=28):
        a = np.radians(np.linspace(a0, a1, n))
        return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in a]

    digits = {
        0: [[ell(14, 14, 5.5, 8.5)],
            [ell(14, 14, 6.5, 8.5)],
            [[(15 - 1.5 * math.sin(t) + 6 * math.cos(t), 14 + 8.5 * math.sin(t))
              for t in np.radians(np.linspace(0, 360, 28))]]],
        1: [[[(15.5, 5), (12.5, 23)]],
            [[(14, 5), (14, 23)]],
            [[(17, 5), (11, 23)]]],
        2: [[[(9, 9), (10.5, 6), (14, 5), (17.5, 6), (19, 9), (18, 12), (15, 15.5),
              (11, 19.5), (9, 22), (14, 22), (20, 22)]],
            [[(9, 8), (12, 5), (16, 5), (18.5, 7.5), (17.5, 11), (9, 22), (20, 22)]]],
        3: [[[(9, 6), (13, 5), (17, 5.5), (19, 8), (18, 11), (14, 13.5), (18, 15.5),
              (19.5, 18.5), (18, 21.5), (14, 23), (9, 22)]],
            [[(10, 5), (18, 5), (13, 12.5), (18, 14.5), (19.5, 18), (17, 22), (13, 23), (9, 21)]]],
        4: [[[(10, 5), (9.5, 15), (20, 15)], [(18, 5), (17, 23)]],
            [[(16, 5), (9, 16), (20, 16)], [(17, 8), (17, 23)]]],
        5: [[[(19, 5), (11, 5), (10, 13), (14, 12), (18, 13.5), (19.5, 17), (18, 21),
              (14, 23), (9, 21.5)]],
            [[(19, 5), (12, 5.5), (11, 12), (15, 11.5), (18.5, 14), (18.5, 19), (15, 22.5),
              (10, 22)]]],
        6: [[[(17, 5), (13, 8), (10.5, 12), (9.5, 16), (10, 20), (13, 23), (16.5, 22.5),
              (18.5, 19), (17.5, 15.5), (14, 14), (10.5, 16)]],
            [[(16, 5), (12, 11), (10, 17), (11, 21.5), (14.5, 23), (18, 21), (18, 17),
              (15, 15), (11, 17)]]],
        7: [[[(9, 5), (19.5, 5), (17, 11), (14.5, 17), (13, 23)]],
            [[(9, 6), (19, 5), (15, 14), (12, 23)]]],
        8: [[ell(14, 9.5, 4.0, 4.2), ell(14, 18.5, 5.0, 4.5)],
            [ell(15, 9.5, 4.0, 4.2), ell(13, 18.5, 5.0, 4.5)]],
        9: [[ell(14, 9.5, 4.5, 4.3), [(18.5, 10), (17.5, 16), (16, 23)]],
            [ell(14.5, 9.5, 4.5, 4.3), [(19, 10), (15, 23)]]],
    }

    def cov(v, i):
        lo, hi = 4 * i + 5.0, 4 * i + 10.0
        dist = max(lo - v, 0.0, v - hi)
        return max(0.0, 1.0 - dist / 3.0)

    def render(polys):
        T = np.zeros((5, 4, 4))
        for P in polys:
            P = np.array(P, float)
            for a, b in zip(P[:-1], P[1:]):
                dx, dy = b - a
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(dy, dx)
                o = [max(0.0, math.cos(2 * (phi - math.radians(th)))) for th in thetas]
                n = max(2, int(L / 0.5) + 1)
                for t in np.linspace(0, 1, n):
                    x, y = a + t * (b - a)
                    hy = [cov(y, i) for i in range(4)]
                    hx = [cov(x, j) for j in range(4)]
                    for i in range(4):
                        for j in range(4):
                            sp = hy[i] * hx[j]
                            if sp <= 0:
                                continue
                            for k in range(4):
                                T[k, i, j] = max(T[k, i, j], o[k] * sp)
                            T[4, i, j] = max(T[4, i, j], sp)
        return T

    # ------------------------------------------------------------------
    # Hand-written expected presence of topology features (prob. per cell)
    # rows: input rows 6-9,10-13,14-17,18-21 ; cols same
    # ------------------------------------------------------------------
    TP = {c: {d: np.zeros((4, 4)) for d in range(10)} for c in range(5, 15)}

    def put(c, d, cells, v):
        for (i, j) in cells:
            TP[c][d][i, j] = max(TP[c][d][i, j], v)

    TOPc = [(0, 1), (0, 2), (1, 1), (1, 2)]
    BOTc = [(2, 1), (2, 2), (3, 1), (3, 2)]
    MIDc = [(1, 1), (1, 2), (2, 1), (2, 2)]
    COL12 = lambda rows: [(r, j) for r in rows for j in (1, 2)]
    # LOOP_s
    put(5, 6, BOTc, 0.5); put(5, 8, TOPc, 0.4); put(5, 8, BOTc, 0.4)
    put(5, 9, TOPc, 0.5); put(5, 0, MIDc, 0.2); put(5, 4, TOPc, 0.15)
    put(5, 2, [(3, 0), (3, 1)], 0.1)
    # LOOP_l
    put(6, 0, MIDc, 0.3); put(6, 6, BOTc, 0.2); put(6, 9, TOPc, 0.2); put(6, 8, MIDc, 0.1)
    # HB_s
    put(7, 0, COL12(range(4)), 0.4); put(7, 4, TOPc, 0.5)
    put(7, 6, BOTc, 0.6); put(7, 8, TOPc, 0.5); put(7, 8, BOTc, 0.5); put(7, 9, TOPc, 0.6)
    put(7, 7, COL12([1]), 0.2)
    # VB_s
    put(8, 6, BOTc, 0.5); put(8, 8, TOPc, 0.4); put(8, 8, BOTc, 0.4); put(8, 9, TOPc, 0.5)
    put(8, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)], 0.3)
    put(8, 5, [(0, 2), (0, 3)], 0.3); put(8, 2, [(3, 2), (3, 3)], 0.3)
    put(8, 0, COL12([0, 3]), 0.2)
    # HB_l (locations informed by probe of step 14)
    put(9, 0, COL12(range(4)), 0.5); put(9, 4, COL12([0, 1]), 0.5)
    put(9, 9, COL12([1]), 0.4); put(9, 6, COL12([1, 2]), 0.3)
    put(9, 8, COL12([1, 3]), 0.2); put(9, 2, COL12([0, 3]), 0.15)
    put(9, 3, COL12([3]), 0.1); put(9, 5, COL12([3]), 0.1); put(9, 7, COL12([1]), 0.25)
    # VB_l
    put(10, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 0.5); put(10, 3, [(2, 0), (2, 1), (3, 0), (3, 1)], 0.5)
    put(10, 5, [(0, 2), (0, 3), (1, 2), (1, 3)], 0.5); put(10, 5, [(2, 0), (2, 1), (3, 0), (3, 1)], 0.3)
    put(10, 2, [(2, 2), (2, 3), (3, 2), (3, 3)], 0.3); put(10, 2, [(1, 0), (1, 1)], 0.2)
    # OPEN_L
    put(11, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 0.5); put(11, 3, [(2, 0), (2, 1), (3, 0), (3, 1)], 0.5)
    put(11, 5, [(2, 0), (2, 1), (3, 0), (3, 1)], 0.4); put(11, 2, [(1, 0), (1, 1), (2, 0), (2, 1)], 0.3)
    # OPEN_R
    put(12, 5, [(0, 2), (0, 3), (1, 2), (1, 3)], 0.5); put(12, 6, [(0, 2), (1, 2)], 0.3)
    # OPEN_U
    put(13, 4, TOPc, 0.5)
    # OPEN_D
    put(14, 2, TOPc, 0.4); put(14, 7, [(1, 0), (1, 1)], 0.15)

    emph = [
        (7, 0, slice(0, 1), slice(0, 4), 1.6),
        (2, 0, slice(3, 4), slice(0, 4), 1.6),
        (5, 2, slice(0, 2), slice(0, 2), 1.5),
        (5, 0, slice(0, 1), slice(0, 4), 1.3),
        (1, 2, slice(0, 4), slice(1, 3), 1.3),
    ]

    def smooth_spatial(M):
        P = np.pad(M, 1, mode='edge')
        return 0.6 * M + 0.1 * (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:])

    topo_w = 1.5
    temps = []
    for d in range(10):
        T = np.mean([render(v) for v in digits[d]], axis=0)
        for (dd, c, rs, cs, fac) in emph:
            if dd == d:
                T[c, rs, cs] *= fac
        full = np.zeros((16, 4, 4))
        full[:5] = T
        for c in range(5, 15):
            full[c] = topo_w * TP[c][d]
        O = full[:4].copy()
        for k in range(4):
            full[k] = 0.7 * O[k] + 0.15 * (O[(k - 1) % 4] + O[(k + 1) % 4])
        for c in range(15):
            full[c] = smooth_spatial(full[c])
        temps.append(full.reshape(-1))
    temps = np.array(temps)

    # ------------------------------------------------------------------
    # fc: correlation classifier
    # ------------------------------------------------------------------
    beta, kappa = 4.0, 0.47
    Tbar = temps.mean(axis=0)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        U = temps[d] - Tbar
        U = U / np.linalg.norm(U)
        Wf[d] = beta * U
        bf[d] = -beta * kappa * float(Tbar @ U)

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
