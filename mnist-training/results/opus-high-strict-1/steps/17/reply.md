## Step 17: strengthen the empty-region evidence and re-balance biases

**What step 16 showed.** The empty-region features helped: accuracy rose to 76.2% and loss fell to 0.86.
- 1 went from 940 to 1000 correct, 4 from 701 to 789, 7 from 851 to 944, 0 from 804 to 851, and 9 from 713 to 759.
- 3 dropped from 774 to 671, losing mainly to 5 (162).
- 5 → 8 (223) is still the largest error.

**Changes in this step.**
1. **η raised from 0.15 to 0.25.** At 0.15 the empty-region evidence clearly helped, so I am giving it more weight. The per-class offset −η · (E_d · Ē) is still applied, so sparse templates gain no automatic head start.
2. **Bias corrections from step 16's column totals.**

| Class | Status | Bias change |
|---|---|---|
| 3 | under-predicted by 215 | +0.25 |
| 5 | under-predicted | +0.1 |
| 2 | under-predicted | +0.1 |
| 0 | over-predicted | −0.1 |
| 6 | over-predicted | −0.1 |
| 7 | over-predicted | −0.1 |
| 9 | over-predicted | −0.1 |

Classes 1, 4 and 8 keep their biases.

```python
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
        3: [[arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)]],
        4: [[line((10.5, 4.5), (8, 15.5)), line((8, 15.5), (20, 15.5)), line((17, 4.5), (16.5, 24))],
            [line((16, 4.5), (7.5, 16)), line((7.5, 16), (20, 16)), line((16, 4.5), (16, 24))]],
        5: [[line((19.5, 5), (11, 5)), line((11, 5), (10.5, 13)),
             line((10.5, 13), (12, 13.8)), arc(14, 18.5, 5, 4.8, 245, 510)]],
        6: [[poly([(17.5, 4.5), (14, 7), (11.5, 10.5), (10, 14.5), (9.5, 19)]),
             arc(14, 19, 4.5, 4.5, 0, 360)]],
        7: [[line((8.5, 6), (20, 6)), line((20, 6), (14, 24))],
            [line((8.5, 6), (19, 6)), line((19, 6), (16.5, 24))]],
        8: [[arc(14, 9.2, 4.3, 4.5, 0, 360), arc(14, 18.5, 5, 5, 0, 360)],
            [arc(15.5, 9, 4, 4.3, 0, 360), arc(12.5, 18.5, 5, 5, 0, 360)]],
        9: [[arc(14.5, 9, 4.5, 4.5, 0, 360), line((19, 9.5), (16, 23.5))],
            [arc(14, 9, 4.5, 4.5, 0, 360), line((18.5, 9.5), (18, 24))]],
    }

    SHEAR = 0.12
    th_arr = np.array(thetas)
    RAMP = 3.0          # spatial blur of orientation templates (px)
    ERAMP = 1.0         # sharper blur for emptiness templates
    OCUT = 0.1

    def soft_win(v, lo, hi, ramp):
        below = np.clip(1 - (lo - v) / ramp, 0, 1)
        above = np.clip(1 - (v - hi) / ramp, 0, 1)
        return np.where(v < lo, below, np.where(v > hi, above, 1.0))

    def segments(strokes):
        X, Y, L, P = [], [], [], []
        for st in strokes:
            st = [(x + SHEAR * (14 - y), y) for (x, y) in st]
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

    def template(strokes):
        X, Y, L, M = segments(strokes)
        ori = pool(orient_v(X, Y, L, M, 1, 3, 1, 3, RAMP)).reshape(128)
        emp = []
        for (ty0, ty1, tx0, tx1) in empt_specs:
            v = orient_v(X, Y, L, M, ty0, ty1, tx0, tx1, ERAMP)
            ink = 0.5 * v.sum(axis=0)
            emp.append(pool(np.clip(1 - ink, 0, 1)))
        return ori, np.stack(emp).reshape(128)

    O = np.zeros((10, 128)); E = np.zeros((10, 128))
    for d in range(10):
        parts = [template(var) for var in digits[d]]
        O[d] = sum(p[0] for p in parts)                       # overlay of variants
        E[d] = sum(p[1] for p in parts) / len(parts)          # expected emptiness

    # ---------------- fc ----------------
    Ohat = O / np.linalg.norm(O, axis=1, keepdims=True)
    U = Ohat.mean(axis=0)
    reward_generic = (Ohat @ U).mean()
    LAMBDA = 0.5
    kappa = 3.0
    ETA = 0.25
    Ebar = E.mean(axis=0)
    fc_w = np.zeros((10, 256))
    fc_b = np.array([0.15, 0.35, 0.05, -0.7, 1.05, -0.8, 0.05, 1.25, -0.55, 0.25])
    for d in range(10):
        empty = np.clip(1 - O[d] / (0.25 * O[d].max()), 0, 1)
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
```
