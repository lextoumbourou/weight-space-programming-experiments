import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]  # direction (cos,sin), x right, y down
    for k, th in enumerate(thetas):
        G = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                dy, dx = i - 2, j - 2
                d = -dx * math.sin(th) + dy * math.cos(th)   # across the line
                l = dx * math.cos(th) + dy * math.sin(th)    # along the line
                G[i, j] = math.exp(-d * d / (2 * 0.81)) * math.exp(-l * l / 8.0)
        G -= G.mean()                       # zero-sum
        G *= 1.25 / G[G > 0].sum()
        W1[k, 0] = G
        b1[k] = -0.25
    # channels 4..7 unused

    # ---------------- conv2: routing / shifting ----------------
    # channel ch = o*4 + sy*2 + sx copies orientation map o, tap at (1+sy, 1+sx)
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for o in range(4):
        for sy in range(2):
            for sx in range(2):
                W2[o * 4 + sy * 2 + sx, o, 1 + sy, 1 + sx] = 1.0

    # ---------------- hand-drawn digit prototypes ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * t / n), cy + ry * math.sin(2 * math.pi * t / n))
                for t in range(n + 1)]

    protos = {
        0: [ellipse(14, 14, 6.0, 9)],
        1: [[(15, 4.5), (13.5, 23)]],
        2: [[(8.5, 9), (9.5, 6.5), (12, 5), (15, 4.8), (18, 6), (19.5, 8.5), (19, 11.5), (16.5, 15),
             (13, 18.5), (10, 21), (8, 23), (12, 23), (16, 23), (21, 23)]],
        # redrawn 3: bigger top arc, cusp further left, rounder lower bowl
        3: [[(8.5, 6), (12, 4.5), (16, 4.8), (18.5, 7), (18, 10), (15, 12.5), (11.5, 13.5),
             (15.5, 14.5), (19, 17), (19, 20.5), (16, 23), (12, 23.5), (8, 21.5)]],
        4: [[(12, 4.5), (10, 9), (7.5, 15), (13, 15.5), (21, 15.5)], [(18, 6), (18, 23)]],
        5: [[(20, 4.5), (10.5, 4.5), (9.5, 12.5), (13, 11.5), (17, 12), (19.5, 15), (19.5, 19),
             (17, 22.5), (13, 23.5), (8.5, 21.5)]],
        6: [[(17, 4.5), (13, 7.5), (10, 11.5), (8.5, 16), (9, 20), (11.5, 23), (15, 23), (18, 21),
             (19, 17.5), (17, 14.5), (13.5, 14), (10, 15.5), (9, 17)]],
        7: [[(7, 5), (20.5, 5), (17.5, 11), (14.5, 17), (13, 23)]],
        # single-stroke figure-eight with diagonal X crossing at the centre
        8: [[(17, 6), (14, 4.5), (11, 6), (10.5, 9), (13, 12), (17, 15), (18.5, 18.5), (16.5, 22),
             (13, 23), (9.5, 21.5), (9, 18), (11, 15), (13, 13), (16, 10.5), (17.5, 8), (17, 6)]],
        9: [ellipse(13.5, 9, 5, 4.5), [(18.5, 9), (17, 23)]],
    }

    SHEAR = 0.12   # top of digit leans right
    BLUR = 4.5     # spatial fall-off (px) of a template stroke

    def render(polys):
        pts = []
        for poly in polys:
            poly = [(x + SHEAR * (14 - y), y) for (x, y) in poly]
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                n = max(1, int(math.ceil(L / 0.5)))
                th = math.atan2(y1 - y0, x1 - x0)
                for k in range(n):
                    t = (k + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0), th))
        P = np.array(pts)
        P[:, 0] += 13.8 - P[:, 0].mean()     # centre of mass centring
        P[:, 1] += 13.8 - P[:, 1].mean()
        T = np.zeros((4, 8, 8))
        for o, tho in enumerate(thetas):
            tune = np.cos(P[:, 2] - tho) ** 2
            for Y in range(8):
                cy = 2 * Y + 5.5
                ddy = np.maximum(0, np.abs(P[:, 1] - cy) - 1.5)
                for X in range(8):
                    cx = 2 * X + 5.5
                    ddx = np.maximum(0, np.abs(P[:, 0] - cx) - 1.5)
                    sp = np.maximum(0, 1 - np.sqrt(ddx ** 2 + ddy ** 2) / BLUR)
                    T[o, Y, X] = np.max(tune * sp)
        return T

    # ---------------- fc: cosine template matching + calibration biases ----------------
    s = 10.0
    #                       0     1     2     3     4     5     6     7     8      9
    class_bias = np.array([0.1, -0.75, 0.1, 0.6, 0.7, 0.7, -0.8, 0.1, -0.05, -0.5])
    Wfc = np.zeros((10, 256))
    bfc = class_bias.copy()
    for dgt in range(10):
        T = render(protos[dgt])
        T = T / np.sqrt(np.sum(T ** 2))      # unit-norm template
        for o in range(4):
            for sy in range(2):
                for sx in range(2):
                    ch = o * 4 + sy * 2 + sx
                    for r in range(4):
                        for c in range(4):
                            Wfc[dgt, ch * 16 + r * 4 + c] = s * T[o, 2 * r + sy, 2 * c + sx]

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
