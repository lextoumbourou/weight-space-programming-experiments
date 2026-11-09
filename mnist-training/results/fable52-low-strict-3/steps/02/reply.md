**Step 2 changes:** the confusion matrix shows the dense templates with few stroke ends (8 and 6) being over-predicted, and slanted 1s leaking into 2 and 8.

- **Stronger penalties:** I raise the penalty for feature energy where a template expects none, especially on the stroke-end channels, since 8 and 0 have no ends and 6 has only one.
- **Slanted 1:** I add a second, fainter slanted stroke to the hand-drawn "1" template.
- **Logit scale:** I raise it from 3 to 5, guessing that the high loss comes from logits that are too flat.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: 4 oriented bar detectors + 4 stroke-end detectors -------------
    w1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.full((8,), -0.1, dtype=np.float32)   # small threshold against weak responses
    bar_angles = [0.0, 45.0, 90.0, 135.0]        # stroke direction, x right / y down
    for k, a in enumerate(bar_angles):
        th = math.radians(a)
        f = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                y, x = r - 2, c - 2
                d = -math.sin(th) * x + math.cos(th) * y   # distance perpendicular to the bar
                f[r, c] = math.exp(-d * d / 2.0)
        f -= f.mean()                 # zero-sum: no response to flat ink
        w1[k, 0] = f / 3.6            # an aligned 3px stroke gives ~1
    # End detector "up": stroke comes from below and stops at the centre.
    p = np.array([-0.5, 0.25, 0.5, 0.25, -0.5])      # zero-sum lateral profile (vertical bar)
    n = np.array([-0.3, -0.6, -0.9, -0.6, -0.3])     # penalty if ink continues above
    e_up = np.stack([n, n, p, p, p]) / 3.0
    e_down = np.flipud(e_up)
    e_left = e_up.T                   # ink to the right, end pointing left
    e_right = np.fliplr(e_left)
    w1[4, 0] = e_up
    w1[5, 0] = e_down
    w1[6, 0] = e_left
    w1[7, 0] = e_right
    end_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]    # outward direction for channels 4..7

    # ---------------- conv2: soft spatial binning of each conv1 feature ---------------------
    w2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros((16,), dtype=np.float32)
    k1 = np.array([1.0, 2.0, 1.0]) / 4.0
    k3 = np.outer(k1, k1)
    for c in range(8):
        gain = 1.0 if c < 4 else 2.0   # end features are point-like, so boost them
        w2[c, c, 1:4, 1:4] = k3 * gain
    # channels 8..15 unused (zero) for now

    # ---------------- hand-drawn digit strokes (unit coords, y down) ------------------------
    def arc(cx, cy, rx, ry, a0, a1, npts=40):
        pts = []
        for i in range(npts + 1):
            a = math.radians(a0 + (a1 - a0) * i / npts)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        return pts

    digits = {}
    # each digit: (list of (points, start_is_end, end_is_end, stroke_weight),
    #              list of extra corner marks (x,y,ux,uy,w))
    digits[0] = ([(arc(.5, .5, .36, .5, 0, 360), False, False, 1.0)], [])
    # "1": upright stroke plus a fainter slanted variant drawn over it
    digits[1] = ([([(.55, 0.), (.45, 1.)], True, True, 0.6),
                  ([(.75, 0.), (.25, 1.)], True, True, 0.4)], [])
    digits[2] = ([(arc(.45, .28, .33, .28, 200, 400) + [(.1, 1.0), (.92, 1.0)], True, True, 1.0)],
                 [(.1, 1.0, -1, 0, .7), (.1, 1.0, 0, 1, .5)])
    digits[3] = ([(arc(.45, .26, .3, .26, 215, 450) + arc(.45, .76, .36, .24, 270, 510),
                   True, True, 1.0)],
                 [(.42, .52, -1, 0, .6)])
    digits[4] = ([([(.22, 0.), (.08, .62), (.95, .62)], True, True, 1.0),
                  ([(.7, 0.), (.66, 1.0)], True, True, 1.0)],
                 [(.08, .62, -1, 0, .6), (.08, .62, 0, 1, .5)])
    digits[5] = ([([(.88, 0.), (.3, 0.), (.25, .42)] + arc(.45, .68, .37, .3, 230, 510),
                   True, True, 1.0)],
                 [(.3, 0., 0, -1, .6), (.3, 0., -1, 0, .6), (.23, .44, -1, 0, .3), (.23, .44, 0, 1, .3)])
    digits[6] = ([([(.8, 0.), (.5, .17), (.28, .42), (.18, .72)] + arc(.48, .72, .3, .27, 180, -180),
                   True, False, 1.0)], [])
    digits[7] = ([([(.05, 0.), (.92, 0.), (.42, 1.0)], True, True, 1.0)],
                 [(.92, 0., 0, -1, .6), (.92, 0., 1, 0, .6)])
    eight = [(0.5 + 0.3 * math.sin(2 * t), 0.5 - 0.5 * math.cos(t))
             for t in np.linspace(0, 2 * math.pi, 81)]
    digits[8] = ([(eight, False, False, 1.0)], [])
    digits[9] = ([(arc(.45, .28, .3, .27, 0, -360) + [(.66, 1.0)], False, True, 1.0)], [])

    # ---------------- draw strokes directly into the (8 feature, 4x4 cell) template ---------
    centers = [7.5 + 4 * i for i in range(4)]        # cell centres in input pixels

    def win(d):                                       # soft cell window (matches conv2 binning)
        return min(1.0, max(0.0, (5.5 - abs(d)) / 3.5))

    def render(strokes, extras):
        # bounding box and length-weighted centroid -> 20px box, centred like MNIST
        allp = [q for s in strokes for q in s[0]]
        xs = [q[0] for q in allp]
        ys = [q[1] for q in allp]
        sc = 17.0 / max(max(xs) - min(xs), max(ys) - min(ys))
        tot = 0.0
        mx = 0.0
        my = 0.0
        for pts, _, _, sw in strokes:
            for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
                L = math.hypot(x1 - x0, y1 - y0) * sw
                tot += L
                mx += L * (x0 + x1) / 2
                my += L * (y0 + y1) / 2
        mx /= tot
        my /= tot

        def tr(q):
            return ((q[0] - mx) * sc + 13.5, (q[1] - my) * sc + 13.5)

        T = np.zeros((8, 4, 4))

        def add_end(x, y, ux, uy, w):
            nrm = math.hypot(ux, uy) + 1e-9
            ux, uy = ux / nrm, uy / nrm
            for k, (dx, dy) in enumerate(end_dirs):
                t = max(0.0, ux * dx + uy * dy) ** 2
                if t <= 0:
                    continue
                for i in range(4):
                    for j in range(4):
                        T[4 + k, i, j] += w * t * win(y - centers[i]) * win(x - centers[j])

        for pts, s_end, e_end, sw in strokes:
            P = [tr(q) for q in pts]
            for (x0, y0), (x1, y1) in zip(P[:-1], P[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-9:
                    continue
                th = math.atan2(y1 - y0, x1 - x0)
                ns = int(math.ceil(L / 0.25))
                dl = L / ns
                for m in range(ns):
                    f = (m + 0.5) / ns
                    x = x0 + f * (x1 - x0)
                    y = y0 + f * (y1 - y0)
                    wy = [win(y - c) for c in centers]
                    wx = [win(x - c) for c in centers]
                    for o, a in enumerate(bar_angles):
                        tun = math.cos(th - math.radians(a)) ** 4   # orientation tuning of bars
                        for i in range(4):
                            if wy[i] == 0:
                                continue
                            for j in range(4):
                                T[o, i, j] += sw * dl / 8.0 * tun * wy[i] * wx[j]
            if s_end:
                add_end(P[0][0], P[0][1], P[0][0] - P[1][0], P[0][1] - P[1][1], sw)
            if e_end:
                add_end(P[-1][0], P[-1][1], P[-1][0] - P[-2][0], P[-1][1] - P[-2][1], sw)
        for (x, y, ux, uy, w) in extras:
            X, Y = tr((x, y))
            add_end(X, Y, ux, uy, w)
        return T

    # ---------------- fc: normalised template per class, penalty where it is empty ----------
    fcw = np.zeros((10, 256), dtype=np.float32)
    fcb = np.zeros((10,), dtype=np.float32)
    GAIN = 5.0        # logit scale
    BETA_BAR = 0.07   # penalty for stroke energy where the template has none
    BETA_END = 0.12   # penalty for stroke ends/corners where the template has none
    TAU = 0.1
    beta = np.zeros((8, 4, 4))
    beta[:4] = BETA_BAR
    beta[4:] = BETA_END
    beta = beta.reshape(-1)
    for d in range(10):
        T = render(*digits[d])
        v = T.reshape(-1)                         # (channel, row, col) order, channels 0..7
        pos = v / (np.linalg.norm(v) + 1e-9)
        pen = np.clip(1.0 - v / TAU, 0.0, 1.0) * beta
        fcw[d, :128] = (GAIN * (pos - pen)).astype(np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
