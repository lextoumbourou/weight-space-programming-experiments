import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
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
        conv1_b[k] = -0.1
    # channels 4..7 unused

    # ---------------- conv2: regional orientation density ----------------
    offsets = [(1, 1), (1, 2), (2, 1), (2, 2)]   # box start (row, col) in 5x5 kernel
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros(16, dtype=np.float64)
    for o in range(4):
        for k, (sy, sx) in enumerate(offsets):
            conv2_w[o * 4 + k, o, sy:sy + 3, sx:sx + 3] = 1.0 / 9.0
    # pool2 cell a with box start s has receptive-field centre 4a + 5.5 + 2s (input px)

    # ---------------- hand-drawn digit prototypes (x=col, y=row) ----------------
    def ell(cx, cy, rx, ry, n=48, tilt=0.0):
        pts = []
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            x, y = rx * math.cos(a), ry * math.sin(a)
            pts.append((cx + x - tilt * y, cy + y))   # tilt>0: top leans right
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
        9: [[ell(14, 9, 5.5, 4.5), [(19.5, 9), (17, 24)]],
            [ell(14, 9, 5, 4.5), [(19, 9), (19, 24)]],
            [ell(15, 9, 5, 4.5), [(20, 9), (14, 24)]]],
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

    sigma = 3.0
    th_o = np.radians(np.array(thetas))

    def feature_template(polys):
        # raw stroke-density template (unnormalised), indexed like fc input
        pts, ws, ths = sample(polys)
        tune = np.clip(np.cos(2 * (ths[:, None] - th_o[None, :])), 0, None)
        T = np.zeros((16, 4, 4))
        for o in range(4):
            for k, (sy, sx) in enumerate(offsets):
                for a in range(4):
                    for b in range(4):
                        cy = 4 * a + 5.5 + 2 * sy
                        cx = 4 * b + 5.5 + 2 * sx
                        d2 = (pts[:, 0] - cx) ** 2 + (pts[:, 1] - cy) ** 2
                        g = np.exp(-d2 / (2 * sigma ** 2))
                        T[o * 4 + k, a, b] = np.sum(ws * tune[:, o] * g)
        return T.reshape(-1)

    alpha = 0.065          # stroke density -> feature units
    templates = np.zeros((10, 256))
    for d in range(10):
        vs = [feature_template(v) for v in variants[d]]
        templates[d] = alpha * np.mean(vs, axis=0)

    # ---------------- fc: nearest-template (squared distance) ----------------
    # logit_c = -s*||f - T_c||^2 + const = 2 s T_c.f - s ||T_c||^2
    s = 4.0
    fc_w = 2.0 * s * templates
    fc_b = -s * np.sum(templates ** 2, axis=1)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
