## Step 3

Step 2 was much worse — loss exploded and predictions collapsed to the two "inkiest" digits (4, 8). I now understand the failure mode: after the average+max-pool, the feature map is **nearly uniformly high wherever the digit is**, so the logit is dominated by the *overall* template magnitude rather than *shape*. Whichever digit's template has the largest total weight always wins.

Two fixes this step:
1. **Zero-mean each digit's weight vector** so a constant feature map produces logit 0 for every class — only genuine spatial *variation* counts (normalized cross-correlation matching).
2. **L2-normalize each class's weight vector** so no digit can win just by having more total ink in its template.
3. Sharper conv1 (3×3 average) to retain more shape detail, and a tuned global `scale`.

```python
import numpy as np

def build_weights():
    # ---------- conv1: sharper 3x3 average (in center of 5x5) ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, 1:4, 1:4] = 1.0 / 9.0     # local ink density, less blur
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

    # emphasise distinctive regions by subtracting the across-digit mean
    Ebar = IMG.mean(axis=0, keepdims=True)
    Tc = IMG - Ebar

    # ---------- fc: build, zero-mean, L2-normalise each class vector ----------
    scale = 8.0
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
        v = v - v.mean()                      # constant feature -> logit 0
        n = np.linalg.norm(v)
        if n > 0:
            v = v / n                         # equalise class magnitudes
        fc_w[d] = scale * v
    fc_b = np.zeros((10,), dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
