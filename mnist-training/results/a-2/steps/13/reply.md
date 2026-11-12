## Step 13: keep the slant only on the digits it helped, and revert the probability cap

**What I'm trying.** Step 12 changed two things at once, a global slant and a cap of 0.82 on presence probabilities. The results split clearly by digit:

| Digit | Correct, step 11 | Correct, step 12 | Main new error |
|---|---|---|---|
| 0 | 711 | 815 | 0→2 fell 217→111 |
| 4 | 774 | 858 | — |
| 8 | 511 | 660 | — |
| 6 | 612 | 363 | 6→4 rose to 349 |
| 2 | 582 | 462 | 2→8 rose to 286 |
| 3 | 669 | 559 | 3→5 rose to 299 |
| 7 | 877 | 790 | 7→9 rose to 184 |

The pattern fits the slant. Leaning 0, 4 and 8 matches how they are written. Leaning 6, 2, 3, 7 and 9 made them overlap other classes; a leaning 6, for instance, starts to resemble the leaning 4.

So in this step:

- the slant (shear 0.15) is applied only to 0, 4 and 8;
- all other digits use their upright drawings, with 1 still using its own slanted strokes;
- the presence-probability cap goes back to 0.92, so the slant's effect can be judged on its own.

Everything else is unchanged from step 12.

```python
import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')   # V = row offset (down), U = col offset (right)
    HOR, DIAG1, VER, DIAG2 = 0, 1, 2, 3

    # ================= conv1: 4 orientation detectors, each as a clipping pair =================
    W1 = np.zeros((8, 1, 5, 5)); b1 = np.zeros(8)
    g1 = 3.0
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)
        perp = -U * math.sin(th) + V * math.cos(th)
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = g1 * K;     b1[k] = -0.6        # relu(3x - 0.6)
        W1[k + 4, 0] = g1 * K; b1[k + 4] = -1.6    # difference -> O_k = clip(3x-0.6, 0, 1)

    # ================= conv2: 8 clipped features (pairs of channels) =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)

    def set_pair(m, Z, g, t):
        """feature m = clip(g*(Z.O - t), 0, 1), O_k = pool1[k] - pool1[k+4]"""
        for k in range(4):
            W2[2 * m, k] = g * Z[k];      W2[2 * m, k + 4] = -g * Z[k]
            W2[2 * m + 1, k] = g * Z[k];  W2[2 * m + 1, k + 4] = -g * Z[k]
        b2[2 * m] = -g * t
        b2[2 * m + 1] = -g * t - 1.0

    # m = 0..3: orientation presence in 3x3 pooled neighbourhood
    nb = np.zeros((5, 5))
    nb[1:4, 1:4] = [[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]]
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k] = nb
        set_pair(k, Z, 1.0, 0.6)

    # strict shape detectors from single side cells at radius 2 pooled cells (~4 px)
    def side(Z, name, w):
        if name == 'top':    Z[HOR, 0, 2] += w
        if name == 'bottom': Z[HOR, 4, 2] += w
        if name == 'left':   Z[VER, 2, 0] += w
        if name == 'right':  Z[VER, 2, 4] += w

    def centre_pen(Z, w=0.5):
        for k in range(4):
            Z[k, 2, 2] -= w

    Z = np.zeros((4, 5, 5))
    for s_ in ['top', 'bottom', 'left', 'right']:
        side(Z, s_, 1.0)
    centre_pen(Z)
    set_pair(4, Z, 2.5, 3.0)                                   # m=4 closed loop

    def arc3(present, absent_cells):
        Z = np.zeros((4, 5, 5))
        for s_ in present:
            side(Z, s_, 1.0)
        k, cells = absent_cells
        for (a, b) in cells:
            Z[k, a, b] -= 1.2
        centre_pen(Z)
        return Z

    set_pair(5, arc3(['top', 'right', 'bottom'], (VER, [(2, 0), (2, 1)])), 2.5, 2.2)   # ⊃ open left
    set_pair(6, arc3(['top', 'left', 'right'], (HOR, [(4, 2), (3, 2)])), 2.5, 2.2)     # ∩ open bottom
    set_pair(7, arc3(['bottom', 'left', 'right'], (HOR, [(0, 2), (1, 2)])), 2.5, 2.2)  # ∪ open top

    # ================= stroke descriptions (x=col, y=row) =================
    def seg(p0, p1, w=1.0):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(L / 0.5))
        t = (np.arange(n) + 0.5) / n
        return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t,
                np.full(n, math.atan2(y1 - y0, x1 - x0)), np.full(n, w * L / n))

    def arc(cx, cy, rx, ry, t0, t1, w=1.0):
        t0r, t1r = math.radians(t0), math.radians(t1)
        n = max(8, int(abs(t1 - t0) / 3))
        t = t0r + (t1r - t0r) * (np.arange(n) + 0.5) / n
        dt = abs(t1r - t0r) / n
        dx = -rx * np.sin(t); dy = ry * np.cos(t)
        return (cx + rx * np.cos(t), cy + ry * np.sin(t),
                np.arctan2(dy, dx), w * np.hypot(dx, dy) * dt)

    def slant(stroke, sh):
        """shear the drawing: x' = x + sh*(14 - y)  (top leans right)."""
        x, y, a, ds = stroke
        dx = np.cos(a); dy = np.sin(a)
        dx2 = dx - sh * dy
        a2 = np.arctan2(dy, dx2)
        ds2 = ds * np.hypot(dx2, dy)
        return (x + sh * (14 - y), y, a2, ds2)

    digits = {
        0: [arc(14, 14, 5.5, 8.5, 0, 360)],
        1: [seg((15, 4.5), (13, 23.5), 0.6), seg((17.5, 5), (10.5, 23), 0.6)],
        2: [arc(14, 10, 5, 5, 180, 390), seg((18.3, 12.5), (9, 22.5)), seg((9, 22.5), (20, 22.5))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [seg((10, 4.5), (8, 16)), seg((8, 16), (20, 16)), seg((17, 5), (17, 23.5))],
        5: [seg((10, 5), (19, 5)), seg((10, 5), (9.5, 13)), arc(13.5, 17.5, 5.5, 5, 228, 510)],
        6: [seg((17, 4.5), (10.5, 12)), seg((10.5, 12), (8.5, 18)), arc(13.5, 18, 5, 4.5, 0, 360)],
        7: [seg((8, 6), (20, 6)), seg((20, 6), (12, 24), 0.6), seg((19.5, 6), (15, 24), 0.6)],
        8: [arc(14, 9, 4, 4.5, 0, 360), arc(14, 18.5, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 4.5, 0, 360), seg((19, 10), (16, 23.5))],
    }
    SH = 0.15
    for d in (0, 4, 8):          # slant only where it helped in step 12
        digits[d] = [slant(s_, SH) for s_ in digits[d]]

    LOOP, OL, OB, OT = 4, 5, 6, 7
    parts = {
        0: [(LOOP, 14, 14, 0.3), (OB, 14, 9.5, 0.45), (OT, 14, 18.5, 0.45)],
        1: [],
        2: [(OL, 14, 10, 0.35), (OB, 14, 9.5, 0.3)],
        3: [(OL, 13, 9, 0.5), (OL, 13, 18.5, 0.55)],
        4: [(OT, 13, 11, 0.45)],
        5: [(OL, 13.5, 17.5, 0.45)],
        6: [(LOOP, 13.5, 18, 0.5)],
        7: [(OL, 16, 8, 0.15)],
        8: [(LOOP, 14, 9, 0.45), (LOOP, 14, 18.5, 0.45)],
        9: [(LOOP, 14, 9.5, 0.5), (OB, 14, 9.5, 0.2)],
    }

    centers = [4 * i + 7.5 for i in range(4)]
    base = 0.08
    pmax = 0.92
    Pr = np.full((10, 8, 4, 4), base)
    Pr[:, 4:] = 0.05

    sig = 2.5
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes]); y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes]); ds = np.concatenate([s[3] for s in strokes])
        for r in range(4):
            for c in range(4):
                prox = np.exp(-((x - centers[c])**2 + (y - centers[r])**2) / (2 * sig**2)) * ds
                for k, th in enumerate(thetas):
                    raw = np.sum(prox * np.cos(a - th)**4)
                    Pr[d, k, r, c] = base + (pmax - base) * (1 - math.exp(-raw / 1.5))

    for d, plist in parts.items():
        for (m, px, py, pk) in plist:
            for r in range(4):
                for c in range(4):
                    v = 0.05 + (pk - 0.05) * math.exp(-((px - centers[c])**2 + (py - centers[r])**2) / (2 * 2.5**2))
                    Pr[d, m, r, c] = max(Pr[d, m, r, c], v)

    # ================= fc: naive Bayes on clipped features =================
    lam_feat = np.full(8, 0.3)
    L = np.log(Pr / (1 - Pr))
    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    for m in range(8):
        Wfc[:, 2 * m] = lam_feat[m] * L[:, m]
        Wfc[:, 2 * m + 1] = -lam_feat[m] * L[:, m]
        bfc += lam_feat[m] * np.sum(np.log(1 - Pr[:, m]).reshape(10, -1), axis=1)
    Wfc = Wfc.reshape(10, 256)

    # cumulative prior corrections (steps 7, 8, 9)
    true_cnt = np.array([991, 1064, 990, 1030, 973, 915, 967, 1090, 1009, 961], dtype=np.float64)
    pred7 = np.array([935, 1343, 1228, 765, 793, 822, 1260, 513, 1055, 1286], dtype=np.float64)
    pred8 = np.array([987, 1334, 1068, 880, 907, 874, 1131, 855, 1019, 945], dtype=np.float64)
    pred9 = np.array([961, 1307, 1012, 966, 928, 907, 1025, 957, 1018, 919], dtype=np.float64)
    bfc = bfc - np.log(pred7 / true_cnt) - np.log(pred8 / true_cnt) - np.log(pred9 / true_cnt)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
