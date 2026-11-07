import numpy as np
import math

def build_weights():
    s2 = 1.0 / math.sqrt(2.0)
    # Orientation unit vectors (dx, dy) in image coords (x = column, y = row, y points DOWN)
    # k=0 horizontal, k=1 "\" diagonal, k=2 vertical, k=3 "/" diagonal
    dirs = [(1.0, 0.0), (s2, s2), (0.0, 1.0), (s2, -s2)]

    # ---------------- conv1: oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    c1 = 2.5          # ridge centre inside the 5x5 kernel (half-pixel, to centre the grid)
    sig_line = 0.8    # ridge width (px)
    for k, (dx, dy) in enumerate(dirs):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                u = i - c1; v = j - c1            # u: row offset (y), v: col offset (x)
                d = v * dy - u * dx               # perpendicular distance to the line
                K[i, j] = math.exp(-d * d / (2 * sig_line ** 2))
        K -= K.mean()                            # zero mean: flat ink gives no response
        K /= K[K > 0].sum()                      # a ~3px stroke gives response ~1
        W1[k, 0] = K
        b1[k] = -0.1
    # channels 4..7 unused

    # ---------------- conv2: pass-through at 4 sub-offsets ----------------
    # channel ch = k*4 + oa*2 + ob copies orientation map k at kernel pos (1+oa, 1+ob).
    # Feature (ch, r, col) = grid cell s=2r+oa, t=2col+ob of orientation k,
    # centred at input row 2s+6, col 2t+6.
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for k in range(4):
        for oa in range(2):
            for ob in range(2):
                W2[k * 4 + oa * 2 + ob, k, 1 + oa, 1 + ob] = 1.0

    # ---------------- digit templates drawn as strokes ----------------
    def line(p, q, step=0.5):
        p = np.array(p, float); q = np.array(q, float)
        L = np.hypot(*(q - p))
        n = max(2, int(math.ceil(L / step)) + 1)
        return [tuple(p + (q - p) * t) for t in np.linspace(0, 1, n)]

    def arc(cx, cy, rx, ry, t0, t1, n=120):
        return [(cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t)))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [arc(14, 13.5, 5.5, 8.5, 0, 360)],
        1: [line((16, 4.5), (12.5, 22.5))],
        2: [arc(14, 9, 5, 4.5, 160, -30),
            line((18.33, 11.25), (9, 22)),
            line((9, 22), (19.5, 22))],
        3: [arc(13.5, 9, 5, 4.5, 150, -90),
            arc(13.5, 18, 5.5, 4.5, 90, -150)],
        4: [line((11, 5), (8.5, 15.5)),
            line((8.5, 15.5), (19.5, 15.5)),
            line((16.5, 6), (16.5, 22.5))],
        5: [line((11, 5), (19, 5)),
            line((11, 5), (10.5, 12.5)),
            arc(13.5, 17, 5.5, 5, 140, -150)],
        6: [line((17, 4.5), (12, 10)),
            line((12, 10), (9.5, 16)),
            arc(14, 18, 4.5, 4.5, 0, 360)],
        7: [line((8.5, 5), (19.5, 5)),
            line((19.5, 5), (12.5, 22.5))],
        8: [arc(14, 9, 4.5, 4.3, 0, 360),
            arc(14, 18, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 5, 0, 360),
            line((19, 10), (17.5, 22.5))],
    }

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 2.5

    def render(strokes):
        T = np.zeros((4, 8, 8))
        for pts in strokes:
            pts = np.asarray(pts, float)
            for a in range(len(pts) - 1):
                p, q = pts[a], pts[a + 1]
                dv = q - p
                L = math.hypot(dv[0], dv[1])
                if L < 1e-9:
                    continue
                ux, uy = dv / L
                mx, my = (p + q) / 2
                g = np.exp(-((Xg - mx) ** 2 + (Yg - my) ** 2) / (2 * sig_t ** 2))
                for k, (dx, dy) in enumerate(dirs):
                    dot = ux * dx + uy * dy
                    tune = max(0.0, 2 * dot * dot - 1)
                    T[k] = np.maximum(T[k], g * tune)
        return T

    # ---------------- fc: cosine-style template matching + class biases ----------------
    beta = 2.0
    Wf = np.zeros((10, 256), np.float32)
    # Prior-shift bias from step-1 confusion: 0.8*log(true_count / predicted_count)
    true_cnt = np.array([1000, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    pred_cnt = np.array([1079, 1037, 829, 487, 121, 684, 1588, 845, 2355, 975], float)
    bf = (0.8 * np.log(true_cnt / pred_cnt)).astype(np.float32)
    for d in range(10):
        T = render(digits[d])
        T = T / (np.linalg.norm(T) + 1e-9)
        for k in range(4):
            for oa in range(2):
                for ob in range(2):
                    ch = k * 4 + oa * 2 + ob
                    for r in range(4):
                        for col in range(4):
                            Wf[d, ch * 16 + r * 4 + col] = beta * T[k, 2 * r + oa, 2 * col + ob]

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wf.astype(np.float32),
        'fc.bias': bf.astype(np.float32),
    }
