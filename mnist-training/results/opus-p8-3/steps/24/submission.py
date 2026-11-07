import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1
    #   ch0-3 oriented line detectors (0=horiz, 45='\', 90=vert, 135='/')
    #   ch4 ink (blur - 0.1); ch5 background ReLU(1-2.5*blur)
    #   ch6/ch7 pair -> saturated ink clip(3*blur-0.3,0,1) after pooling
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
    # conv2: ch0-4 blurred pass-through; ch5 LOOP_s, ch6 LOOP_l, ch7 HB_s,
    # ch8 VB_s, ch9 HB_l, ch10 VB_l, ch11 OPEN_L, ch12 OPEN_R, ch13 OPEN_U, ch14 OPEN_D
    # ------------------------------------------------------------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def sat(ch, r, c, w):
        W2[ch, 6, r, c] += w
        W2[ch, 7, r, c] -= w

    near = {'U': (1, 2), 'D': (3, 2), 'L': (2, 1), 'R': (2, 3)}
    far = {'U': (0, 2), 'D': (4, 2), 'L': (2, 0), 'R': (2, 4)}

    def detector(ch, taps, sides_req, sides_forbid=()):
        W2[ch, 5, 2, 2] = 1.0
        for sd in sides_req:
            sat(ch, *taps[sd], 1.0)
        for sd in sides_forbid:
            sat(ch, *taps[sd], -1.0)
        b2[ch] = -(len(sides_req) + 1 - 0.6)

    detector(5, near, 'UDLR')
    detector(6, far, 'UDLR')
    detector(7, near, 'LR')
    detector(8, near, 'UD')
    detector(9, far, 'LR')
    detector(10, far, 'UD')
    detector(11, far, 'UDR', 'L')
    detector(12, far, 'UDL', 'R')
    detector(13, far, 'LRD', 'U')
    detector(14, far, 'LRU', 'D')

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

    # ---- part 1: stroke templates, correlation classifier on ch0-4 ----
    temps = []
    for d in range(10):
        T = np.mean([render(v) for v in digits[d]], axis=0)
        for (dd, c, rs, cs, fac) in emph:
            if dd == d:
                T[c, rs, cs] *= fac
        full = np.zeros((16, 4, 4))
        full[:5] = T
        O = full[:4].copy()
        for k in range(4):
            full[k] = 0.7 * O[k] + 0.15 * (O[(k - 1) % 4] + O[(k + 1) % 4])
        for c in range(5):
            full[c] = smooth_spatial(full[c])
        temps.append(full.reshape(-1))
    temps = np.array(temps)

    beta, kappa = 3.0, 0.47
    Tbar = temps.mean(axis=0)
    Wf = np.zeros((10, 256), np.float64)
    bf = np.zeros(10, np.float64)
    for d in range(10):
        U = temps[d] - Tbar
        U = U / np.linalg.norm(U)
        Wf[d] = beta * U
        bf[d] = -beta * kappa * float(Tbar @ U)

    # ---- naive-Bayes helpers ----
    idx = lambda c, i, j: c * 16 + i * 4 + j

    def region(ch, rows, cols=range(4)):
        v = np.zeros(256)
        for i in rows:
            for j in cols:
                v[idx(ch, i, j)] = 1.0
        return v

    def add_nb(v, p, lam, m):
        p = np.clip(np.asarray(p, float), 0.03, 0.95)
        lo = np.log(p / (1 - p))
        for d in range(10):
            Wf[d] += lam * (lo[d] / m) * v
            bf[d] += lam * np.log(1 - p[d])

    # ---- part 2: topology features (probes 3-5) ----
    loop_rows = np.array([
        [1, 96, 287, 101], [0, 1, 1, 1], [16, 153, 68, 68], [175, 46, 130, 182],
        [5, 338, 74, 14], [13, 33, 148, 205], [3, 219, 350, 55], [0, 357, 63, 1],
        [155, 337, 26, 227], [4, 617, 25, 5]]) / 1000.0
    for r in range(4):
        add_nb(region(6, [r]), 1.3 * loop_rows[:, r], 0.6, 0.8)
    cav = np.array([
        [33, 78, 8, 184, 1, 279, 352, 2],
        [31, 36, 13, 83, 1, 0, 1, 1],
        [598, 51, 6, 159, 0, 17, 64, 87],
        [277, 676, 39, 13, 0, 15, 5, 0],
        [8, 84, 72, 17, 680, 25, 2, 51],
        [0, 472, 357, 45, 4, 17, 3, 8],
        [1, 5, 752, 21, 108, 64, 2, 1],
        [384, 444, 10, 12, 24, 1, 146, 26],
        [127, 386, 105, 281, 35, 1, 3, 3],
        [33, 560, 79, 44, 13, 28, 26, 66]]) / 1000.0
    for n, ch in enumerate([11, 12, 13, 14]):
        for half in (0, 1):
            add_nb(region(ch, [2 * half, 2 * half + 1]), 1.3 * cav[:, 2 * n + half], 0.6, 0.8)
    add_nb(region(5, [0, 1]), np.array([74, 0, 146, 255, 190, 52, 214, 160, 476, 427]) / 1000.0, 0.6, 0.8)
    add_nb(region(5, [2, 3]), np.array([102, 0, 161, 92, 100, 86, 406, 20, 412, 121]) / 1000.0, 0.6, 0.8)
    add_nb(region(7, [0, 1]), np.array([835, 15, 667, 459, 719, 410, 466, 815, 800, 750]) / 1000.0, 0.6, 0.8)

    # ---- part 3: stroke features (probes 6-7), presence = region sum > 0.8 ----
    lam_s, m_s = 0.5, 1.6
    add_nb(region(0, [0]),               np.array([665, 7, 710, 917, 27, 852, 41, 990, 816, 843]) / 1000.0, lam_s, m_s)  # top bar
    add_nb(region(0, [3]),               np.array([864, 21, 918, 787, 224, 683, 857, 63, 280, 113]) / 1000.0, lam_s, m_s)  # bottom bar
    add_nb(region(2, [0, 1], [0, 1]),    np.array([615, 302, 122, 72, 767, 489, 754, 177, 738, 578]) / 1000.0, lam_s, m_s)  # UL vertical
    add_nb(region(2, [0, 1], [2, 3]),    np.array([733, 970, 923, 768, 923, 66, 214, 911, 603, 814]) / 1000.0, lam_s, m_s)  # UR vertical
    add_nb(region(2, [2, 3], [0, 1]),    np.array([900, 830, 269, 65, 527, 245, 912, 267, 855, 434]) / 1000.0, lam_s, m_s)  # LL vertical
    add_nb(region(3, [1, 2], [1, 2]),    np.array([756, 682, 909, 972, 835, 586, 929, 908, 980, 908]) / 1000.0, lam_s, m_s)  # centre '/'

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf.astype(np.float32), "fc.bias": bf.astype(np.float32),
    }
