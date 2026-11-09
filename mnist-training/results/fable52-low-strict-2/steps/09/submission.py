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

    pos = {}   # the digit's strokes (variants)
    neg = {}   # strokes that must NOT be there
    emp = {}   # strokes that get extra positive weight (distinguishing parts)
    pos[0] = [(16, [arc(.5, .5, .5, .5, 0, 360, 40)]),
              (13, [arc(.5, .5, .5, .5, 0, 360, 40)])]
    # 0: no horizontal stroke in the centre (kept short so it does not touch the ring)
    neg[0] = [[(.38, .5), (.62, .5)]]
    emp[0] = []
    pos[1] = [(10, [[(.5, 0), (.5, 1)]]),
              (10, [[(.65, 0), (.35, 1)]]),
              (10, [[(.9, 0), (.1, 1)]])]
    # 1: no horizontal through the middle / top / bottom, no parallel strokes at the sides
    neg[1] = [[(.1, .5), (.9, .5)], [(-.2, .2), (-.2, .8)], [(1.2, .2), (1.2, .8)],
              [(.1, 0), (.9, 0)], [(.1, 1), (.9, 1)]]
    emp[1] = []
    two_a = arc(.5, .25, .45, .25, 200, 420) + [(.05, 1.0), (1.0, .97)]
    two_b = arc(.5, .25, .45, .25, 200, 420) + [(.1, .9)] + \
        arc(.25, .88, .15, .1, 180, 450, 12) + [(1.0, 1.0)]
    two_c = arc(.5, .22, .4, .22, 190, 400) + [(.0, .95), (1.0, .9)]   # smaller top, rising base
    pos[2] = [(15, [two_a]), (15, [two_b]), (12, [two_c]), (12, [two_b])]
    # 2: no vertical at lower right
    neg[2] = [[(.95, .55), (.95, .85)]]
    # 2: the long "/" diagonal and the base line are what make it a 2
    emp[2] = [[(.7, .5), (.1, .95)], [(.1, .98), (1.0, .97)]]
    pos[3] = [(13, [arc(.45, .25, .4, .25, 200, 450),
                    arc(.45, .75, .45, .25, 270, 520)])]
    # 3: no vertical on the left side, no "/" diagonal in the lower left (that is a 2)
    neg[3] = [[(.1, .15), (.1, .45)], [(.05, .55), (.05, .8)], [(.1, .92), (.5, .6)]]
    emp[3] = []
    pos[4] = [(14, [[(.15, 0), (.05, .6), (1.0, .6)], [(.7, 0), (.7, 1)]]),
              (14, [[(.7, 0), (.0, .65), (1.0, .65)], [(.7, 0), (.7, 1)]])]
    # 4: no horizontal bar at top or bottom
    neg[4] = [[(.2, 0), (.7, 0)], [(.1, 1), (.9, 1)]]
    # 4: left arm and the bar sticking out to the right of the stem
    emp[4] = [[(.1, .1), (.05, .55)], [(.75, .62), (1.0, .62)]]
    pos[5] = [(14, [[(.9, 0), (.25, 0), (.2, .45)],
                    arc(.45, .7, .45, .3, 230, 530)])]
    # 5: no vertical at upper right (3), no vertical at lower left (6)
    neg[5] = [[(.85, .1), (.85, .4)], [(.0, .55), (.0, .8)]]
    # 5: top bar and upper-left stem
    emp[5] = [[(.9, 0), (.3, 0)], [(.25, 0), (.2, .45)]]
    loop6 = arc(.5, .72, .4, .28, 0, 360, 30)
    pos[6] = [(13, [[(.8, 0), (.45, .2), (.2, .45), (.12, .7)], loop6]),
              (13, [[(.65, 0), (.3, .25), (.15, .5), (.12, .75)], loop6])]   # more upright stem
    # 6: no vertical at upper right (that is a 0), no horizontal bar at top right (that is a 5)
    neg[6] = [[(.9, .0), (.9, .45)], [(1.0, .05), (1.0, .4)], [(.45, 0), (1.0, 0)]]
    # 6: closed left side of the lower loop
    emp[6] = [[(.1, .5), (.1, .9)]]
    pos[7] = [(14, [[(0, .03), (1, .03), (.4, 1)]]),
              (14, [[(0, .03), (1, .03), (.4, 1)]]),
              (14, [[(0, .03), (1, .03), (.4, 1)], [(.3, .5), (.85, .5)]])]  # crossed 7 (rarer)
    # 7: no vertical at upper left, no loop bottom at middle left (that is a 9)
    neg[7] = [[(.05, .15), (.05, .45)], [(.0, .5), (.4, .5)]]
    emp[7] = []
    eight_x = arc(.5, .22, .3, .22, 330, 180, 14) + [(.25, .35), (.75, .65)] + \
        arc(.5, .78, .35, .22, -40, 220, 20) + [(.23, .64), (.78, .33)]
    pos[8] = [(12, [arc(.5, .25, .35, .25, 0, 360, 30),
                    arc(.5, .75, .42, .25, 0, 360, 30)]),
              (12, [eight_x])]                                              # crossing figure-eight
    neg[8] = []
    emp[8] = []
    pos[9] = [(12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.8, 1.0)]]),
              (12, [arc(.45, .28, .4, .28, 0, 360, 30), [(.85, .28), (.5, 1.0)]])]
    # 9: no vertical at lower left
    neg[9] = [[(.1, .65), (.1, .95)]]
    # 9: left half of the loop (absent in 7 and open 4)
    emp[9] = [arc(.45, .28, .4, .28, 90, 270, 12)]

    sigma_s = 3.0
    shears = [0.0, 0.25]
    neg_w = 0.7
    emp_w = 0.4

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

    def draw_template(width, p_lines, n_lines, e_lines, shear):
        X, Y, PHI, DS = sample(p_lines, width, shear)
        # centre of mass of the positive strokes goes to the image centre
        mx = (X * DS).sum() / DS.sum() - 13.5
        my = (Y * DS).sum() / DS.sum() - 13.5
        P = splat(X - mx, Y - my, PHI, DS)
        Xn, Yn, PHIn, DSn = sample(n_lines, width, shear)
        N = splat(Xn - mx, Yn - my, PHIn, DSn)
        Xe, Ye, PHIe, DSe = sample(e_lines, width, shear)
        E = splat(Xe - mx, Ye - my, PHIe, DSe)
        return P, N, E

    # ---------------- fc: contrastive, zero-mean, unit-norm templates ----------------
    gain = 8.0
    Ps, Ns, Es = [], [], []
    for d in range(10):
        P = np.zeros((16, 4, 4))
        N = np.zeros((16, 4, 4))
        E = np.zeros((16, 4, 4))
        cnt = 0
        for (width, pls) in pos[d]:
            for sh in shears:
                p, n, e = draw_template(width, pls, neg[d], emp[d], sh)
                P += p
                N += n
                E += e
                cnt += 1
        P = (P / cnt).reshape(-1)
        N = (N / cnt).reshape(-1)
        E = (E / cnt).reshape(-1)
        nrm = np.linalg.norm(P)
        Ps.append(P / nrm)
        Ns.append(N / nrm)
        Es.append(E / nrm)
    mean_all = np.mean(Ps, axis=0)  # mean of the ten hand-drawn templates

    # Hand-chosen "confuser" list: for digit d, the digits that were wrongly called d
    # (read off the confusion matrices), with a weight. Their templates are subtracted.
    confusers = {
        0: {2: 1.0, 6: 0.8, 9: 0.5, 8: 0.4},
        1: {8: 1.8, 2: 1.6, 6: 0.9, 9: 0.3},
        2: {8: 2.2, 0: 1.4, 5: 1.1, 6: 0.6, 4: 0.7, 1: 0.8, 3: 0.8},
        3: {2: 1.8, 5: 0.6, 7: 0.5, 9: 0.4},
        4: {9: 1.2, 2: 1.1, 6: 1.0},
        5: {3: 2.6},
        6: {0: 1.0, 5: 2.4, 9: 0.4},
        7: {9: 3.2, 3: 1.6, 8: 1.3, 2: 0.9},
        8: {5: 1.4, 3: 0.8, 6: 0.7, 2: 0.6, 4: 0.6},
        9: {7: 2.4, 4: 2.0, 2: 0.7, 8: 0.5, 6: 0.3},
    }
    gamma = 0.12

    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        v = Ps[d] - 0.6 * mean_all - neg_w * Ns[d] + emp_w * Es[d]
        for c, wgt in confusers[d].items():
            v = v - gamma * wgt * Ps[c]
        v = v - v.mean()
        v = v / np.linalg.norm(v)
        fc_w[d] = (gain * v).astype(np.float32)

    # biases re-balanced from the step-8 predicted-count totals
    fc_b = np.array([0.45, -0.9, -0.4, -0.15, 0.4, 0.62, -0.33, -0.6, 1.35, 0.05],
                    dtype=np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
