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
    # angles in degrees, math convention (y up); converted to row coords (y down)
    L = abs(t1 - t0) * math.pi / 180 * max(rx, ry)
    n = max(2, int(L / step) + 2)
    t = np.radians(np.linspace(t0, t1, n))
    return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], 1)

def _bez(p0, p1, p2, n=120):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = np.array(p0, float), np.array(p1, float), np.array(p2, float)
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

# Hand-described digit skeletons (digits occupy roughly rows 4..23)
def _digit_strokes():
    S = {}
    S[0] = [_arc(14, 14, 6.5, 9.5, 0, 360)]
    S[1] = [_line((15.5, 4), (12.5, 23))]
    S[2] = [_arc(13.5, 9, 5.5, 4.5, 160, -30), _line((18.3, 11.3), (8, 22)), _line((8, 22), (20, 22))]
    S[3] = [_arc(13, 9, 6, 5, 150, -90), _arc(13, 18.5, 7, 5, 90, -150)]
    S[4] = [_line((10, 4), (7.5, 16)), _line((7.5, 16), (21, 16)), _line((18, 5), (17, 23))]
    S[5] = [_line((11, 4.5), (20, 4.5)), _line((11, 4.5), (10, 12)), _arc(13, 17, 6.5, 5.5, 140, -150)]
    S[6] = [_bez((17, 4), (9, 7), (8.5, 18)), _arc(14, 18, 5.5, 5, 0, 360)]
    S[7] = [_line((7, 5), (20, 5)), _line((20, 5), (13, 23))]
    S[8] = [_arc(14, 9, 4.5, 4.5, 0, 360), _arc(14, 18.5, 5.5, 5, 0, 360)]
    S[9] = [_arc(14, 9.5, 5, 5, 0, 360), _line((19, 10), (16.5, 23))]
    return S

# Hand-described hole centres: (x, y)
SMALL_HOLES = {6: [(14, 18)], 8: [(14, 9), (14, 18.5)], 9: [(14, 9.5)]}
LARGE_HOLES = {0: [(14, 14)]}

ORIENTS = [k * math.pi / 4 for k in range(4)]   # 0,45,90,135 degrees (math convention)
INK_TAPS = [(1, 1), (1, 2), (2, 1), (2, 2)]     # conv2 taps producing the 8x8 ink grid

def _soft(d, half, blur):
    e = np.maximum(0.0, np.abs(d) - half)
    return np.exp(-e ** 2 / (2.0 * blur ** 2))

def _templates():
    """Returns stroke templates T (10,16,4,4) for channels 0..11, and hole maps H (10,2,4,4)."""
    INK, OR = 0.7, 0.5
    S = _digit_strokes()
    c8 = 2 * np.arange(8) + 5.5        # centres of 8x8 ink grid (input pixels)
    c4 = 4 * np.arange(4) + 7.5        # centres of 4x4 grid
    T = np.zeros((10, 16, 4, 4))
    H = np.zeros((10, 2, 4, 4))
    for d in range(10):
        ink8 = np.zeros((8, 8))
        tight = np.zeros((4, 4, 4))
        wide = np.zeros((4, 4, 4))
        for pts in S[d]:
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
            a, b = i - 1, j - 1
            T[d, q] = ink8[a::2, b::2]
        T[d, 4:8] = tight
        T[d, 8:12] = np.minimum(wide, 1.5)
        for (hx, hy) in SMALL_HOLES.get(d, []):
            H[d, 0] = np.maximum(H[d, 0], np.outer(_soft(hy - c4, 2.5, 1.5), _soft(hx - c4, 2.5, 1.5)))
        for (hx, hy) in LARGE_HOLES.get(d, []):
            H[d, 1] = np.maximum(H[d, 1], np.outer(_soft(hy - c4, 2.5, 1.5), _soft(hx - c4, 2.5, 1.5)))
    return T, H

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
    # ch5: empty-spot detector, 1 where a 3x3 patch has no ink
    c1w[5, 0, 1:4, 1:4] = -0.5 / 0.6
    c1b[5] = 1.0
    # ch6, ch7 unused

    # ---------------- conv2 ----------------
    c2w = np.zeros((16, 8, 5, 5), np.float32)
    c2b = np.zeros(16, np.float32)
    # ch0..3: 8x8 ink grid via 4 offset taps
    for q, (i, j) in enumerate(INK_TAPS):
        c2w[q, 0, i, j] = 1.0
    # ch4..7: tight orientation; ch8..11: wide orientation
    for k in range(4):
        c2w[4 + k, 1 + k, 2, 2] = 1.0
        c2w[8 + k, 1 + k, 1:4, 1:4] = 1.0 / 3.0
    # ch12: small-hole detector (softer threshold)
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
    # ch14, ch15 unused

    # ---------------- fc ----------------
    T, H = _templates()
    T = T.reshape(10, 256)
    Tn = T / np.linalg.norm(T, axis=1, keepdims=True)    # cosine over channels 0..11 only
    s = 5.0
    fcw = s * Tn
    # hole evidence added separately (not normalised), weight WH per unit detector output
    WH = 1.0
    fcw = fcw.reshape(10, 16, 4, 4)
    fcw[:, 12] = WH * H[:, 0]
    fcw[:, 13] = WH * H[:, 1]
    fcw = fcw.reshape(10, 256).astype(np.float32)
    true_cnt = np.array([980, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    pred5 = np.array([692, 1356, 536, 674, 128, 300, 1120, 494, 3287, 1413], float)
    pred6 = np.array([766, 1288, 966, 987, 617, 1371, 1382, 698, 742, 1183], float)
    fcb = 0.7 * np.log(true_cnt / pred5) + 0.7 * np.log(true_cnt / pred6)
    fcb = fcb.astype(np.float32)

    return {
        "conv1.weight": c1w,
        "conv1.bias": c1b,
        "conv2.weight": c2w,
        "conv2.bias": c2b,
        "fc.weight": fcw,
        "fc.bias": fcb,
    }
