## Step 4

Good jump to 35%. Zero-mean + normalized matching works. Now the confusion matrix shows two clear issues: (1) loss is still high (overconfident), and (2) the predicted-class marginals are very unbalanced — digit **4** is predicted 2597 times and **1** 1561 times, while **5** only 397. That imbalance is costing accuracy.

This step I keep the feature/template design and make two calibrations:
- **Lower the logit scale** (8 → 6) to reduce overconfidence and loss.
- **Add per-class biases** that correct the predicted marginals toward uniform: `bias_d = -1.2 · ln(pred_count_d / 1000)`, computed from this step's confusion matrix. This demotes over-predicted 4/1/9 and promotes under-predicted 5/0/6/8.

```python
import numpy as np

def build_weights():
    # ---------- conv1: sharper 3x3 average ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, 1:4, 1:4] = 1.0 / 9.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---------- conv2: 16 delta filters sampling the ink map at offsets ----------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(16):
        a = 1 + k // 4
        b = 1 + k % 4
        conv2_w[k, 0, a, b] = 1.0
    conv2_b = np.zeros((16,), dtype=np.float32)

    # ---------- hand-drawn 12x12 digit templates ('#' = ink) ----------
    T = {
        0: ["............","...#####....","..##...##...","..#.....#...",
            "..#.....#...","..#.....#...","..#.....#...","..#.....#...",
            "..##...##...","...#####....","............","............"],
        1: ["............",".....##.....","....###.....","...#.##.....",
            ".....##.....",".....##.....",".....##.....",".....##.....",
            ".....##.....","...######...","............","............"],
        2: ["............","...#####....","..##...##...",".......##...",
            "......##....",".....##.....","....##......","...##.......",
            "..##........","..#######...","............","............"],
        3: ["............","..######....","......##....",".....##.....",
            "...####.....",".....##.....","......##....",".......#....",
            "..#...##....","...####.....","............","............"],
        4: ["............","......##....",".....###....","....#.##....",
            "...#..##....","..#...##....","..#######...","......##....",
            "......##....","......##....","............","............"],
        5: ["............","..######....","..##........","..##........",
            "..#####.....","......##....",".......##...",".......##...",
            "..#...##....","...####.....","............","............"],
        6: ["............","....####....","...##.......","..##........",
            "..#.........","..#####.....","..##...##...","..#.....#...",
            "..##...##...","...#####....","............","............"],
        7: ["............","..#######...",".......##...","......##....",
            ".....##.....","....##......","....##......","...##.......",
            "...##.......","...##.......","............","............"],
        8: ["............","...#####....","..##...##...","..##...##...",
            "...#####....","..##...##...","..#.....#...","..#.....#...",
            "..##...##...","...#####....","............","............"],
        9: ["............","...#####....","..##...##...","..#.....#...",
            "..##...##...","...######...",".......##...","......##....",
            ".....##.....","...###......","............","............"],
    }
    IMG = np.zeros((10, 12, 12), dtype=np.float32)
    for d in range(10):
        for r in range(12):
            for c in range(12):
                IMG[d, r, c] = 1.0 if T[d][r][c] == '#' else 0.0

    Ebar = IMG.mean(axis=0, keepdims=True)
    Tc = IMG - Ebar

    # ---------- fc: zero-mean + L2-normalise each class vector ----------
    scale = 6.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        v = np.zeros(256, dtype=np.float32)
        for k in range(16):
            a = 1 + k // 4
            b = 1 + k % 4
            for R in range(4):
                for C in range(4):
                    p = 2 * R + a
                    q = 2 * C + b
                    idx = k * 16 + R * 4 + C
                    v[idx] = Tc[d, p, q]
        v = v - v.mean()
        n = np.linalg.norm(v)
        if n > 0:
            v = v / n
        fc_w[d] = scale * v

    # ---------- per-class bias to balance predicted marginals ----------
    # bias_d = -1.2 * ln(pred_count_d / 1000) from step-3 confusion matrix
    fc_b = np.array([0.787, -0.534, 0.572, -0.025, -1.145,
                     1.109, 0.609, 0.205, 0.454, -0.174], dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
