import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 filters, 5x5 ----------------
    angles = [0, 30, 60, 90, 120, 150]  # degrees, image coords (x right, y down)
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    ys, xs = np.mgrid[0:5, 0:5]
    xs = xs - 2.0
    ys = ys - 2.0
    for k, a in enumerate(angles):
        t = math.radians(a)
        dpar = xs * math.cos(t) + ys * math.sin(t)
        dperp = -xs * math.sin(t) + ys * math.cos(t)
        g = np.exp(-dperp ** 2 / (2 * 0.8 ** 2)) * np.exp(-dpar ** 2 / (2 * 2.0 ** 2))
        g = g - g.mean()                      # zero-sum ridge detector
        g = g / (np.abs(g).sum() / 2.0)       # positive part sums to ~1
        w1[k, 0] = g
        b1[k] = -0.2
    g = np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.2 ** 2))
    w1[6, 0] = g / g.sum()                    # blob (ink density)
    w1[7, 0] = 1.0 / 25                       # uniform average

    # ---------------- conv2: 16 channels, 8x5x5 ----------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for k in range(6):
        w2[k, k, :, :] = 0.08                 # broad orientation maps
    w2[6, 6, :, :] = 0.08                     # broad blob
    for k in range(6):
        w2[8 + k, k, 1:4, 1:4] = 0.2          # narrow orientation maps
    w2[14, 6, 1:4, 1:4] = 0.2                 # narrow blob
    w2[15, 7, :, :] = 0.08
    b2[:] = -0.02
    # channel 7: HOLE detector on blob map: ink on ring (offset 2), no ink in centre 3x3
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            m = max(abs(dx), abs(dy))
            if m == 2:
                w2[7, 6, dy + 2, dx + 2] = 0.05
            elif m <= 1:
                w2[7, 6, dy + 2, dx + 2] = -0.10
    b2[7] = -0.25

    # ---------------- fc: hand-drawn stroke templates ----------------
    def ellipse(cx, cy, rx, ry, a0=0, a1=360, n=40):
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        return pts

    strokes = {
        0: [ellipse(14, 14, 6, 9)],
        1: [[(11, 8), (14, 5), (14, 23)]],
        2: [[(8, 9), (10, 6), (14, 5), (18, 7), (19, 11), (8, 23), (20, 23)]],
        3: [[(8, 7), (14, 5), (19, 8), (14, 13), (19, 17), (14, 23), (8, 21)]],
        4: [[(17, 23), (17, 5), (7, 17), (21, 17)]],
        5: [[(19, 5), (9, 5), (8, 13), (14, 12), (19, 16), (14, 23), (8, 21)]],
        6: [[(18, 5), (10, 12), (8, 18), (13, 23), (18, 19), (13, 14), (9, 16)]],
        7: [[(8, 5), (20, 5), (12, 23)]],
        8: [ellipse(14, 9, 5, 4), ellipse(14, 19, 6, 5)],
        9: [ellipse(14, 10, 5, 5), [(19, 10), (15, 23)]],
    }
    holes = {
        0: [(14, 14, 1.0)],
        4: [(14, 12, 0.5)],
        6: [(13, 18, 1.0)],
        8: [(14, 9, 0.8), (14, 19, 1.0)],
        9: [(14, 10, 1.0)],
    }

    cen = [7 + 4 * i for i in range(4)]

    def make_T(sigma):
        T = np.zeros((10, 7, 4, 4))
        for d in range(10):
            for poly in strokes[d]:
                for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                    L = math.hypot(x1 - x0, y1 - y0)
                    if L < 1e-6:
                        continue
                    th = math.atan2(y1 - y0, x1 - x0) % math.pi
                    n = int(L / 0.5) + 1
                    ow = np.zeros(6)
                    for k, a in enumerate(angles):
                        dd = abs(math.degrees(th) - a)
                        dd = min(dd, 180 - dd)
                        ow[k] = math.exp(-(dd / 25.0) ** 2)
                    for s_ in range(n):
                        f = (s_ + 0.5) / n
                        px = x0 + f * (x1 - x0)
                        py = y0 + f * (y1 - y0)
                        wt = L / n
                        for i in range(4):
                            for j in range(4):
                                r2 = (px - cen[j]) ** 2 + (py - cen[i]) ** 2
                                gw = math.exp(-r2 / (2 * sigma ** 2))
                                T[d, 6, i, j] += wt * gw
                                for k in range(6):
                                    T[d, k, i, j] += wt * gw * ow[k]
        T = T - T.mean(axis=0, keepdims=True)
        T = T - T.mean(axis=(2, 3), keepdims=True)
        for c in range(7):
            m = np.abs(T[:, c]).max()
            if m > 0:
                T[:, c] /= m
        return T

    def make_H(sigma):
        H = np.zeros((10, 4, 4))
        for d, lst in holes.items():
            for (hx, hy, st) in lst:
                for i in range(4):
                    for j in range(4):
                        r2 = (hx - cen[j]) ** 2 + (hy - cen[i]) ** 2
                        H[d, i, j] += st * math.exp(-r2 / (2 * sigma ** 2))
        H = H - H.mean(axis=0, keepdims=True)
        H = H - H.mean(axis=(1, 2), keepdims=True)
        m = np.abs(H).max()
        return H / m

    Tb = make_T(4.0)
    Tn = make_T(2.5)
    Hh = make_H(3.0)
    s = 0.6
    wf = np.zeros((10, 16, 4, 4))
    for k in range(6):
        wf[:, k] = Tb[:, k] * s
        wf[:, 8 + k] = Tn[:, k] * s * 1.3
    wf[:, 6] = Tb[:, 6] * s
    wf[:, 7] = Hh * s * 1.5                   # hole-detector channel
    wf[:, 14] = Tn[:, 6] * s * 0.5
    wf[:, 15] = Tb[:, 6] * s * 0.5
    wfc = wf.reshape(10, 256).astype(np.float32)

    # biases adjusted from step-9 column sums (7 over-, 8 and 4 under-predicted)
    #               0    1     2     3     4     5    6     7     8     9
    fcb = np.array([0.5, 0.1, 0.4, 0.45, -1.0, 0.8, -1.4, -0.1, 0.5, -0.7], np.float32)

    return {
        "conv1.weight": w1,
        "conv1.bias": b1,
        "conv2.weight": w2,
        "conv2.bias": b2,
        "fc.weight": wfc,
        "fc.bias": fcb,
    }
