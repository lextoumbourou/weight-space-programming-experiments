import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    thetas = [k * math.pi / 8 for k in range(8)]   # line direction; 0=horizontal, pi/2=vertical (y down)
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    for k, th in enumerate(thetas):
        D = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                y, x = i - 2, j - 2
                D[i, j] = -x * math.sin(th) + y * math.cos(th)   # perpendicular distance to line
        narrow = np.exp(-D**2 / 2.0)
        wide = np.exp(-D**2 / (2 * 2.2**2))
        c = narrow.sum() / wide.sum()            # zero-sum kernel
        w = narrow - c * wide
        R = w[np.abs(D) <= 1.2].sum()
        conv1_w[k, 0] = w / R                    # ideal stroke along band -> ~1
    conv1_b = np.full(8, -0.2)

    # ---------------- conv2 ----------------
    # ch 0-7  : orientation o summed over pool1 taps 1..3 (x1/3)        -> orientation histogram
    # ch 8-11 : emptiness, 3x3 taps shifted by (sy,sx) in {0,1}^2       -> ReLU(1 - ink/3)
    # ch 12-15: emptiness, 2x2 taps at (1+2ay.., 1+2ax..)               -> ReLU(1 - ink/2)
    conv2_w = np.zeros((16, 8, 5, 5))
    conv2_b = np.zeros(16)
    for o in range(8):
        conv2_w[o, o, 1:4, 1:4] = 1.0 / 3.0
    empt_specs = []   # (ty0, ty1, tx0, tx1) inclusive tap ranges for channels 8..15
    for j in range(4):
        sy, sx = j // 2, j % 2
        empt_specs.append((1 + sy, 3 + sy, 1 + sx, 3 + sx))
    for j in range(4):
        ay, ax = j // 2, j % 2
        empt_specs.append((1 + 2 * ay, 2 + 2 * ay, 1 + 2 * ax, 2 + 2 * ax))
    for j, (ty0, ty1, tx0, tx1) in enumerate(empt_specs):
        k = 8 + j
        ntap = ty1 - ty0 + 1
        conv2_w[k, :, ty0:ty1 + 1, tx0:tx1 + 1] = -1.0 / ntap
        conv2_b[k] = 1.0

    # ---------------- hand-drawn digit strokes (x right, y down) ----------------
    def line(p0, p1):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        n = int(L / 0.25) + 2
        return [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
                for t in np.linspace(0, 1, n)]

    def arc(cx, cy, rx, ry, a0, a1):
        n = int(abs(a1 - a0) / 2) + 2
        return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
                for a in np.linspace(a0, a1, n)]

    def poly(pts):
        out = []
        for a, b in zip(pts[:-1], pts[1:]):
            out += line(a, b)
        return out

    digits = {
        0: [[arc(14, 14, 7, 9.5, 0, 360)]],
        1: [[line((15.5, 4.5), (12.5, 23.5))],
            [line((14, 4), (14, 24))],
            [line((18, 4.5), (10, 23.5))]],
        2: [[arc(14, 9.5, 5, 5, 190, 390), line((18.3, 12), (9, 23)), line((9, 23), (20, 23))],
            [arc(14, 9.5, 5, 5, 190, 390), line((18.3, 12), (10, 20.5)),
             arc(10.5, 21.5, 2, 1.8, 200, 520), line((12, 22.5), (20.5, 22.5))]],
        3: [[arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
            [arc(14, 9, 4.5, 4, 190, 440), arc(13.5, 18.5, 5.5, 5, 280, 515)]],
        4: [[line((10.5, 4.5), (8, 15.5)), line((8, 15.5), (20, 15.5)), line((17, 4.5), (16.5, 24))],
            [line((16, 4.5), (7.5, 16)), line((7.5, 16), (20, 16)), line((16, 4.5), (16, 24))]],
        5: [[line((19.5, 5), (11, 5)), line((11, 5), (10.5, 13)),
             line((10.5, 13), (12, 13.8)), arc(14, 18.5, 5, 4.8, 245, 510)],
            [line((20, 5.5), (12.5, 5)), line((12.5, 5), (10.5, 12.5)),
             poly([(10.5, 12.5), (14, 11.8), (17.5, 13), (19.5, 16.5), (18.5, 20.5),
                   (15, 23), (11, 23), (8.5, 21)])]],
        6: [[poly([(17.5, 4.5), (14, 7), (11.5, 10.5), (10, 14.5), (9.5, 19)]),
             arc(14, 19, 4.5, 4.5, 0, 360)]],
        7: [[line((8.5, 6), (20, 6)), line((20, 6), (14, 24))],
            [line((8.5, 6), (19, 6)), line((19, 6), (16.5, 24))]],
        8: [[arc(14, 9.2, 4.3, 4.5, 0, 360), arc(14, 18.5, 5, 5, 0, 360)],
            [arc(15.5, 9, 4, 4.3, 0, 360), arc(12.5, 18.5, 5, 5, 0, 360)]],
        9: [[arc(14.5, 9, 4.5, 4.5, 0, 360), line((19, 9.5), (16, 23.5))],
            [arc(14, 9, 4.5, 4.5, 0, 360), line((18.5, 9.5), (18, 24))]],
    }

    # per-digit slant (x += shear*(14 - y)), part of each drawing
    SHEARS = {0: 0.20, 1: 0.20, 2: 0.12, 3: 0.20, 4: 0.12,
              5: 0.20, 6: 0.12, 7: 0.12, 8: 0.12, 9: 0.20}
    th_arr = np.array(thetas)
    RAMP = 3.0          # spatial blur of orientation (reward) templates (px)
    PRAMP = 1.5         # sharper blur used to decide where a class expects no ink (penalty mask)
    ERAMP = 1.0         # sharp blur for emptiness templates
    OCUT = 0.1

    def soft_win(v, lo, hi, ramp):
        below = np.clip(1 - (lo - v) / ramp, 0, 1)
        above = np.clip(1 - (v - hi) / ramp, 0, 1)
        return np.where(v < lo, below, np.where(v > hi, above, 1.0))

    def segments(strokes, shear):
        X, Y, L, P = [], [], [], []
        for st in strokes:
            st = [(x + shear * (14 - y), y) for (x, y) in st]
            for a, b in zip(st[:-1], st[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                l = math.hypot(dx, dy)
                if l < 1e-9:
                    continue
                X.append((a[0] + b[0]) / 2); Y.append((a[1] + b[1]) / 2)
                L.append(l); P.append(math.atan2(dy, dx) % math.pi)
        X, Y, L, P = map(np.array, (X, Y, L, P))
        X = X - (np.sum(X * L) / np.sum(L) - 14.0)     # MNIST-style centre of mass
        Y = Y - (np.sum(Y * L) / np.sum(L) - 14.0)
        M = np.clip((np.cos(2 * (P[:, None] - th_arr[None, :])) - OCUT) / (1 - OCUT), 0, None)
        return X, Y, L, M

    def orient_v(X, Y, L, M, ty0, ty1, tx0, tx1, ramp):
        WY = np.zeros((len(X), 8)); WX = np.zeros((len(X), 8))
        for r in range(8):
            WY[:, r] = soft_win(Y, 2 * r + 2 * ty0 + 1.5, 2 * r + 2 * ty1 + 3.5, ramp)
            WX[:, r] = soft_win(X, 2 * r + 2 * tx0 + 1.5, 2 * r + 2 * tx1 + 3.5, ramp)
        n = 2.0 * (ty1 - ty0 + 1)
        return np.einsum('n,no,nr,nc->orc', L, M, WY, WX) / n          # (8,8,8)

    def pool(v):  # (...,8,8) -> (...,4,4) max pool
        sh = v.shape[:-2]
        return v.reshape(sh + (4, 2, 4, 2)).max(axis=(-3, -1))

    def template(strokes, shear):
        X, Y, L, M = segments(strokes, shear)
        ori = pool(orient_v(X, Y, L, M, 1, 3, 1, 3, RAMP)).reshape(128)
        ori_sharp = pool(orient_v(X, Y, L, M, 1, 3, 1, 3, PRAMP)).reshape(128)
        emp = []
        for (ty0, ty1, tx0, tx1) in empt_specs:
            v = orient_v(X, Y, L, M, ty0, ty1, tx0, tx1, ERAMP)
            ink = 0.5 * v.sum(axis=0)
            emp.append(pool(np.clip(1 - ink, 0, 1)))
        return ori, ori_sharp, np.stack(emp).reshape(128)

    O = np.zeros((10, 128)); OS = np.zeros((10, 128)); E = np.zeros((10, 128))
    for d in range(10):
        parts = [template(var, SHEARS[d]) for var in digits[d]]
        O[d] = sum(p[0] for p in parts)                       # overlay of variants
        OS[d] = sum(p[1] for p in parts)                      # sharp overlay (penalty mask)
        E[d] = sum(p[2] for p in parts) / len(parts)          # expected emptiness

    # ---------------- fc ----------------
    Ohat = O / np.linalg.norm(O, axis=1, keepdims=True)
    U = Ohat.mean(axis=0)
    reward_generic = (Ohat @ U).mean()
    LAMBDA = 0.5
    kappa = 3.0
    ETA = 0.15
    Ebar = E.mean(axis=0)
    fc_w = np.zeros((10, 256))
    fc_b = np.array([0.1, 0.35, 0.15, -0.38, 1.0, -0.85, 0.0, 1.25, -0.4, 0.2])
    for d in range(10):
        empty = np.clip(1 - OS[d] / (0.25 * OS[d].max()), 0, 1)   # sharp "no ink expected" mask
        P = U * empty
        P = P * (LAMBDA * reward_generic / (P @ U + 1e-9))
        fc_w[d, :128] = kappa * (Ohat[d] - P)                 # orientation evidence
        fc_w[d, 128:] = ETA * E[d]                            # reward for expected-empty regions
        fc_b[d] -= ETA * (E[d] @ Ebar)                        # remove sparse-template head start

    return {
        'conv1.weight': conv1_w.astype(np.float32),
        'conv1.bias': conv1_b.astype(np.float32),
        'conv2.weight': conv2_w.astype(np.float32),
        'conv2.bias': conv2_b.astype(np.float32),
        'fc.weight': fc_w.astype(np.float32),
        'fc.bias': fc_b.astype(np.float32),
    }
