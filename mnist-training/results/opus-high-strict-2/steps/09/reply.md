# Step 9: add loop ("hole") detectors, and keep only the anti-strokes that helped

**What I learned from step 8.**

- **Anti-strokes were mixed.** They helped 4, 5 and 6, but badly hurt 3, 7, 9 and 0. Because 8 had no anti-strokes while every other digit was penalised, 8 became a sink with 1,737 predictions.
- **The real gap is loops.** Most remaining errors (3↔5↔8, 9→8, 7→9, 0→8, 2→8) are about whether a part of the digit is closed. Linear stroke templates cannot express "closed".

**What changes in this step.** I free conv2 channels and use them for nonlinear loop features.

1. **Orientation features on a checkerboard.** Each of the 4 orientations now uses 2 diagonal sub-offsets, (1,1) and (2,2), instead of 4, giving 8 channels.
   - The features then sample the 8×8 grid on a checkerboard (32 cells per orientation).
   - With a template blur of 1.5 cells, very little is lost.
2. **Ink map.** conv1 channel 4 becomes a plain ink detector: the 2×2 centre mean of the kernel, with bias −0.15. Pooled, it gives a 12×12 ink map.
3. **Two loop detectors in conv2.** Both look at the ink map through a 5×5 window, which spans about 10 px.
   - **Channel 8, "left–right enclosure".** It needs ink in the left column and the right column of the window, and an empty centre cell. It is thresholded by a bias so that one side alone gives 0.
   - **Channel 9, "full ring".** It needs ink on all four sides of the window, and an empty centre. It is thresholded so that a C shape (three sides) gives 0.
   - After max-pooling, each detector reports where a loop is on a 4×4 grid. Row r = 0 is a top loop (9, 8, closed 4); rows 2–3 are a bottom loop (6, 8); 0 fires left–right along its whole height.
4. **fc weights for the loop channels.** These are drawn by hand, per class and per row.
   - Loops at the right height are rewarded: 0 gets centre loops, 6 bottom, 8 top and bottom, 9 top.
   - Loops are penalised for 1, 2, 3, 5 and 7.
5. **Kept from earlier steps.** The anti-strokes stay only for 4, 5 and 6. The biases are the cumulative ones from steps 3–7.

```python
import numpy as np
import math

def build_weights():
    s2 = 1.0 / math.sqrt(2.0)
    # Orientation unit vectors (dx, dy), x = column, y = row (DOWN)
    # k=0 horizontal, k=1 "\" diagonal, k=2 vertical, k=3 "/" diagonal
    dirs = [(1.0, 0.0), (s2, s2), (0.0, 1.0), (s2, -s2)]

    # ================= conv1 =================
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    # ch0-3: oriented line detectors (zero-mean ridge, centre (2.5,2.5))
    c1 = 2.5
    sig_line = 0.8
    for k, (dx, dy) in enumerate(dirs):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                u = i - c1; v = j - c1
                d = v * dy - u * dx
                K[i, j] = math.exp(-d * d / (2 * sig_line ** 2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = K
        b1[k] = -0.1
    # ch4: ink detector = mean of the 2x2 kernel centre (same centre 2.5,2.5)
    W1[4, 0, 2:4, 2:4] = 0.25
    b1[4] = -0.15
    # ch5-7 unused

    # ================= conv2 =================
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    # ch0-7: orientation pass-through, ch = k*2 + o, kernel pos (1+o, 1+o)
    #   feature (ch, r, c) = grid cell s=2r+o, t=2c+o of orientation k (centre row 2s+6, col 2t+6)
    for k in range(4):
        for o in range(2):
            W2[k * 2 + o, k, 1 + o, 1 + o] = 1.0
    # ch8: left-right enclosure on the ink map (ch4): ink left col & right col, empty centre
    for rr in range(1, 4):
        W2[8, 4, rr, 0] = 0.5
        W2[8, 4, rr, 4] = 0.5
    W2[8, 4, 2, 2] = -2.0
    b2[8] = -1.4          # one side only (~1.3) -> 0 ; both sides (~2.55) -> ~1.1
    # ch9: full ring: ink on all 4 sides, empty centre
    for m in range(1, 4):
        W2[9, 4, 0, m] = 0.5     # top
        W2[9, 4, 4, m] = 0.5     # bottom
        W2[9, 4, m, 0] = 0.5     # left
        W2[9, 4, m, 4] = 0.5     # right
    W2[9, 4, 2, 2] = -2.0
    b2[9] = -4.2          # 3 sides (~3.8) -> 0 ; 4 sides (~5.1) -> ~0.9
    # ch10-15 unused
    # Loop feature (ch, r, c): conv2 positions i in {2r,2r+1}, window centre input row 2i+7
    #   r=0 -> rows ~7-9, r=1 -> ~11-13, r=2 -> ~15-17, r=3 -> ~19-21 (same for columns)

    # ================= stroke templates =================
    def line(p, q, step=0.5):
        p = np.array(p, float); q = np.array(q, float)
        L = np.hypot(*(q - p))
        n = max(2, int(math.ceil(L / step)) + 1)
        return [tuple(p + (q - p) * t) for t in np.linspace(0, 1, n)]

    def poly(pts):
        out = []
        for a in range(len(pts) - 1):
            out += line(pts[a], pts[a + 1])
        return out

    def arc(cx, cy, rx, ry, t0, t1, n=120):
        return [(cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t)))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [arc(14, 13.5, 5.5, 8.5, 0, 360)],
        1: [line((15, 4.5), (13, 22.5))],
        2: [arc(14, 9, 5, 4.5, 160, -30),
            line((18.33, 11.25), (9, 22)),
            line((9, 22), (19.5, 22))],
        3: [arc(13.5, 9, 5, 4.5, 135, -90),
            line((13.5, 13.5), (11, 13.5)),
            arc(13.5, 18, 5.5, 4.5, 90, -150)],
        4: [line((10.5, 5), (8, 15)),
            line((8, 15), (20, 15)),
            line((17, 6.5), (16, 22.5))],
        5: [line((11, 5), (19, 5)),
            line((11, 5), (10.5, 13)),
            arc(13.5, 17.5, 5.5, 4.5, 140, -150)],
        6: [poly([(17.5, 4), (13.5, 6.5), (11, 10), (9.5, 14), (9.5, 18)]),
            arc(14, 18, 4.7, 4.7, 0, 360)],
        7: [line((8.5, 5), (19.5, 5)),
            line((19.5, 5), (12.5, 22.5))],
        8: [arc(14.5, 8.8, 3.8, 4.3, 0, 360),
            arc(13.5, 18, 4.8, 4.5, 0, 360)],
        9: [arc(14.5, 9, 4.5, 4.5, 0, 360),
            line((19, 9), (17, 22.5))],
    }
    # anti-strokes kept only where they helped in step 8
    anti = {d: [] for d in range(10)}
    anti[4] = [line((11, 4.5), (17, 4.5))]                       # 9's closed top
    anti[5] = [line((18.5, 7), (18.5, 11)), line((9, 15.5), (9.5, 18.5))]
    anti[6] = [arc(14, 13.5, 5.5, 8.5, 20, 80), line((14.5, 5), (19.5, 5))]
    lam_anti = 0.7

    base_shear = {d: 0.12 for d in range(10)}
    base_shear[8] = 0.22
    shear_spread = [-0.2, 0.0, 0.2]

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 3.0

    def render(strokes, shear):
        T = np.zeros((4, 8, 8))
        for pts in strokes:
            pts = np.asarray(pts, float).copy()
            pts[:, 0] = pts[:, 0] + shear * (13.5 - pts[:, 1])
            for a in range(len(pts) - 1):
                p, q = pts[a], pts[a + 1]
                dv = q - p
                L = math.hypot(dv[0], dv[1])
                if L < 1e-9:
                    continue
                ux, uy = dv / L
                mx, my = (p + q) / 2
                g = np.exp(-((Xg - mx) ** 2 + (Yg - my) ** 2) / (2 * sig_t ** 2))
                for k, (dx, dy) in enumerate(dirs):
                    dot = ux * dx + uy * dy
                    T[k] = np.maximum(T[k], g * dot ** 4)
        return T

    def blurred(strokes, d):
        if len(strokes) == 0:
            return np.zeros((4, 8, 8))
        return np.mean([render(strokes, base_shear[d] + ds) for ds in shear_spread], axis=0)

    # ================= fc =================
    beta = 3.0
    Wf = np.zeros((10, 256), np.float32)

    # --- orientation part: centred, unit-norm template sampled on the checkerboard ---
    for d in range(10):
        T = blurred(digits[d], d) - lam_anti * blurred(anti[d], d)
        vals = np.zeros((4, 2, 4, 4))
        for k in range(4):
            for o in range(2):
                for r in range(4):
                    for c in range(4):
                        vals[k, o, r, c] = T[k, 2 * r + o, 2 * c + o]
        vals = vals - vals.mean()
        vals = vals / (np.linalg.norm(vals) + 1e-9)
        for k in range(4):
            for o in range(2):
                ch = k * 2 + o
                for r in range(4):
                    for c in range(4):
                        Wf[d, ch * 16 + r * 4 + c] = beta * vals[k, o, r, c]

    # --- loop part: hand-set row profiles (r = 0 top .. 3 bottom), column weights ---
    colw = [0.5, 1.0, 1.0, 0.5]
    alpha = 1.5
    ring = {0: [0.5, 1, 1, 0.5], 1: [-1] * 4, 2: [-1] * 4, 3: [-1] * 4,
            4: [0.3, 0.3, -0.5, -0.5], 5: [-1] * 4, 6: [-1, -0.5, 1, 1],
            7: [-1] * 4, 8: [1, 0.5, 1, 1], 9: [1, 0.5, -1, -1]}
    lr = {0: [1, 1, 1, 1], 1: [-1] * 4, 2: [-0.5] * 4, 3: [-1] * 4,
          4: [1, 1, 0, -0.5], 5: [-1] * 4, 6: [-0.5, 0, 1, 1],
          7: [-0.5] * 4, 8: [0.5, 0.3, 0.5, 0.5], 9: [1, 0.5, -0.5, -0.5]}
    for d in range(10):
        for r in range(4):
            for c in range(4):
                Wf[d, 8 * 16 + r * 4 + c] = alpha * lr[d][r] * colw[c]
                Wf[d, 9 * 16 + r * 4 + c] = alpha * ring[d][r] * colw[c]

    # --- class biases (cumulative prior-shift from steps 3-7) ---
    true_cnt = np.array([1000, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    preds = [
        [1153, 1439, 1368, 567, 251, 687, 1668, 1524, 423, 920],
        [1312, 1420, 942, 687, 976, 877, 1017, 1397, 701, 675],
        [1198, 1491, 1022, 751, 916, 808, 1015, 1137, 768, 896],
        [1129, 1380, 881, 826, 838, 731, 967, 1057, 1257, 934],
        [1122, 1388, 960, 855, 881, 852, 929, 970, 1050, 994],
    ]
    bf = np.zeros(10)
    for p in preds:
        bf += 0.5 * np.log(true_cnt / np.array(p, float))

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wf.astype(np.float32),
        'fc.bias': bf.astype(np.float32),
    }
```
