## Step 21: drop the endpoints and add top- and bottom-shifted horizontal features

**What the probe showed.** The endpoint detectors are not selective, and there is a geometric reason.

- **1s produce no endpoint activity at all**: 949 of 1,064 fell in the low/low bin.
- **4, 5, 6, 9 and 3s mostly land in "high/high"**: the detectors fire on loop bottoms, corners and thick-stroke edges.

The reason is the conv2 geometry. A conv2 kernel's centre can only sit over pooled cells 2–9, which is input rows and columns **6.5–20.5**. True stroke ends, such as the tops and bottoms of 1, 4, 7 and 9 at rows ≈4–5 and ≈23–24, lie *outside* that range. So a centred endpoint detector can never see them.

**The same geometry hurts the horizontal features.** The top bars of 5 and 7 (row ≈5–6) and the bottom bar of 2 (row ≈22.5) fall at the very edge of the outer row of the presence features. They are only weakly detected, even though they are among the most distinctive strokes.

**Changes.**

1. Back to the step 16/17 model, keeping λ = 0.3 and step 17's 2 template. The endpoint detectors are removed.
2. Two new clipped features, replacing the two corner detectors:
   - **m = 4, H-up**: horizontal presence with the 3×3 neighbourhood placed one pooled row *above* the kernel centre. Its cell centres are input rows 5.5, 9.5, 13.5 and 17.5, so it catches top bars.
   - **m = 5, H-down**: the same, one pooled row *below*. Its cell centres are rows 9.5, 13.5, 17.5 and 21.5, so it catches bottom bars.
   - Their templates are computed from the strokes with the correspondingly shifted cell centres.
3. The strict loop (m = 6) and small loop (m = 7) are unchanged clipped pairs, with the calibrated templates from step 16.

```python
import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')   # V = row offset (down), U = col offset (right)
    HOR, D1, VER, D2 = 0, 1, 2, 3                 # D1 = "\", D2 = "/"

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

    nb3 = np.array([[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]])

    # m = 0..3: orientation presence, 3x3 neighbourhood centred in the kernel
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k, 1:4, 1:4] = nb3
        set_pair(k, Z, 1.0, 0.6)
    # m = 4: horizontal presence shifted one pooled row UP (rows 0..2 of the kernel)
    Z = np.zeros((4, 5, 5)); Z[HOR, 0:3, 1:4] = nb3
    set_pair(4, Z, 1.0, 0.6)
    # m = 5: horizontal presence shifted one pooled row DOWN (rows 2..4 of the kernel)
    Z = np.zeros((4, 5, 5)); Z[HOR, 2:5, 1:4] = nb3
    set_pair(5, Z, 1.0, 0.6)

    # m = 6: strict loop (four straight sides at radius 2 cells, empty centre)
    Z = np.zeros((4, 5, 5))
    Z[HOR, 0, 2] = 1; Z[HOR, 4, 2] = 1; Z[VER, 2, 0] = 1; Z[VER, 2, 4] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_pair(6, Z, 2.5, 3.0)

    # m = 7: small loop from inner diagonal cells, empty centre
    Z = np.zeros((4, 5, 5))
    Z[D2, 1, 1] = 1; Z[D1, 1, 3] = 1; Z[D1, 3, 1] = 1; Z[D2, 3, 3] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_pair(7, Z, 2.5, 3.0)

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
        x, y, a, ds = stroke
        dx = np.cos(a); dy = np.sin(a)
        dx2 = dx - sh * dy
        return (x + sh * (14 - y), y, np.arctan2(dy, dx2), ds * np.hypot(dx2, dy))

    digits = {
        0: [arc(14, 14, 5.5, 8.5, 0, 360)],
        1: [seg((15, 4.5), (13, 23.5), 0.6), seg((17.5, 5), (10.5, 23), 0.6)],
        2: [arc(14, 10, 5, 5, 180, 390), seg((18.3, 12.5), (8.5, 22.5)), seg((8.5, 22.5), (20.5, 22.5), 1.3)],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [seg((10, 4.5), (8, 16)), seg((8, 16), (20, 16)), seg((17, 5), (17, 23.5))],
        5: [seg((10, 5), (19, 5)), seg((10, 5), (9.5, 13)), arc(13.5, 17.5, 5.5, 5, 228, 510)],
        6: [seg((17, 4.5), (10.5, 12)), seg((10.5, 12), (8.5, 18)), arc(13.5, 18, 5, 4.5, 0, 360)],
        7: [seg((8, 6), (20, 6)), seg((20, 6), (12, 24), 0.6), seg((19.5, 6), (15, 24), 0.6)],
        8: [arc(14, 9, 4, 4.5, 0, 360), arc(14, 18.5, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 4.5, 0, 360), seg((19, 10), (16, 23.5))],
    }
    for d in (0, 8):
        digits[d] = [slant(s_, 0.15) for s_ in digits[d]]

    LOOP, SLOOP = 6, 7
    parts = {
        0: [(SLOOP, 14, 14, 0.12)],
        1: [],
        2: [(SLOOP, 10, 21, 0.08)],
        3: [(LOOP, 13.5, 9, 0.06)],
        4: [(LOOP, 13, 10, 0.07)],
        5: [(LOOP, 13.5, 18, 0.05)],
        6: [(LOOP, 13.5, 18, 0.3), (SLOOP, 13.5, 18, 0.3)],
        7: [],
        8: [(LOOP, 14, 9, 0.25), (LOOP, 14, 18.5, 0.25), (SLOOP, 14, 9, 0.3), (SLOOP, 14, 18.5, 0.3)],
        9: [(LOOP, 14, 9.5, 0.4), (SLOOP, 14, 9.5, 0.35)],
    }

    centers = np.array([4 * i + 7.5 for i in range(4)])
    base = 0.08
    pmax = 0.92
    pbase_part = 0.02
    Pr = np.full((10, 8, 4, 4), base)
    Pr[:, 6:] = pbase_part

    sig = 2.5
    # (feature m, orientation k, row-centre offset in px)
    or_feats = [(0, 0, 0.0), (1, 1, 0.0), (2, 2, 0.0), (3, 3, 0.0), (4, 0, -2.0), (5, 0, 2.0)]
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes]); y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes]); ds = np.concatenate([s[3] for s in strokes])
        for (m, k, dy) in or_feats:
            tune = np.cos(a - thetas[k])**4
            for r in range(4):
                for c in range(4):
                    prox = np.exp(-((x - centers[c])**2 + (y - (centers[r] + dy))**2) / (2 * sig**2)) * ds
                    raw = np.sum(prox * tune)
                    Pr[d, m, r, c] = base + (pmax - base) * (1 - math.exp(-raw / 1.5))

    for d, plist in parts.items():
        for (m, px, py, pk) in plist:
            for r in range(4):
                for c in range(4):
                    v = pbase_part + (pk - pbase_part) * math.exp(-((px - centers[c])**2 + (py - centers[r])**2) / (2 * 2.5**2))
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

    # cumulative prior corrections (as step 16)
    true_cnt = np.array([991, 1064, 990, 1030, 973, 915, 967, 1090, 1009, 961], dtype=np.float64)
    pred7 = np.array([935, 1343, 1228, 765, 793, 822, 1260, 513, 1055, 1286], dtype=np.float64)
    pred8 = np.array([987, 1334, 1068, 880, 907, 874, 1131, 855, 1019, 945], dtype=np.float64)
    pred9 = np.array([961, 1307, 1012, 966, 928, 907, 1025, 957, 1018, 919], dtype=np.float64)
    pred13 = np.array([1112, 1276, 745, 865, 1134, 1123, 746, 1130, 1068, 801], dtype=np.float64)
    bfc = (bfc - np.log(pred7 / true_cnt) - np.log(pred8 / true_cnt) - np.log(pred9 / true_cnt)
           - 0.7 * np.log(pred13 / true_cnt))

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
