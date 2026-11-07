# Step 25: halve the 5 anti-arc and revert the loop weight

**What I learned from step 24.** The full-arc anti-stroke on 5 had a large effect on both classes. Overall accuracy fell from 73.27% to 72.67%.

- **3 improved sharply.** Recall rose from 637 to 717, and 3→5 fell from 230 to 135.
- **5 got much worse.** Recall fell from 610 to 468: 5→6 rose to 201 and 5→3 to 77. Real 5s evidently carry some ink in the upper-right region too, from the end of the top bar and the shoulder of the bowl.
- **5 is under-predicted.** It got 638 predictions against 892 true.

The stronger ring weight (α = 2.0) changed at the same time, so its effect is unclear. I return it to the known-good 1.5.

**What changes in this step.**

1. **Half-strength anti-arc.** The 5's upper-right anti-arc keeps the full 3-bowl shape but at weight 0.5. The aim is to keep much of 3's gain while giving back most of 5's loss.
2. **Ring weight back to 1.5.**
3. **Bias trim.** A term of 0.3·log(true count / predicted count) is added using step 24's counts. It mainly raises 5, which is under-predicted.

Everything else is unchanged.

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

    W = lambda pts, w=1.0: (pts, w)

    digits = {
        0: [W(arc(14, 13.5, 5.5, 8.5, 0, 360))],
        1: [W(line((15, 4.5), (13, 22.5)))],
        2: [W(arc(14, 9, 5, 4.5, 160, -10)),
            W(poly([(18.9, 9.8), (18.0, 12.5), (15.5, 15.5), (12.0, 18.8), (9.0, 22.0)])),
            W(line((9, 22), (19.5, 22)))],
        3: [W(arc(13.5, 9, 5, 4.5, 170, -90)),
            W(line((13.5, 13.5), (11, 13.5))),
            W(arc(13.5, 18, 5.5, 4.5, 90, -150))],
        4: [W(line((10.5, 5), (8, 15))),
            W(line((8, 15), (20, 15))),
            W(line((17, 6.5), (16, 22.5)))],
        5: [W(line((11, 5), (19, 5))),
            W(line((11, 5), (10.5, 13))),
            W(arc(13.5, 17.5, 5.5, 4.5, 140, -150))],
        6: [W(poly([(17.5, 4), (13.5, 6.5), (11, 10), (9.5, 14), (9.5, 18)])),
            W(arc(14, 18, 4.7, 4.7, 0, 360))],
        7: [W(line((8.5, 5), (19.5, 5))),
            W(line((19.5, 5), (12.5, 22.5)))],
        8: [W(arc(14, 8.5, 4.0, 3.8, 0, 180)),
            W(line((10, 8.5), (18.5, 18))),
            W(arc(14, 18, 4.5, 4.3, 0, -180)),
            W(line((9.5, 18), (18, 8.5)))],
        9: [W(arc(14.5, 9, 4.5, 4.5, 0, 360)),
            W(line((19, 9), (17, 22.5)))],
    }
    anti = {d: [] for d in range(10)}
    anti[4] = [W(line((11, 4.5), (17, 4.5))),                 # 9's closed top
               W(arc(14, 18, 4.5, 4.3, 200, 250))]            # 6's bottom-left loop
    anti[5] = [W(arc(13.5, 9, 5, 4.5, 60, -50), 0.5),         # 3's upper-right bowl (half strength)
               W(line((9, 15.5), (9.5, 18.5)))]               # 6's closed left
    anti[6] = [W(arc(14, 13.5, 5.5, 8.5, 20, 80)), W(line((14.5, 5), (19.5, 5)))]
    anti[9] = [W(arc(14, 18, 4.5, 4.3, 160, 250), 0.4)]       # 8's bottom-left loop (soft)
    lam_anti = 0.7

    base_shear = {d: 0.12 for d in range(10)}
    base_shear[8] = 0.22
    narrow = [-0.2, 0.0, 0.2]
    wide = [-0.25, -0.05, 0.15, 0.35]
    spread = {d: narrow for d in range(10)}
    for d in (0, 9):
        spread[d] = wide
    spread[1] = [-0.2, 0.0, 0.2, 0.4]

    centers = 2.0 * np.arange(8) + 6.0
    Yg, Xg = np.meshgrid(centers, centers, indexing='ij')
    sig_t = 3.3

    def render(strokes, shear):
        T = np.zeros((4, 8, 8))
        for pts, wgt in strokes:
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
                g = wgt * np.exp(-((Xg - mx) ** 2 + (Yg - my) ** 2) / (2 * sig_t ** 2))
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
            4: [-0.3, 0.3, -0.5, -0.5], 5: [-1] * 4, 6: [-1, -0.5, 1, 1],
            7: [-1] * 4, 8: [1, 0.5, 1.5, 1.5], 9: [1, 0.5, -1.5, -1.5]}
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
    extra = [
        (0.3, [1037, 1209, 1035, 990, 909, 875, 925, 1038, 964, 979]),   # step 13
        (0.3, [1032, 1199, 1035, 987, 924, 877, 920, 1042, 959, 985]),   # step 15
        (0.5, [1004, 1333, 1004, 976, 892, 888, 910, 986, 1013, 1034]),  # step 16
        (0.3, [1074, 1292, 956, 960, 896, 1030, 898, 937, 884, 1095]),   # step 18
        (0.3, [1062, 1194, 895, 964, 951, 1011, 942, 921, 1022, 1041]),  # step 19
        (0.3, [1045, 1184, 938, 1141, 974, 837, 941, 950, 989, 1001]),   # step 20
        (0.3, [1025, 1182, 931, 1017, 975, 867, 938, 1003, 1033, 1036]), # step 21
        (0.5, [1061, 1212, 1001, 1008, 982, 882, 1034, 1043, 1019, 698]),# step 22
        (0.3, [1032, 1186, 995, 967, 906, 881, 997, 974, 963, 980]),     # step 23
        (0.3, [1029, 1170, 996, 1100, 977, 638, 1052, 983, 977, 996]),   # step 24
    ]
    for g, p in extra:
        bf += g * np.log(true_cnt / np.array(p, float))

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
