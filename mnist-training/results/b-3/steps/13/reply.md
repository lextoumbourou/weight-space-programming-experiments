## Approach for step 13

Step 12 reached 64% accuracy with no hand-set biases. That is close to the best so far (65% in step 8), so the nearest-centroid model with scale β works.

Two clear problems remain:

1. **Underconfidence.** The top probabilities in the misclassified examples are only about 0.2–0.3. I double the logit scale, from s = 0.45 to s = 0.9, keeping β = 0.55.
2. **Class imbalance.**
   - Class 4 is predicted only 210 times; 495 true 4s went to 9.
   - Class 5 is predicted only 424 times.
   - Classes 1, 2 and 9 are over-predicted.

   I add bias corrections of about 0.85·log(true count / predicted count). Class 4's correction is capped at +1.3.

Features and templates are unchanged.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1 =================
    # ch0..3: oriented line detectors (0, 45, 90, 135 deg); ch4: ink blur; ch5-7 unused
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

    # ================= conv2: max-pooled maps, single taps =================
    # type 0: ink (ch4); 1: horizontal (ch0); 2: vertical (ch2); 3: diagonal (ch1+ch3)
    type_inputs = [[4], [0], [2], [1, 3]]
    offs = [(2, 2), (2, 3), (3, 2), (3, 3)]       # tap (dy, dx)
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros(16, dtype=np.float64)
    for ty in range(4):
        for k, (dy, dx) in enumerate(offs):
            for ic in type_inputs[ty]:
                conv2_w[ty * 4 + k, ic, dy, dx] = 1.0
    # pool2 cell (a,b) of tap (dy,dx): max over ~8x8 px window centred at
    # (4a + 2dy + 3.5, 4b + 2dx + 3.5)

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
        9: [[ell(14, 10, 6, 5.5), [(20, 10), (18, 24)]],
            [ell(13.5, 9.5, 5.5, 5), [(19, 10), (19, 24)]],
            [ell(15, 9.5, 5.5, 5, tilt=0.2), [(20, 10), (15, 24)]]],
    }

    def sample(polys):
        pts, ths = [], []
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
                    ths.append(th)
        return np.array(pts), np.array(ths)

    th_o = np.radians(np.array(thetas))
    A = [0.8, 0.65, 0.65, 0.65]          # assumed peak feature value per type

    def feature_template(polys):
        pts, ths = sample(polys)
        dth = ths[:, None] - th_o[None, :]
        tune4 = np.clip((np.cos(dth) ** 2 - 0.25) / 0.75, 0, None)
        tunes = [np.ones(len(pts)),
                 tune4[:, 0],
                 tune4[:, 2],
                 np.minimum(1.0, tune4[:, 1] + tune4[:, 3])]
        T = np.zeros((16, 4, 4))
        for ty in range(4):
            for k, (dy, dx) in enumerate(offs):
                for a in range(4):
                    for b in range(4):
                        cy = 4 * a + 2 * dy + 3.5
                        cx = 4 * b + 2 * dx + 3.5
                        d = np.sqrt((pts[:, 0] - cx) ** 2 + (pts[:, 1] - cy) ** 2)
                        e = np.maximum(0.0, d - 2.5)
                        v = tunes[ty] * np.exp(-e * e / 8.0)
                        T[ty * 4 + k, a, b] = A[ty] * v.max()
        return T

    mu = np.zeros((10, 256))
    for d in range(10):
        acc = np.zeros((16, 4, 4))
        for var in variants[d]:
            acc += feature_template(var)
        mu[d] = (acc / len(variants[d])).reshape(-1)

    # ================= fc: nearest centroid with global scale beta =================
    beta = 0.55
    s = 0.9
    fc_w = 2.0 * s * beta * mu
    fc_b = -s * beta ** 2 * np.sum(mu ** 2, axis=1)
    # class-balance correction from step-12 prediction counts (~0.85*log(true/pred))
    #                  0      1      2     3     4     5     6      7     8      9
    corr = np.array([-0.08, -0.42, -0.26, 0.12, 1.30, 0.65, -0.18, 0.10, 0.15, -0.26])
    fc_b = fc_b + corr

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
