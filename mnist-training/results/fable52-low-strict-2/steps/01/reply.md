This first step builds a hand-designed, HOG-like pipeline; later steps will tune it from the confusion matrix.

- **conv1:** 8 oriented line detectors, one every 22.5°.
- **conv2:** each orientation map is locally averaged at two diagonally offset positions, so the 16 channels give 8 orientations on two interleaved 4x4 grids.
- **fc:** one template per digit, drawn directly in feature space from pen strokes I describe by hand (polylines and arcs). Each stroke point adds to the orientation channel and grid cell it should excite. Templates are made zero-mean so that ink in unexpected places is penalised.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    # Filter k responds to strokes whose direction (in image coords, x=col, y=row)
    # has angle phi_k = k*pi/8 (mod pi). Zero-mean so flat ink gives no response.
    K = 8
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    for k in range(K):
        phi = k * math.pi / K
        ker = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                x, y = j - 2, i - 2
                d = -x * math.sin(phi) + y * math.cos(phi)  # distance to line
                ker[i, j] = math.exp(-d * d / (2 * 0.9 ** 2))
        ker -= ker.mean()
        ker /= ker[ker > 0].sum()
        conv1_w[k, 0] = ker
    conv1_b = np.full((8,), -0.05, dtype=np.float32)  # small threshold vs noise

    # ---------------- conv2: local spatial averaging per orientation ----------------
    # Channel k      : orientation k, 4x4 window at kernel offset 0 -> cell centres 4r+6.5 px
    # Channel 8 + k  : orientation k, 4x4 window at kernel offset 1 -> cell centres 4r+8.5 px
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    w1 = np.array([0.5, 1.0, 1.0, 0.5])
    w2 = np.outer(w1, w1) / 9.0
    for k in range(K):
        conv2_w[k, k, 0:4, 0:4] = w2
        conv2_w[8 + k, k, 1:5, 1:5] = w2
    conv2_b = np.zeros((16,), dtype=np.float32)
    offsets = [6.5, 8.5]  # pixel centre of cell r is 4*r + offset, for the two sets

    # ---------------- stroke descriptions of the digits ----------------
    # Normalised coords: u in [0,1] left->right, v in [0,1] top->bottom.
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        # angle 0 = right, 90 = bottom, 180 = left, 270 = top (y points down)
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * t / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
                for t in range(n + 1)]

    # each digit: list of variants; each variant: (width_px, [polylines])
    digits = {}
    digits[0] = [(13, [arc(.5, .5, .5, .5, 0, 360, 40)]),
                 (10, [arc(.5, .5, .5, .5, 0, 360, 40)])]
    digits[1] = [(10, [[(.5, 0), (.5, 1)]]),
                 (10, [[(.65, 0), (.35, 1)]]),
                 (10, [[(.9, 0), (.1, 1)]])]
    two_a = arc(.5, .25, .45, .25, 200, 420) + [(.05, 1.0), (1.0, .97)]
    two_b = arc(.5, .25, .45, .25, 200, 420) + [(.1, .9)] + \
        arc(.25, .88, .15, .1, 180, 450, 12) + [(1.0, 1.0)]  # with loop at the base
    digits[2] = [(13, [two_a]), (13, [two_b])]
    digits[3] = [(12, [arc(.45, .25, .4, .25, 200, 450),
                       arc(.45, .75, .45, .25, 270, 520)])]
    digits[4] = [(13, [[(.15, 0), (.05, .6), (1.0, .6)], [(.7, 0), (.7, 1)]]),      # open top
                 (13, [[(.7, 0), (.0, .65), (1.0, .65)], [(.7, 0), (.7, 1)]])]      # closed top
    digits[5] = [(12, [[(.9, 0), (.25, 0), (.2, .45)],
                       arc(.45, .7, .45, .3, 230, 530)])]
    digits[6] = [(12, [[(.8, 0), (.45, .2), (.2, .45), (.12, .7)],
                       arc(.5, .72, .4, .28, 0, 360, 30)])]
    digits[7] = [(12, [[(0, .03), (1, .03), (.4, 1)]]),
                 (12, [[(0, .03), (1, .03), (.4, 1)], [(.3, .5), (.85, .5)]])]      # crossed 7
    digits[8] = [(11, [arc(.5, .25, .35, .25, 0, 360, 30),
                       arc(.5, .75, .42, .25, 0, 360, 30)])]
    digits[9] = [(12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.8, 1.0)]]),
                 (12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.5, 1.0)]])]

    sigma_s = 3.0          # spatial tolerance of a cell (px)
    shears = [0.0, 0.25]   # upright and right-slanted handwriting

    def draw_template(width, polylines, shear):
        # Draw the strokes directly into feature space (orientation x cell grid).
        X, Y, PHI, DS = [], [], [], []
        for pl in polylines:
            for (u0, v0), (u1, v1) in zip(pl[:-1], pl[1:]):
                y0, y1 = v0 * 20.0, v1 * 20.0
                x0 = u0 * width - shear * (y0 - 10.0)
                x1 = u1 * width - shear * (y1 - 10.0)
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.25))
                phi = math.atan2(y1 - y0, x1 - x0)
                for t in range(n):
                    a = (t + 0.5) / n
                    X.append(x0 + a * (x1 - x0))
                    Y.append(y0 + a * (y1 - y0))
                    PHI.append(phi)
                    DS.append(L / n)
        X, Y, PHI, DS = map(np.array, (X, Y, PHI, DS))
        # MNIST centres digits by centre of mass
        X = X - (X * DS).sum() / DS.sum() + 13.5
        Y = Y - (Y * DS).sum() / DS.sum() + 13.5
        T = np.zeros((16, 4, 4))
        for k in range(K):
            ow = np.maximum(0.0, np.cos(2 * (PHI - k * math.pi / K))) ** 2  # orientation tuning
            for s in range(2):
                for r in range(4):
                    for c in range(4):
                        cy = 4 * r + offsets[s]
                        cx = 4 * c + offsets[s]
                        g = np.exp(-((Y - cy) ** 2 + (X - cx) ** 2) / (2 * sigma_s ** 2))
                        T[s * 8 + k, r, c] = (DS * ow * g).sum()
        return np.tanh(T / 5.0)  # saturate: pooled features do not grow with stroke length

    # ---------------- fc: zero-mean, unit-norm matched templates ----------------
    gain = 8.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        T = np.zeros((16, 4, 4))
        cnt = 0
        for (width, pls) in digits[d]:
            for sh in shears:
                T += draw_template(width, pls, sh)
                cnt += 1
        T /= cnt
        v = T.reshape(-1)          # (channel, row, col) order, same as Flatten
        v = v / np.linalg.norm(v)
        v = v - v.mean()           # penalise ink where this digit has none
        v = v / np.linalg.norm(v)
        fc_w[d] = (gain * v).astype(np.float32)
    fc_b = np.zeros((10,), dtype=np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
