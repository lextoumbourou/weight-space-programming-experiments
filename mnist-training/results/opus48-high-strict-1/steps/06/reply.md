## Step 6

Now at 38.6%. The step-5 redraw of **7** backfired badly (only 7 correct — its diagonal collided with 1 and 9), while **9** improved (244→348) so I'll keep that. Biggest remaining errors: 7 (barely ever predicted — under-predicted at 199), 8→2, and 9→4.

This step:
- **Redraw 7** with a *thick, emphatic top bar* (the one feature unique to 7 vs 1/9) plus a compact diagonal, leaving mid/lower-left empty (→ negative after centering) to repel 1 and 9.
- **Re-tune biases** from step-5 marginals (compounded `-0.7·ln(pred/1000)`): strong boost to the collapsed 7, and a strong push-down on the over-predicted 4 (now −1.95) to free up 9.

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
        7: ["............","..#######...",".......#....","......##....",
            "......#.....",".....##.....",".....#......","....##......",
            "....#.......","............","............","............"],
        8: ["............","...#####....","..##...##...","..##...##...",
            "...#####....","..##...##...","..#.....#...","..#.....#...",
            "..##...##...","...#####....","............","............"],
        9: ["............","...#####....","..##...##...","..#.....#...",
            "..##...##...","...######...","......##....","......##....",
            "......##....","......#.....","............","............"],
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

    # ---------- per-class bias (compounded marginal correction) ----------
    fc_b = np.array([1.578, -1.002, 0.502, -0.226, -1.949,
                     1.539, 1.079, 1.403, 0.928, -0.574], dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
