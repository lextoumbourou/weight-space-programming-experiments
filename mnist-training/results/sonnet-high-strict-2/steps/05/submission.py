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

    c1[0, 0] = ridge(ys)
    c1[1, 0] = ridge(xs)
    c1[2, 0] = ridge((ys - xs) / math.sqrt(2))
    c1[3, 0] = ridge((ys + xs) / math.sqrt(2))
    blob = np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.2 ** 2))
    c1[4, 0] = blob / blob.sum()                  # ink density (used downstream)

    def edge(g):
        g = g * np.exp(-(xs ** 2 + ys ** 2) / (2 * 1.3 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    c1[5, 0] = edge(ys)
    c1[6, 0] = edge(xs)
    c1[7, 0] = edge(-xs)
    b1 = np.zeros(8)

    # ---------------- conv2: ink sampler at kernel offsets (i,j) in {1,2,3}^2 ----------------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16)
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            c2[(i - 1) * 3 + (j - 1), 4, i, j] = 1.0

    # ---------------- 9x9 hand-drawn ink templates ----------------
    m = {'#': 1.0, '+': 0.5, '-': -0.5, '.': 0.0}
    tpl = {
        0: ["..+###+..",
            ".+#+-+#+.",
            ".##---##.",
            ".#+---+#.",
            ".#+---+#.",
            ".##---##.",
            ".#+---+#.",
            ".+#+-+#+.",
            "..+###+.."],
        1: ["....+#+..",
            "...+##+..",
            ".-..##.-.",
            ".-..##.-.",
            ".-..##.-.",
            ".-..##.-.",
            ".-..##.-.",
            ".-..##.-.",
            "....##..."],
        2: ["..+###+..",
            ".+#+.+#+.",
            ".....+#+.",
            ".....##+.",
            "....##+..",
            "...##+...",
            "..##+....",
            ".+#+.....",
            ".#######."],
        3: [".+####+..",
            ".-..++#+.",
            ".--..+#+.",
            "...+###+.",
            ".--..+##.",
            ".--..+#+.",
            ".-...+#+.",
            ".+...+#+.",
            "..+###+.."],
        4: ["...+#-.#+",
            "..+#--.#+",
            ".+#-...#+",
            ".#+....#+",
            ".#######+",
            "......##+",
            "......##+",
            "......##.",
            "......##."],
        5: [".#######.",
            ".##......",
            ".##+++...",
            ".#####+..",
            "....+##+.",
            ".....+##.",
            ".....+#+.",
            ".+..+##+.",
            "..+###+.."],
        6: ["....+##+.",
            "...##+...",
            "..##+....",
            ".##+###+.",
            ".##+..+#+",
            ".#+---+#+",
            ".##+-+#+.",
            "..+####+.",
            "...+##+.."],
        7: [".#######.",
            "......#+.",
            ".....##+.",
            ".....#+..",
            "....##+..",
            "...##+...",
            "...#+....",
            "..##+....",
            "..#+....."],
        8: ["..+###+..",
            ".+#+-+#+.",
            ".+#+-+#+.",
            "..+###+..",
            "...###...",
            "..+###+..",
            ".+#+-+#+.",
            ".+#+-+#+.",
            "..+###+.."],
        9: ["..+###+..",
            ".+#+-+#+.",
            ".+#+-+#+.",
            "..+####+.",
            ".....+#+.",
            ".....+#+.",
            ".....#+..",
            "....##+..",
            "....#+..."],
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
    lam = 1.5   # penalty weight for ink outside the template
    fcw = np.zeros((10, 16, 4, 4))
    fcb = np.zeros(10)
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
    fcw = fcw.reshape(10, 256)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
