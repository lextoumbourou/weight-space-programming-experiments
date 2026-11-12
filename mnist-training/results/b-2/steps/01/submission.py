import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 orientations x 2 polarities of edge detectors ----------------
    # Orientation angles (math convention, y pointing UP): 0 = horizontal stroke, 45 = "/",
    # 90 = vertical, 135 = "\".
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    def edge_kernel(theta):
        # Derivative-of-Gaussian across the stroke direction, elongated along it.
        K = np.zeros((5, 5))
        ct, st = math.cos(theta), math.sin(theta)
        for r in range(5):
            for c in range(5):
                u = c - 2          # x (right)
                v = -(r - 2)       # y (up)
                a = u * ct + v * st        # coordinate along the stroke
                n = -u * st + v * ct       # coordinate across the stroke
                K[r, c] = n * math.exp(-a * a / (2 * 1.5 ** 2) - n * n / (2 * 1.0 ** 2))
        K /= K[K > 0].sum()   # full-contrast step edge -> response ~1
        return K

    for k, th in enumerate(thetas):
        K = edge_kernel(th)
        conv1_w[2 * k, 0] = K       # edge with ink on the +normal side
        conv1_w[2 * k + 1, 0] = -K  # edge with ink on the -normal side
        conv1_b[2 * k] = -0.25      # threshold: sharpens orientation tuning, kills noise
        conv1_b[2 * k + 1] = -0.25

    # ---------------- conv2: orientation energy maps (sum of polarities, 3x3 blur) -------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15
    # channels 4..15 unused (all-zero -> output 0)

    # ---------------- fc: hand-drawn stroke templates in the 4x4x4 feature space ----------------
    # final cell m (row or column) covers input pixels about 4m+4..4m+11, centre 4m+7.5
    cell_c = np.array([7.5 + 4 * m for m in range(4)])

    def ellipse(cx, cy, rx, ry, a0=0.0, a1=360.0, n=40):
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        return pts

    # Digit prototypes: lists of polylines, points are (x=column, y=row) in input pixels.
    strokes = {
        0: [ellipse(14, 14, 5.5, 9.0)],
        1: [[(15.5, 4), (13, 23.5)]],
        2: [[(8, 8), (10, 5), (14, 4), (18, 5), (20, 8), (19, 12), (15, 16),
             (11, 20), (8, 23), (14, 23), (21, 23)]],
        3: [[(8, 6), (12, 4), (17, 4), (20, 7), (19, 11), (14, 13), (19, 15),
             (21, 19), (18, 23), (12, 24), (8, 22)]],
        4: [[(13, 4), (9, 12), (7, 16), (15, 16), (22, 16)],
            [(18, 8), (17, 24)]],
        5: [[(20, 4), (10, 4), (9, 12), (14, 11), (19, 13), (21, 18), (18, 22),
             (13, 23), (8, 21)]],
        6: [[(17, 4), (12, 8), (9, 14), (9, 19), (12, 23), (16, 23), (19, 19),
             (18, 15), (14, 13), (10, 16)]],
        7: [[(8, 5), (21, 5), (17, 12), (14, 18), (13, 24)]],
        8: [ellipse(14, 8.5, 4.5, 4.5), ellipse(14, 18.5, 5.5, 5.0)],
        9: [ellipse(14, 9, 5.0, 4.5), [(19, 9), (17, 24)]],
    }

    sig = 2.5  # spatial spread of a stroke sample over the cells

    def template(polys):
        T = np.zeros((4, 4, 4))  # [orientation, cell row, cell col]
        for poly in polys:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(-dy, dx) % math.pi   # stroke angle, y up
                ow = np.array([max(0.0, math.cos(2 * (phi - th))) ** 2 for th in thetas])
                ns = max(1, int(L / 0.5))
                for i in range(ns):
                    t = (i + 0.5) / ns
                    x = x0 + t * dx
                    y = y0 + t * dy
                    sy = np.exp(-(y - cell_c) ** 2 / (2 * sig ** 2))
                    sx = np.exp(-(x - cell_c) ** 2 / (2 * sig ** 2))
                    T += ow[:, None, None] * sy[None, :, None] * sx[None, None, :] * (L / ns)
        return T

    temps = np.zeros((10, 4, 4, 4))
    for d in range(10):
        T = template(strokes[d])
        temps[d] = T / np.linalg.norm(T)
    temps -= temps.mean(axis=0, keepdims=True)   # keep only what distinguishes digits

    alpha = 6.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        # features flattened as (channel, row, col); only channels 0..3 used
        fc_w[d, :64] = alpha * temps[d].reshape(-1)
    fc_b = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
