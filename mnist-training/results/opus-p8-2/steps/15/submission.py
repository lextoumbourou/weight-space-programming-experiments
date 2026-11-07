import numpy as np
import math

# ---------------------------------------------------------------------------
# Stroke helpers: arrays of (x=col, y=row) points in 28x28 input coordinates
# ---------------------------------------------------------------------------
def _line(p0, p1, step=0.25):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    n = max(2, int(L / step) + 1)
    t = np.linspace(0, 1, n)
    return np.stack([p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t], 1)

def _arc(cx, cy, rx, ry, t0, t1, step=0.25):
    L = abs(t1 - t0) * math.pi / 180 * max(rx, ry)
    n = max(2, int(L / step) + 2)
    t = np.radians(np.linspace(t0, t1, n))
    return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], 1)

def _bez(p0, p1, p2, n=120):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = np.array(p0, float), np.array(p1, float), np.array(p2, float)
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

def _V(w, strokes, ends=(), sh=(), lh=()):
    # one hand-drawn style variant: weight, strokes, endpoints (x,y,strength), small holes, large holes
    return (w, strokes, list(ends), list(sh), list(lh))

def _variants():
    V = {}
    V[0] = [_V(0.5, [_arc(14, 14, 6.5, 9.5, 0, 360)], lh=[(14, 14)]),
            _V(0.25, [_arc(14, 14, 5.0, 9.5, 0, 360)], lh=[(14, 14)]),
            _V(0.25, [_arc(14, 14, 7.5, 9.0, 0, 360)], lh=[(14, 14)])]
    V[1] = [_V(0.4, [_line((15.5, 4), (12.5, 23))], ends=[(15.5, 4.5, 1), (12.5, 22.5, 1)]),
            _V(0.3, [_line((14, 4), (14, 23))], ends=[(14, 4.5, 1), (14, 22.5, 1)]),
            _V(0.3, [_line((18, 4.5), (10.5, 23))], ends=[(18, 5, 1), (10.5, 22.5, 1)])]
    top2 = _arc(13.5, 9, 5.5, 4.5, 160, -30)
    V[2] = [_V(0.45, [top2, _line((18.3, 11.3), (8, 22)), _line((8, 22), (20, 22))],
               ends=[(8.3, 7.5, 1), (20, 22, 1)]),
            _V(0.3, [top2, _bez((18.3, 11.3), (15, 17), (8, 22)), _line((8, 22), (21, 21.5))],
               ends=[(8.3, 7.5, 1), (21, 21.5, 1)]),
            # curly-bottom 2: small loop at bottom-left before the base stroke
            _V(0.25, [top2, _bez((18.3, 11.3), (14, 17), (9.5, 19.5)),
                      _arc(10.5, 20.5, 2.2, 2.0, 135, -200), _line((11, 22), (21, 21.5))],
               ends=[(8.3, 7.5, 1), (21, 21.5, 1)])]
    V[3] = [_V(1.0, [_arc(13, 9, 6, 5, 150, -90), _arc(13, 18.5, 7, 5, 90, -150)],
               ends=[(7.8, 6.5, 1), (7.0, 21, 1), (12, 13.5, 0.5)])]
    V[4] = [_V(0.55, [_line((10, 4), (7.5, 16)), _line((7.5, 16), (21, 16)), _line((18, 5), (17, 23))],
               ends=[(10, 4.5, 1), (18, 5, 1), (17, 22.5, 1), (21, 16, 0.6)]),
            _V(0.45, [_line((16, 4), (7, 16)), _line((7, 16), (21, 16)), _line((17.5, 6), (17, 23))],
               ends=[(16, 4.5, 1), (17.5, 6, 0.7), (17, 22.5, 1), (21, 16, 0.6)])]
    V[5] = [_V(1.0, [_line((11, 4.5), (20, 4.5)), _line((11, 4.5), (10, 12)), _arc(13, 17, 6.5, 5.5, 140, -150)],
               ends=[(20, 4.5, 1), (7.4, 19.8, 1)])]
    V[6] = [_V(0.45, [_bez((17, 4), (9, 7), (8.5, 18)), _arc(14, 18, 5.5, 5, 0, 360)],
               ends=[(17, 4.5, 1)], sh=[(14, 18)]),
            _V(0.3, [_line((16, 4), (9, 15)), _arc(14, 18.5, 5.5, 4.5, 0, 360)],
               ends=[(16, 4.5, 1)], sh=[(14, 18.5)]),
            # big round loop with short top stroke
            _V(0.25, [_bez((16, 5), (10, 8), (8, 15)), _arc(13.5, 17, 6, 6, 0, 360)],
               ends=[(16, 5, 1)], sh=[(13.5, 17)])]
    V[7] = [_V(0.4, [_line((7, 5), (20, 5)), _line((20, 5), (13, 23))], ends=[(7, 5, 1), (13, 22.5, 1)]),
            _V(0.2, [_line((7, 5), (20, 5)), _line((20, 5), (16.5, 23))], ends=[(7, 5, 1), (16.5, 22.5, 1)]),
            _V(0.2, [_line((8, 5), (20, 5)), _line((20, 5), (11, 23))], ends=[(8, 5, 1), (11, 22.5, 1)]),
            # short top bar
            _V(0.2, [_line((10, 5.5), (19, 5)), _line((19, 5), (14, 23))], ends=[(10, 5.5, 1), (14, 22.5, 1)])]
    V[8] = [_V(0.45, [_arc(14, 9, 4.5, 4.5, 0, 360), _arc(14, 18.5, 5.5, 5, 0, 360)],
               sh=[(14, 9), (14, 18.5)]),
            _V(0.3, [_arc(15.5, 9, 4.5, 4.5, 0, 360), _arc(12.5, 18.5, 5.5, 5, 0, 360)],
               sh=[(15.5, 9), (12.5, 18.5)]),
            # small top loop, large bottom loop
            _V(0.25, [_arc(14.5, 8, 3.5, 3.5, 0, 360), _arc(13.5, 17.5, 6, 5.5, 0, 360)],
               sh=[(14.5, 8), (13.5, 17.5)])]
    V[9] = [_V(0.35, [_arc(14, 9.5, 5, 5, 0, 360), _line((19, 10), (16.5, 23))],
               ends=[(16.5, 22.5, 1)], sh=[(14, 9.5)]),
            _V(0.25, [_arc(14, 9.5, 5, 5, 0, 360), _line((19, 10), (19, 23))],
               ends=[(19, 22.5, 1)], sh=[(14, 9.5)]),
            _V(0.25, [_arc(15, 9.5, 5, 5, 0, 360), _line((20, 10), (14, 23))],
               ends=[(14, 22.5, 1)], sh=[(15, 9.5)]),
            # stem curving left at the bottom
            _V(0.15, [_arc(14, 9.5, 5, 5, 0, 360), _bez((19, 10), (19, 19), (14, 23))],
               ends=[(14, 23, 1)], sh=[(14, 9.5)])]
    return V

SHEARS = [(-0.2, 0.25), (0.0, 0.5), (0.2, 0.25)]   # slant k (x += k*(14-y)), weight

ORIENTS = [k * math.pi / 4 for k in range(4)]   # 0,45,90,135 degrees (math convention)
INK_TAPS = [(1, 1), (1, 2), (2, 1), (2, 2)]     # conv2 taps producing the 8x8 ink grid

def _soft(d, half, blur):
    e = np.maximum(0.0, np.abs(d) - half)
    return np.exp(-e ** 2 / (2.0 * blur ** 2))

def _render(strokes, ends, sh, lh):
    """Draw one style variant into feature-template space (16,4,4)."""
    INK, OR = 0.7, 0.5
    c8 = 2 * np.arange(8) + 5.5
    c4 = 4 * np.arange(4) + 7.5
    R = np.zeros((16, 4, 4))
    ink8 = np.zeros((8, 8)); tight = np.zeros((4, 4, 4)); wide = np.zeros((4, 4, 4))
    for pts in strokes:
        x, y = pts[:, 0], pts[:, 1]
        dx = np.gradient(x); dy = np.gradient(y)
        seg = np.hypot(dx, dy)
        theta = np.mod(np.arctan2(-dy, dx), math.pi)
        tun = np.zeros((len(x), 4))
        for k, ok in enumerate(ORIENTS):
            dl = np.mod(theta - ok + math.pi / 2, math.pi) - math.pi / 2
            tun[:, k] = np.maximum(0.0, np.cos(2 * dl))
        wy = _soft(y[:, None] - c8[None, :], 2.7, 1.2)
        wx = _soft(x[:, None] - c8[None, :], 2.7, 1.2)
        ink8 = np.maximum(ink8, INK * (wy[:, :, None] * wx[:, None, :]).max(0))
        wy = _soft(y[:, None] - c4[None, :], 2.5, 1.2)
        wx = _soft(x[:, None] - c4[None, :], 2.5, 1.2)
        w = wy[:, :, None] * wx[:, None, :]
        for k in range(4):
            tight[k] = np.maximum(tight[k], (OR * w * tun[:, k, None, None]).max(0))
        wy = _soft(y[:, None] - c4[None, :], 4.0, 1.2)
        wx = _soft(x[:, None] - c4[None, :], 4.0, 1.2)
        ww = wy[:, :, None] * wx[:, None, :] * seg[:, None, None]
        for k in range(4):
            wide[k] += OR * (ww * tun[:, k, None, None]).sum(0) / 6.0
    for q, (i, j) in enumerate(INK_TAPS):
        R[q] = ink8[i - 1::2, j - 1::2]
    R[4:8] = tight
    R[8:12] = np.minimum(wide, 1.5)
    for (hx, hy) in sh:
        R[12] = np.maximum(R[12], np.outer(_soft(hy - c4, 2.5, 1.5), _soft(hx - c4, 2.5, 1.5)))
    for (hx, hy) in lh:
        R[13] = np.maximum(R[13], np.outer(_soft(hy - c4, 2.5, 1.5), _soft(hx - c4, 2.5, 1.5)))
    for (ex, ey, st) in ends:
        R[14] = np.maximum(R[14], st * np.outer(_soft(ey - c4, 2.5, 1.2), _soft(ex - c4, 2.5, 1.2)))
        R[15] = np.maximum(R[15], st * np.outer(_soft(ey - c4, 4.0, 1.2), _soft(ex - c4, 4.0, 1.2)))
    return R

def _shear_pts(p, k):
    q = p.copy(); q[:, 0] = p[:, 0] + k * (14.0 - p[:, 1]); return q

def _shear_xy(x, y, k):
    return x + k * (14.0 - y), y

def _templates():
    V = _variants()
    T = np.zeros((10, 16, 4, 4))
    for d in range(10):
        for (w, strokes, ends, sh, lh) in V[d]:
            for (k, ws) in SHEARS:
                st = [_shear_pts(p, k) for p in strokes]
                en = [(*_shear_xy(x, y, k), s) for (x, y, s) in ends]
                s1 = [_shear_xy(x, y, k) for (x, y) in sh]
                l1 = [_shear_xy(x, y, k) for (x, y) in lh]
                T[d] += w * ws * _render(st, en, s1, l1)
    return T

def build_weights():
    # ---------------- conv1 ----------------
    c1w = np.zeros((8, 1, 5, 5), np.float32)
    c1b = np.zeros(8, np.float32)
    # ch0: tight ink detector
    c1w[0, 0, 2, 2] = 0.5
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        c1w[0, 0, r, c] = 0.125
    c1b[0] = -0.25
    # ch1..4: zero-mean ridge (line) detectors at 0,45,90,135 degrees
    yy, xx = np.mgrid[-2:3, -2:3].astype(np.float64)
    for k, th in enumerate(ORIENTS):
        ux, uy = math.cos(th), -math.sin(th)
        dist = np.abs(xx * uy - yy * ux)
        g = np.exp(-dist ** 2 / (2 * 1.0 ** 2))
        w = g - g.mean()
        w /= w[w > 0].sum()
        c1w[1 + k, 0] = w
        c1b[1 + k] = -0.1
    # ch5: empty-spot detector
    c1w[5, 0, 1:4, 1:4] = -0.5 / 0.6
    c1b[5] = 1.0
    # ch6: endpoint detector
    c1w[6, 0, :, :] = -1.0
    c1w[6, 0, 1:4, 1:4] = 1.0
    c1b[6] = -1.5
    # ch7 unused

    # ---------------- conv2 ----------------
    c2w = np.zeros((16, 8, 5, 5), np.float32)
    c2b = np.zeros(16, np.float32)
    for q, (i, j) in enumerate(INK_TAPS):          # ch0..3: 8x8 ink grid
        c2w[q, 0, i, j] = 1.0
    for k in range(4):                              # ch4..7 tight / ch8..11 wide orientation
        c2w[4 + k, 1 + k, 2, 2] = 1.0
        c2w[8 + k, 1 + k, 1:4, 1:4] = 1.0 / 3.0
    # ch12: small-hole detector
    c2w[12, 5, 2, 2] = 2.0
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        c2w[12, 0, r, c] = 0.5
    for (r, c) in [(0, 2), (4, 2), (2, 0), (2, 4)]:
        c2w[12, 0, r, c] = 1.0
    c2b[12] = -4.6
    # ch13: large-hole detector
    c2w[13, 5, 2, 2] = 2.0
    for (r, c) in [(0, 2), (4, 2), (2, 0), (2, 4)]:
        c2w[13, 0, r, c] = 1.5
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        c2w[13, 0, r, c] = -0.6
    c2b[13] = -5.0
    # ch14/15: endpoint tight / wide
    c2w[14, 6, 2, 2] = 1.0
    c2w[15, 6, 1:4, 1:4] = 1.0 / 3.0

    # ---------------- fc ----------------
    T = _templates()
    groups = [(slice(0, 4), 1.5), (slice(4, 8), 3.0), (slice(8, 12), 3.0)]
    fcw = np.zeros((10, 16, 4, 4))
    for sl, sg in groups:
        Tg = T[:, sl].reshape(10, -1)
        Tg = Tg / np.linalg.norm(Tg, axis=1, keepdims=True)
        fcw[:, sl] = sg * Tg.reshape(10, -1, 4, 4)
    WH, WE = 1.0, 0.5
    fcw[:, 12] = WH * T[:, 12]
    fcw[:, 13] = WH * T[:, 13]
    fcw[:, 14] = WE * T[:, 14]
    fcw[:, 15] = 0.6 * WE * T[:, 15]
    fcw = fcw.reshape(10, 256).astype(np.float32)

    true_cnt = np.array([980, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    pred5 = np.array([692, 1356, 536, 674, 128, 300, 1120, 494, 3287, 1413], float)
    pred6 = np.array([766, 1288, 966, 987, 617, 1371, 1382, 698, 742, 1183], float)
    pred8 = np.array([869, 1211, 852, 960, 804, 891, 1026, 844, 1559, 984], float)
    pred9 = np.array([986, 1017, 1135, 1174, 871, 994, 929, 999, 898, 997], float)
    pred11 = np.array([870, 1013, 1157, 1429, 1252, 1020, 991, 917, 645, 706], float)
    pred13 = np.array([947, 1193, 1020, 1089, 1772, 974, 801, 764, 734, 706], float)
    pred14 = np.array([947, 1191, 992, 1060, 1253, 901, 934, 856, 910, 956], float)
    fcb = 0.7 * (np.log(true_cnt / pred5) + np.log(true_cnt / pred6)
                 + np.log(true_cnt / pred8) + np.log(true_cnt / pred9)
                 + np.log(true_cnt / pred11))
    fcb += 0.8 * (np.log(true_cnt / pred13) + np.log(true_cnt / pred14))
    fcb = fcb.astype(np.float32)

    return {
        "conv1.weight": c1w,
        "conv1.bias": c1b,
        "conv2.weight": c2w,
        "conv2.bias": c2b,
        "fc.weight": fcw,
        "fc.bias": fcb,
    }
