## Step 5: give every class the same expected penalty

**What step 4 showed.** The unexpected-ink penalty helped 0 and 1, but it badly favoured 8. The 8 template expects ink almost everywhere, so its "empty" area is tiny and it was barely penalised. Sparse templates such as 7, 9, 2 and 6 were penalised heavily, even for small amounts of extra ink from thick strokes.

**Fix: normalise each class's penalty.**
- Each penalty vector P_d = U · e_d is rescaled so that U · P_d is the same for every class.
- In other words, an image with generic ink spread in the usual places costs every class the same amount.
- Each penalty therefore lands on that class's own empty regions, with equal total strength. For 8 that is a few strongly weighted spots; for 7 it is many lightly weighted ones.
- The penalty strength is set to half the average generic reward, so its expected effect is fixed and does not grow or shrink with how much ink a class's drawing has.

The step-4 template changes stay: the slant, the wider 0 and the slanted 9 stem.

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

    # ---------------- conv2: orientation sums over 3x3 pool1 cells ----------------
    conv2_w = np.zeros((16, 8, 5, 5))
    for k in range(16):
        o = k % 8
        s = 0 if k < 8 else 1                    # s=1: window shifted 2 input px down-right
        for ty in range(1 + s, 4 + s):
            for tx in range(1 + s, 4 + s):
                conv2_w[k, o, ty, tx] = 1.0 / 3.0
    conv2_b = np.zeros(16)

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
        0: [arc(14, 14, 7, 9.5, 0, 360)],
        1: [line((15.5, 4.5), (12.5, 23.5))],
        2: [arc(14, 9.5, 5, 5, 190, 390), line((18.3, 12), (9, 23)), line((9, 23), (20, 23))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [line((10.5, 4.5), (8, 15.5)), line((8, 15.5), (20, 15.5)), line((17, 4.5), (16.5, 24))],
        5: [line((19, 4.5), (10.5, 4.5)), line((10.5, 4.5), (10, 12.5)),
            line((10, 12.5), (11, 13.7)), arc(13.5, 18, 5, 5, 240, 510)],
        6: [poly([(17.5, 4.5), (14, 6.5), (11, 10), (9.5, 14), (9, 18)]),
            arc(13.5, 18.5, 4.8, 4.8, 0, 360)],
        7: [line((8.5, 5.5), (20, 5.5)), line((20, 5.5), (14, 24))],
        8: [arc(14, 9.2, 4.3, 4.5, 0, 360), arc(14, 18.5, 5, 5, 0, 360)],
        9: [arc(14.5, 9, 4.5, 4.5, 0, 360), line((19, 9.5), (16, 23.5))],
    }

    SHEAR = 0.12   # right-leaning slant: x += SHEAR*(14 - y)

    th_arr = np.array(thetas)
    RAMP = 2.5          # spatial blur of templates (px)
    OCUT = 0.1          # orientation tuning cutoff

    def soft_win(v, lo, hi):
        below = np.clip(1 - (lo - v) / RAMP, 0, 1)
        above = np.clip(1 - (v - hi) / RAMP, 0, 1)
        return np.where(v < lo, below, np.where(v > hi, above, 1.0))

    def template(strokes):
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
        M = np.clip((np.cos(2 * (P[:, None] - th_arr[None, :])) - OCUT) / (1 - OCUT), 0, None)
        WY = np.zeros((len(X), 2, 8)); WX = np.zeros((len(X), 2, 8))
        for s in range(2):
            for r in range(8):
                lo, hi = 2 * r + 3.5 + 2 * s, 2 * r + 9.5 + 2 * s
                WY[:, s, r] = soft_win(Y, lo, hi)
                WX[:, s, r] = soft_win(X, lo, hi)
        v = np.einsum('n,no,ngr,ngc->gorc', L, M, WY, WX) / 6.0
        v = v.reshape(16, 8, 8)
        t = v.reshape(16, 4, 2, 4, 2).max(axis=(2, 4))
        return t.reshape(256)

    # ---------------- fc: cosine match minus normalised "unexpected ink" penalty ----------------
    T = np.stack([template(digits[d]) for d in range(10)])        # (10,256)
    That = T / np.linalg.norm(T, axis=1, keepdims=True)           # unit templates
    U = That.mean(axis=0)                                         # generic ink distribution
    reward_generic = (That @ U).mean()                            # typical reward for generic ink
    LAMBDA = 0.5
    kappa = 3.0
    fc_w = np.zeros((10, 256)); fc_b = np.zeros(10)
    for d in range(10):
        empty = np.clip(1 - T[d] / (0.25 * T[d].max()), 0, 1)     # 1 where class d expects nothing
        P = U * empty
        P = P * (LAMBDA * reward_generic / (P @ U + 1e-9))        # equal expected penalty per class
        fc_w[d] = kappa * (That[d] - P)

    return {
        'conv1.weight': conv1_w.astype(np.float32),
        'conv1.bias': conv1_b.astype(np.float32),
        'conv2.weight': conv2_w.astype(np.float32),
        'conv2.bias': conv2_b.astype(np.float32),
        'fc.weight': fc_w.astype(np.float32),
        'fc.bias': fc_b.astype(np.float32),
    }
```
