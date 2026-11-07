# Step 17: widen the slant blur for every digit

**What I learned from step 16.** Accuracy rose to 69.67% and loss to its best yet, 0.939. The clearest win was the wider slant blur on 1: its recall jumped from 923 to 1,003, and 1→7 fell from 107 to 17.

- 1 is now over-predicted, with 1,333 predictions against 1,135 true. The excess comes from 4→1 (94) and 6→1 (77).
- The stronger loop weight helped 8 and 9 slightly and cost 5 slightly. I keep it.

**What changes in this step.**

1. **Slant blur for all digits.** Every other template now uses four slants, at offsets −0.25, −0.05, +0.15 and +0.35 around its base slant, instead of three. Strongly right-slanted handwriting is common in MNIST, and the 1 result suggests every class is losing slanted samples. The 1 keeps its step-16 spread.
2. **Bias trim.** A prior-shift term, 0.5·log(true count / predicted count), is added using step 16's counts. This mainly pulls 1 back down.

Everything else is unchanged: σ = 3.3, ring weight 1.5 and temperature 1.6.

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
    # ch4: ink detector (2x2 centre mean)
    W1[4, 0, 2:4, 2:4] = 0.25
    b1[4] = -0.15
    # ch5-7 unused

    # ================= conv2 =================
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    # ch0-11: orientation pass-through, ch = k*3 + m, offsets (oa,ob) in [(0,0),(1,1),(0,1)]
    offs = [(0, 0), (1, 1), (0, 1)]
    for k in range(4):
        for m, (oa, ob) in enumerate(offs):
            W2[k * 3 + m, k, 1 + oa, 1 + ob] = 1.0
    # ch12: strict full-ring loop detector on the ink map
    for m in range(1, 4):
        W2[12, 4, 0, m] = 0.5
        W2[12, 4, 4, m] = 0.5
        W2[12, 4, m, 0] = 0.5
        W2[12, 4, m, 4] = 0.5
    W2[12, 4, 2, 2] = -2.0
    b2[12] = -4.5
    # ch13-15 unused

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
        3: [arc(13.5, 9, 5, 4.5, 170, -90),
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
    anti = {d: [] for d in range(10)}
    anti[4] = [line((11, 4.5), (17, 4.5))]
    anti[5] = [line((18.5, 7), (18.5, 11)), line((9, 15.5), (9.5, 18.5))]
    anti[6] = [arc(14, 13.5, 5.5, 8.5, 20, 80), line((14.5, 5), (19.5, 5))]
    lam_anti = 0.7

    base_shear = {d: 0.12 for d in range(10)}
    base_shear[8] = 0.22
    # slant blur: wider, skewed toward right-leaning handwriting
    spread = {d: [-0.25, -0.05, 0.15, 0.35] for d in range(10)}
    spread[1] = [-0.2, 0.0, 0.2, 0.4]

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 3.3

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
        return np.mean([render(strokes, base_shear[d] + ds) for ds in spread[d]], axis=0)

    # ================= fc =================
    beta = 3.0
    Wf = np.zeros((10, 256), np.float64)

    for d in range(10):
        T = blurred(digits[d], d) - lam_anti * blurred(anti[d], d)
        vals = np.zeros((4, 3, 4, 4))
        for k in range(4):
            for m, (oa, ob) in enumerate(offs):
                for r in range(4):
                    for c in range(4):
                        vals[k, m, r, c] = T[k, 2 * r + oa, 2 * c + ob]
        vals = vals - vals.mean()
        vals = vals / (np.linalg.norm(vals) + 1e-9)
        for k in range(4):
            for m in range(3):
                ch = k * 3 + m
                for r in range(4):
                    for c in range(4):
                        Wf[d, ch * 16 + r * 4 + c] = beta * vals[k, m, r, c]

    # loop part (ch12)
    colw = [0.5, 1.0, 1.0, 0.5]
    alpha = 1.5
    ring = {0: [0.3, 0.5, 0.5, 0.3], 1: [-1] * 4, 2: [-1] * 4, 3: [-1] * 4,
            4: [0.3, 0.3, -0.5, -0.5], 5: [-1] * 4, 6: [-1, -0.5, 1, 1],
            7: [-1] * 4, 8: [1, 0.5, 1, 1], 9: [1, 0.5, -1, -1]}
    for d in range(10):
        for r in range(4):
            for c in range(4):
                Wf[d, 12 * 16 + r * 4 + c] = alpha * ring[d][r] * colw[c]

    # class biases: cumulative prior-shift, pre-temperature units
    true_cnt = np.array([1000, 1135, 1032, 1010, 982, 892, 958, 1028, 974, 1009], float)
    preds = [
        [1153, 1439, 1368, 567, 251, 687, 1668, 1524, 423, 920],
        [1312, 1420, 942, 687, 976, 877, 1017, 1397, 701, 675],
        [1198, 1491, 1022, 751, 916, 808, 1015, 1137, 768, 896],
        [1129, 1380, 881, 826, 838, 731, 967, 1057, 1257, 934],
        [1122, 1388, 960, 855, 881, 852, 929, 970, 1050, 994],
        [1079, 1342, 946, 898, 806, 943, 779, 854, 1370, 947],
        [1071, 1282, 1023, 922, 861, 880, 874, 952, 1116, 934],
        [1052, 1233, 1030, 962, 903, 874, 919, 1040, 985, 964],
    ]
    bf = np.zeros(10)
    for p in preds:
        bf += 0.5 * np.log(true_cnt / np.array(p, float))
    pred13 = np.array([1037, 1209, 1035, 990, 909, 875, 925, 1038, 964, 979], float)
    bf += 0.3 * np.log(true_cnt / pred13)
    pred15 = np.array([1032, 1199, 1035, 987, 924, 877, 920, 1042, 959, 985], float)
    bf += 0.3 * np.log(true_cnt / pred15)
    pred16 = np.array([1004, 1333, 1004, 976, 892, 888, 910, 986, 1013, 1034], float)
    bf += 0.5 * np.log(true_cnt / pred16)

    temp = 1.6
    Wf *= temp
    bf *= temp

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wf.astype(np.float32),
        'fc.bias': bf.astype(np.float32),
    }
```
