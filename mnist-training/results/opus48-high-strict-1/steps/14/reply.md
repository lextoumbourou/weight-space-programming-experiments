## Step 14

New best at 40.63%. The dominant remaining error is still **4→9 (540)** with almost no reverse flow (9→4 = 69), and 9 is still heavily over-predicted (1655×) while 4 is starved (531×). That huge asymmetry means a bias shift toward 4 is nearly free accuracy.

This step is a safe bias-only update on the best (step-13) config: data-driven rebalance from step-13's marginals — notably lifting 4 (−1.33→−0.95) and damping 9 (−1.54→−1.84), plus damping over-predicted 1/3. I keep this as a low-risk test before the final scored step.

```python
import numpy as np

def build_weights():
    # ---------- conv1: 3x3 ink-density average ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, 1:4, 1:4] = 1.0 / 9.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---------- conv2: ch0-13 ink offsets, ch14-15 ring/hole detectors ----------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(14):
        a = 1 + k // 4
        b = 1 + k % 4
        conv2_w[k, 0, a, b] = 1.0
    ring = np.full((5, 5), 1.0 / 16.0, np.float32)
    ring[1:4, 1:4] = -1.0 / 9.0
    conv2_b = np.zeros((16,), dtype=np.float32)
    for k in (14, 15):
        conv2_w[k, 0, :, :] = ring
        conv2_b[k] = -0.20

    # ---------- hand-drawn 12x12 ink templates ('#' = ink) ----------
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
        4: ["............","......#.....","......#.....",".....##.....",
            "....#.#.....","...#..#.....","..#######...","......#.....",
            "......#.....","......#.....","............","............"],
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

    # ---------- 4x4 hole templates ----------
    H = {d: np.zeros((4, 4), np.float32) for d in range(10)}
    H[0] = np.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]], np.float32)
    H[8] = np.array([[0,1,1,0],[0,0,0,0],[0,0,0,0],[0,1,1,0]], np.float32)
    H[9] = np.array([[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]], np.float32)
    H[6] = np.array([[0,0,0,0],[0,0,0,0],[0,1,1,0],[0,1,1,0]], np.float32)
    Hbar = np.mean(np.stack([H[d] for d in range(10)]), axis=0)

    # ---------- assemble fc ----------
    scale_ink = 6.0
    scale_hole = 2.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    ink_idx = [k * 16 + R * 4 + C for k in range(14) for R in range(4) for C in range(4)]
    for d in range(10):
        v = np.zeros(256, dtype=np.float32)
        for k in range(14):
            a = 1 + k // 4
            b = 1 + k % 4
            for R in range(4):
                for C in range(4):
                    p = 2 * R + a
                    q = 2 * C + b
                    v[k * 16 + R * 4 + C] = Tc[d, p, q]
        sub = v[ink_idx]
        sub = sub - sub.mean()
        n = np.linalg.norm(sub)
        if n > 0:
            sub = sub / n
        v[ink_idx] = scale_ink * sub
        for k in (14, 15):
            for R in range(4):
                for C in range(4):
                    v[k * 16 + R * 4 + C] = scale_hole * (H[d][R, C] - Hbar[R, C])
        fc_w[d] = v

    # ---------- biases: step-13 marginal rebalance (lift 4, damp 9/1/3) ----------
    fc_b = np.array([2.00, -1.62, 0.32, -0.51, -0.95,
                     1.95, 1.04, 1.87, 1.78, -1.84], dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
