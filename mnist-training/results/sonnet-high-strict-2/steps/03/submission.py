import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 filters (only the blob is used now) ----------------
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
    # channel (i-1)*3+(j-1) outputs B[p+i, p+j]; 2x2 maxpool then gives a 4x4 grid of
    # pair-maxima centred at pooled index 2a+i+0.5.
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

    # how many (a,i) pairs map to each grid index k = 2a+i-1
    cnt = np.zeros(9)
    for a in range(4):
        for i in (1, 2, 3):
            cnt[2 * a + i - 1] += 1

    s = 1.0
    fcw = np.zeros((10, 16, 4, 4))
    fcb = np.zeros(10)
    for d in range(10):
        T = np.array([[m[ch] for ch in row] for row in tpl[d]])
        for i in (1, 2, 3):
            for j in (1, 2, 3):
                ch = (i - 1) * 3 + (j - 1)
                for a in range(4):
                    for b in range(4):
                        kr = 2 * a + i - 1
                        kc = 2 * b + j - 1
                        fcw[d, ch, a, b] = s * T[kr, kc] / (cnt[kr] * cnt[kc])
        fcb[d] = -0.35 * s * np.sum(np.clip(T, 0, None) ** 2)
    fcw = fcw.reshape(10, 256)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
