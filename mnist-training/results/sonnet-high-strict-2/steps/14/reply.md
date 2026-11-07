Step 13 reached 52.2%. The orientation scale has been climbing steadily, so this step raises it again from 4.8 to 6.0. I'm also making small bias corrections from the step-13 column sums: 7, 3, 6 and 1 are lowered, and 8 is raised, since 8 is under-predicted and 7 is over-predicted.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1 ----------------
    c1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)

    def ridge(d, sig=0.9):
        w = np.exp(-d ** 2 / (2 * sig ** 2))
        w = w - w.mean()
        return w / w[w > 0].sum()

    c1[0, 0] = ridge(ys)                          # horizontal
    c1[1, 0] = ridge(xs)                          # vertical
    c1[2, 0] = ridge((ys - xs) / math.sqrt(2))    # "\"
    c1[3, 0] = ridge((ys + xs) / math.sqrt(2))    # "/"
    blob = np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.2 ** 2))
    c1[4, 0] = blob / blob.sum()                  # ink density

    def edge(g):
        g = g * np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.3 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    c1[5, 0] = edge(ys)
    c1[6, 0] = edge(xs)
    c1[7, 0] = edge(-xs)
    b1 = np.zeros(8)

    # ---------------- conv2 ----------------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16)
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            c2[(i - 1) * 3 + (j - 1), 4, i, j] = 1.0
    for o in range(4):
        c2[9 + o, o, :, :] = 0.04

    # ---------------- ASCII ink templates ----------------
    m = {'#': 1.0, '+': 0.5, '-': -0.5, '.': 0.0}
    tpl = {
        0: ["..+###+..", ".+#+-+#+.", ".##---##.", ".#+---+#.", ".#+---+#.",
            ".##---##.", ".#+---+#.", ".+#+-+#+.", "..+###+.."],
        1: [".....##..", "....+#+..", ".-..+#+-.", ".-..##.-.", ".-.+#+.-.",
            ".-.+#+.-.", ".-.##..-.", ".-.##..-.", "..+#+...."],
        2: ["..+###+..", ".+#+.+#+.", ".....+#+.", ".....##+.", "....##+..",
            "...##+...", "..##+....", ".+#+.....", ".#######."],
        3: [".+####+..", ".-..++#+.", ".--..+#+.", "...+###+.", ".--..+##.",
            ".--..+#+.", ".-...+#+.", ".+...+#+.", "..+###+.."],
        4: ["...+#-.#+", "..+#--.#+", ".+#-...#+", ".#+....#+", ".#######+",
            "......##+", "......##+", "......##.", "......##."],
        5: [".#######.", ".##......", ".##+++...", ".#####+..", "....+##+.",
            ".....+##.", ".....+#+.", ".+..+##+.", "..+###+.."],
        6: ["....+##+.", "...##+...", "..##+....", ".##+###+.", ".##+..+#+",
            ".#+---+#+", ".##+-+#+.", "..+####+.", "...+##+.."],
        7: [".#######.", "......#+.", ".....##+.", ".....#+..", "....##+..",
            "...##+...", "...#+....", "..##+....", "..#+....."],
        8: ["..+###+..", ".+#+-+#+.", ".+#+-+#+.", "..+###+..", "...###...",
            "..+###+..", ".+#+-+#+.", ".+#+-+#+.", "..+###+.."],
        9: ["..+###+..", ".+#---#+.", ".+#---#+.", "..+####+.", ".....+#+.",
            ".....+#+.", ".....#+..", "....##+..", "....#+..."],
    }

    def blur(A):
        k = np.array([1.0, 2.0, 1.0]) / 4.0
        P = np.pad(A, 1)
        out = np.zeros_like(A)
        for di in range(3):
            for dj in range(3):
                out += k[di] * k[dj] * P[di:di + 9, dj:dj + 9]
        return out

    cnt = np.zeros(9)
    for a in range(4):
        for i in (1, 2, 3):
            cnt[2 * a + i - 1] += 1

    s = 15.0
    lam = 1.5
    fcw = np.zeros((10, 16, 4, 4))
    for d in range(10):
        T = np.array([[m[ch] for ch in row] for row in tpl[d]])
        pos = np.clip(T, 0, None)
        neg = np.clip(-T, 0, None) * 2.0
        P = np.clip(blur(pos) * 1.3, 0, 1)
        N = np.clip(blur(neg), 0, 1)
        Q = (1.0 - P) * (1.0 + 1.5 * N)
        W = s * (P / P.sum() - lam * Q / Q.sum())
        for i in (1, 2, 3):
            for j in (1, 2, 3):
                ch = (i - 1) * 3 + (j - 1)
                for a in range(4):
                    for b in range(4):
                        kr = 2 * a + i - 1
                        kc = 2 * b + j - 1
                        fcw[d, ch, a, b] = W[kr, kc] / (cnt[kr] * cnt[kc])

    # ---------------- hand-described strokes (row, col in 9x9 grid units) ----------------
    def ell(cr, cc, rr, rc, n=20):
        pts = []
        for t in range(n + 1):
            th = 2 * math.pi * t / n
            pts.append((cr - rr * math.cos(th), cc + rc * math.sin(th)))
        return pts

    strokes = {
        0: [ell(4, 4, 4.0, 3.0)],
        1: [[(0.3, 5.5), (8.2, 3.3)], [(1.3, 4.0), (0.3, 5.5)]],
        2: [[(1.5, 1.2), (0.4, 2.5), (0.2, 4), (1, 5.5), (2.3, 5.8), (3.5, 5.0),
             (5, 3.5), (6.5, 2), (8, 1.2), (8, 7.2)]],
        3: [[(1, 1.5), (0.2, 3), (0.3, 4.5), (1.3, 5.5), (2.5, 5.2), (3.7, 3.5),
             (4.0, 4.8), (5.2, 5.8), (6.5, 5.6), (7.7, 4.5), (8, 3), (7.3, 1.5)]],
        4: [[(0.2, 5), (5, 1), (5.3, 7.5)], [(0, 5.2), (8.3, 5.3)]],
        5: [[(0.4, 6.2), (0.4, 2.2), (3.3, 1.8), (3.3, 3.5), (3.8, 5.0), (5.2, 6.0),
             (6.8, 5.8), (7.9, 4.5), (8.1, 3.0), (7.5, 1.3)]],
        6: [[(0.5, 5.5), (1.5, 3.5), (3, 2.2), (5, 1.3), (6.8, 1.5), (7.9, 3),
             (7.9, 4.8), (6.8, 6), (5.3, 6), (4.2, 4.8), (4.2, 3.2), (5, 2)]],
        7: [[(0.4, 1), (0.4, 7), (2, 6.3), (4, 5.3), (6, 4.2), (8.3, 3.2)]],
        8: [ell(2, 4, 2.0, 2.2), ell(6, 4, 2.2, 2.6)],
        9: [ell(2.3, 4.2, 2.3, 2.5), [(2.5, 6.6), (5, 6.3), (8.3, 5.2)]],
    }

    gr, gc = np.mgrid[0:9, 0:9].astype(np.float64)

    def seg_dist(p, q):
        pr, pc = p
        qr, qc = q
        vr, vc = qr - pr, qc - pc
        L2 = vr * vr + vc * vc + 1e-9
        t = np.clip(((gr - pr) * vr + (gc - pc) * vc) / L2, 0, 1)
        return np.sqrt((gr - (pr + t * vr)) ** 2 + (gc - (pc + t * vc)) ** 2)

    orient_dirs = [0.0, 90.0, 45.0, 135.0]   # H, V, "\", "/"
    sig = 0.9
    Oc = np.zeros((10, 4, 4, 4))
    for d in range(10):
        O = np.zeros((4, 9, 9))
        for st in strokes[d]:
            for p, q in zip(st[:-1], st[1:]):
                dr, dc = q[0] - p[0], q[1] - p[1]
                if abs(dr) + abs(dc) < 1e-6:
                    continue
                phi = math.degrees(math.atan2(dr, dc))
                ink = np.exp(-seg_dist(p, q) ** 2 / (2 * sig ** 2))
                for o in range(4):
                    dd = abs((phi - orient_dirs[o] + 90.0) % 180.0 - 90.0)
                    w = math.cos(math.radians(dd)) ** 4
                    O[o] = np.maximum(O[o], ink * w)
        for o in range(4):
            for a in range(4):
                for b in range(4):
                    k, l = 2 * a + 1, 2 * b + 1
                    Oc[d, o, a, b] = O[o, k - 1:k + 2, l - 1:l + 2].mean()
    s_o = 6.0
    Wo = Oc - Oc.mean(axis=0, keepdims=True)
    Wo = Wo - Wo.mean(axis=(2, 3), keepdims=True)
    Wo = s_o * Wo
    for o in range(4):
        fcw[:, 9 + o] = Wo[:, o]

    fcw = fcw.reshape(10, 256)

    # biases lightly re-centred with the step-13 column sums
    fcb = np.array([0.9, -2.1, 0.2, -0.55, 0.8, 0.1, -0.7, -0.4, 0.1, 0.1])

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
