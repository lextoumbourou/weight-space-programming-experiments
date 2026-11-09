This step corrects the template geometry and rebalances the biases:

- **Wider digits:** I suspect my templates were too narrow, since a real MNIST 0 is roughly 15–16 px wide. All digits are widened, which should mainly help the 0→6 confusion.
- **Forbidden strokes:** the 6 gets a stronger penalty in its upper right (vertical and horizontal), and the 2 loses its left-middle penalty.
- **Biases:** the 2 bias is restored after it was over-penalised, 6, 7 and 9 are lowered, and 8 is raised.
- **Gain:** raised slightly from 8 to 11, with biases scaled to match.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    # Filter k responds to strokes with direction angle phi_k = k*pi/8 (image coords).
    K = 8
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    for k in range(K):
        phi = k * math.pi / K
        ker = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                x, y = j - 2, i - 2
                d = -x * math.sin(phi) + y * math.cos(phi)
                ker[i, j] = math.exp(-d * d / (2 * 0.9 ** 2))
        ker -= ker.mean()
        ker /= ker[ker > 0].sum()
        conv1_w[k, 0] = ker
    conv1_b = np.full((8,), -0.05, dtype=np.float32)

    # ---------------- conv2: local spatial averaging per orientation ----------------
    # Channel k     : orientation k, window offset 0 -> cell centres 4r+6.5 px
    # Channel 8 + k : orientation k, window offset 1 -> cell centres 4r+8.5 px
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    w1 = np.array([0.5, 1.0, 1.0, 0.5])
    w2 = np.outer(w1, w1) / 9.0
    for k in range(K):
        conv2_w[k, k, 0:4, 0:4] = w2
        conv2_w[8 + k, k, 1:5, 1:5] = w2
    conv2_b = np.zeros((16,), dtype=np.float32)
    offsets = [6.5, 8.5]

    # ---------------- stroke descriptions ----------------
    def arc(cx, cy, rx, ry, a0, a1, n=24):
        # angle 0 = right, 90 = bottom, 180 = left, 270 = top (y down)
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * t / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * t / n)))
                for t in range(n + 1)]

    pos = {}
    neg = {}
    pos[0] = [(16, [arc(.5, .5, .5, .5, 0, 360, 40)]),
              (13, [arc(.5, .5, .5, .5, 0, 360, 40)])]
    # 0: nothing in the centre, in any orientation
    neg[0] = [[(.5, .3), (.5, .7)], [(.3, .5), (.7, .5)],
              [(.35, .35), (.65, .65)], [(.65, .35), (.35, .65)]]
    pos[1] = [(10, [[(.5, 0), (.5, 1)]]),
              (10, [[(.65, 0), (.35, 1)]]),
              (10, [[(.9, 0), (.1, 1)]])]
    # 1: no horizontal through the middle, no parallel strokes at the sides
    neg[1] = [[(.1, .5), (.9, .5)], [(-.2, .2), (-.2, .8)], [(1.2, .2), (1.2, .8)]]
    two_a = arc(.5, .25, .45, .25, 200, 420) + [(.05, 1.0), (1.0, .97)]
    two_b = arc(.5, .25, .45, .25, 200, 420) + [(.1, .9)] + \
        arc(.25, .88, .15, .1, 180, 450, 12) + [(1.0, 1.0)]
    pos[2] = [(15, [two_a]), (15, [two_b])]
    # 2: no vertical at lower right
    neg[2] = [[(.95, .55), (.95, .85)]]
    pos[3] = [(13, [arc(.45, .25, .4, .25, 200, 450),
                    arc(.45, .75, .45, .25, 270, 520)])]
    # 3: no vertical on the left side
    neg[3] = [[(.1, .15), (.1, .45)], [(.05, .55), (.05, .8)]]
    pos[4] = [(14, [[(.15, 0), (.05, .6), (1.0, .6)], [(.7, 0), (.7, 1)]]),
              (14, [[(.7, 0), (.0, .65), (1.0, .65)], [(.7, 0), (.7, 1)]])]
    # 4: no horizontal bar at top or bottom
    neg[4] = [[(.2, 0), (.7, 0)], [(.1, 1), (.9, 1)]]
    pos[5] = [(14, [[(.9, 0), (.25, 0), (.2, .45)],
                    arc(.45, .7, .45, .3, 230, 530)])]
    # 5: no vertical at upper right
    neg[5] = [[(.85, .1), (.85, .4)]]
    pos[6] = [(13, [[(.8, 0), (.45, .2), (.2, .45), (.12, .7)],
                    arc(.5, .72, .4, .28, 0, 360, 30)])]
    # 6: no vertical at upper right (that is a 0), no horizontal bar at top right (that is a 5)
    neg[6] = [[(.9, .0), (.9, .45)], [(1.0, .05), (1.0, .4)], [(.45, 0), (1.0, 0)]]
    pos[7] = [(14, [[(0, .03), (1, .03), (.4, 1)]]),
              (14, [[(0, .03), (1, .03), (.4, 1)], [(.3, .5), (.85, .5)]])]
    # 7: no vertical at upper left
    neg[7] = [[(.05, .15), (.05, .45)]]
    pos[8] = [(12, [arc(.5, .25, .35, .25, 0, 360, 30),
                    arc(.5, .75, .42, .25, 0, 360, 30)])]
    neg[8] = []
    pos[9] = [(12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.8, 1.0)]]),
              (12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.5, 1.0)]])]
    # 9: no vertical at lower left
    neg[9] = [[(.1, .65), (.1, .95)]]

    sigma_s = 3.0
    shears = [0.0, 0.25]
    neg_w = 0.7

    def sample(polylines, width, shear):
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
        return np.array(X), np.array(Y), np.array(PHI), np.array(DS)

    def splat(X, Y, PHI, DS):
        # deposit stroke points into (orientation channel, cell) feature space
        T = np.zeros((16, 4, 4))
        if len(X) == 0:
            return T
        for k in range(K):
            ow = np.maximum(0.0, np.cos(2 * (PHI - k * math.pi / K))) ** 2
            for s in range(2):
                for r in range(4):
                    for c in range(4):
                        cy = 4 * r + offsets[s]
                        cx = 4 * c + offsets[s]
                        g = np.exp(-((Y - cy) ** 2 + (X - cx) ** 2) / (2 * sigma_s ** 2))
                        T[s * 8 + k, r, c] = (DS * ow * g).sum()
        return np.tanh(T / 5.0)

    def draw_template(width, p_lines, n_lines, shear):
        X, Y, PHI, DS = sample(p_lines, width, shear)
        # centre of mass of the positive strokes goes to the image centre
        mx = (X * DS).sum() / DS.sum() - 13.5
        my = (Y * DS).sum() / DS.sum() - 13.5
        P = splat(X - mx, Y - my, PHI, DS)
        Xn, Yn, PHIn, DSn = sample(n_lines, width, shear)
        N = splat(Xn - mx, Yn - my, PHIn, DSn) if len(Xn) else np.zeros((16, 4, 4))
        return P, N

    # ---------------- fc: contrastive, zero-mean, unit-norm templates ----------------
    gain = 11.0
    Ps, Ns = [], []
    for d in range(10):
        P = np.zeros((16, 4, 4))
        N = np.zeros((16, 4, 4))
        cnt = 0
        for (width, pls) in pos[d]:
            for sh in shears:
                p, n = draw_template(width, pls, neg[d], sh)
                P += p
                N += n
                cnt += 1
        P = (P / cnt).reshape(-1)
        N = (N / cnt).reshape(-1)
        Ps.append(P / np.linalg.norm(P))
        Ns.append(N / np.linalg.norm(P))
    mean_all = np.mean(Ps, axis=0)  # mean of the ten hand-drawn templates

    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        v = Ps[d] - 0.5 * mean_all - neg_w * Ns[d]
        v = v - v.mean()
        v = v / np.linalg.norm(v)
        fc_w[d] = (gain * v).astype(np.float32)

    # biases tuned from the confusion matrices (expressed at gain 8, then rescaled)
    fc_b = np.array([0.5, -0.3, -0.1, -0.1, 0.3, 0.2, -0.6, -0.4, 0.8, -0.4],
                    dtype=np.float32) * (gain / 8.0)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
