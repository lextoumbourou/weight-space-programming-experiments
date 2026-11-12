## Step 19: revert the stricter threshold and add stroke-endpoint detectors

**What I'm trying.** Raising the orientation presence threshold in step 18 hurt badly: accuracy fell to 66.9%. The sparser features no longer matched the templates; 8 collapsed and 1 and 7 absorbed many digits. I'm reverting the threshold to 0.6.

**Endpoint detectors.** Going through the main remaining confusions, almost every one can be separated by *where the strokes end*:

| Confusion | Endpoint cue |
|---|---|
| 6→0, 9→0 | 6 has a top end and 9 a bottom end; 0 has none |
| 2→3 | only 2 ends at the bottom right |
| 3↔5 | 3 ends on the left at top and bottom; 5 ends at the top right |
| 4→9 | 4 has two top ends; 9 has none |
| 7↔9 | 7's top bar starts with a free left end |
| 2/3/5 → 8 | 8 has no ends at all |

So I'm adding four endpoint detectors in conv2. Let ink(cell) be the sum of the four clipped orientation maps at that cell. Each detector requires:

- ink at the kernel centre;
- ink continuing in one direction;
- no ink on the opposite side or the lateral sides.

| Feature | Fires at | Examples |
|---|---|---|
| E_down | top endpoints (stroke continues downward) | top of a 1, the two tops of a 4, top of a 6's stem |
| E_up | bottom endpoints | bottom of a 1, 4, 7 or 9 |
| E_right | left endpoints | start of a 7's bar; the left ends of a 3 or a 5's belly |
| E_left | right endpoints | end of a 2's bottom bar; end of a 5's top bar |

**Channel budget.**

- The 4 orientation presence features stay as clipped pairs (conv2 channels 0–7).
- The part features become single ReLU channels, scaled so that a clear detection is about 1:
  - 8 = strict loop;
  - 9 = small loop;
  - 10–13 = the four endpoint detectors.
- The two corner detectors are dropped to make room.

The part templates list the hand-identified endpoint locations for each digit.

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

    # ================= conv2 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)

    def put(ch, Z, g):
        """write g*Z (4,5,5 weights on O_k) into conv2 channel ch, via O_k = pool[k]-pool[k+4]"""
        for k in range(4):
            W2[ch, k] += g * Z[k]
            W2[ch, k + 4] -= g * Z[k]

    def set_pair(m, Z, g, t):
        """clipped feature: channels 2m, 2m+1 ; fc uses ch(2m) - ch(2m+1) = clip(g(z-t),0,1)"""
        put(2 * m, Z, g);     b2[2 * m] = -g * t
        put(2 * m + 1, Z, g); b2[2 * m + 1] = -g * t - 1.0

    def set_single(ch, Z, g, t):
        """single ReLU feature: relu(g(z - t))"""
        put(ch, Z, g); b2[ch] = -g * t

    # channels 0-7: orientation presence (clipped pairs), threshold back to 0.6
    nb = np.zeros((5, 5))
    nb[1:4, 1:4] = [[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]]
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k] = nb
        set_pair(k, Z, 1.0, 0.6)

    # channel 8: strict loop (four straight sides at radius 2 cells, empty centre)
    Z = np.zeros((4, 5, 5))
    Z[HOR, 0, 2] = 1; Z[HOR, 4, 2] = 1; Z[VER, 2, 0] = 1; Z[VER, 2, 4] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_single(8, Z, 2.0, 3.0)

    # channel 9: small loop from inner diagonal cells, empty centre
    Z = np.zeros((4, 5, 5))
    Z[D2, 1, 1] = 1; Z[D1, 1, 3] = 1; Z[D1, 3, 1] = 1; Z[D2, 3, 3] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_single(9, Z, 2.0, 3.0)

    # channels 10-13: endpoint detectors on "ink" = sum over orientations
    Edown = np.zeros((5, 5))          # endpoint at centre, stroke continues downward
    Edown[2, 2] = 0.4; Edown[3, 2] = 0.4; Edown[3, 1] = 0.2; Edown[3, 3] = 0.2; Edown[4, 2] = 0.2
    Edown[1, 1] = -0.6; Edown[1, 2] = -0.6; Edown[1, 3] = -0.6; Edown[0, 2] = -0.2
    Edown[2, 1] = -0.3; Edown[2, 3] = -0.3
    Eup = np.flipud(Edown)            # stroke continues upward (bottom endpoint)
    Eright = Edown.T.copy()           # stroke continues to the right (left endpoint)
    Eleft = np.fliplr(Eright)         # stroke continues to the left (right endpoint)
    for ch, Emap in zip([10, 11, 12, 13], [Edown, Eup, Eright, Eleft]):
        Z = np.stack([Emap] * 4)      # same weight on every orientation = ink
        set_single(ch, Z, 1.5, 1.1)
    # channels 14, 15 unused

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

    # part features: index into the 16-channel map, (x, y, peak probability)
    LOOP, SLOOP, EDN, EUP, ERT, ELT = 8, 9, 10, 11, 12, 13
    parts = {
        0: [(SLOOP, 14, 14, 0.12)],
        1: [(EDN, 15, 5, 0.6), (EUP, 13, 23, 0.6)],
        2: [(SLOOP, 10, 21, 0.08), (ELT, 20.5, 22.5, 0.45), (EUP, 9, 10, 0.2), (ERT, 9, 9.5, 0.2)],
        3: [(LOOP, 13.5, 9, 0.06), (ERT, 9.5, 7.5, 0.3), (ERT, 9, 20, 0.35), (EUP, 9.5, 8, 0.15)],
        4: [(LOOP, 13, 10, 0.07), (EDN, 10, 5, 0.5), (EDN, 17, 5.5, 0.5), (EUP, 17, 23, 0.5), (ELT, 20, 16, 0.25)],
        5: [(LOOP, 13.5, 18, 0.05), (ELT, 19, 5, 0.5), (ERT, 9, 20, 0.35)],
        6: [(LOOP, 13.5, 18, 0.3), (SLOOP, 13.5, 18, 0.3), (EDN, 16.5, 5, 0.5)],
        7: [(ERT, 8, 6, 0.5), (EUP, 13.5, 23.5, 0.5)],
        8: [(LOOP, 14, 9, 0.25), (LOOP, 14, 18.5, 0.25), (SLOOP, 14, 9, 0.3), (SLOOP, 14, 18.5, 0.3)],
        9: [(LOOP, 14, 9.5, 0.4), (SLOOP, 14, 9.5, 0.35), (EUP, 16, 23, 0.55)],
    }

    centers = [4 * i + 7.5 for i in range(4)]
    base = 0.08
    pmax = 0.92
    Pr_or = np.full((10, 4, 4, 4), base)          # orientation features
    Pr_pt = np.full((10, 16, 4, 4), 0.03)         # part features (indexed by channel)
    Pr_pt[:, 8:10] = 0.02

    sig = 2.5
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes]); y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes]); ds = np.concatenate([s[3] for s in strokes])
        for r in range(4):
            for c in range(4):
                prox = np.exp(-((x - centers[c])**2 + (y - centers[r])**2) / (2 * sig**2)) * ds
                for k, th in enumerate(thetas):
                    raw = np.sum(prox * np.cos(a - th)**4)
                    Pr_or[d, k, r, c] = base + (pmax - base) * (1 - math.exp(-raw / 1.5))

    for d, plist in parts.items():
        for (ch, px, py, pk) in plist:
            for r in range(4):
                for c in range(4):
                    b0 = Pr_pt[d, ch, r, c]
                    v = 0.03 + (pk - 0.03) * math.exp(-((px - centers[c])**2 + (py - centers[r])**2) / (2 * 2.5**2))
                    Pr_pt[d, ch, r, c] = max(b0, v)

    # ================= fc: naive Bayes =================
    lam = 0.3
    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    Lor = np.log(Pr_or / (1 - Pr_or))
    for k in range(4):                        # clipped orientation pairs
        Wfc[:, 2 * k] = lam * Lor[:, k]
        Wfc[:, 2 * k + 1] = -lam * Lor[:, k]
    bfc += lam * np.sum(np.log(1 - Pr_or).reshape(10, -1), axis=1)
    for ch in range(8, 14):                   # single-channel part features
        Lp = np.log(Pr_pt[:, ch] / (1 - Pr_pt[:, ch]))
        Wfc[:, ch] = lam * Lp
        bfc += lam * np.sum(np.log(1 - Pr_pt[:, ch]).reshape(10, -1), axis=1)
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
