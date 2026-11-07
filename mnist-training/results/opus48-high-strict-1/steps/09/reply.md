## Step 9

Bias tuning has basically converged, and we're stuck at ~39% because at this resolution the ink-density map genuinely can't tell apart **0/8/2** and **4/9** (the dominant errors: 0→8 382, 9→4 471, 8→2 357). These are *loop/hole* distinctions.

My earlier hole attempt failed because the 5×5 detector ran on the **28×28** image where holes are too big to sit inside a 5×5 ring. The fix: run the ring detector in **conv2**, on the already-pooled 12×12 ink map, where holes are ~4–6 px and fit the 5×5 ring nicely. I use 14 channels for ink sampling and just 2 for the hole map, a strict threshold to suppress false fires, and compact hole templates (0 centre, 8 top+bottom, 9 upper, 6 lower; zero/negative elsewhere). This directly targets 9-vs-4 (9 has an upper hole, 4 doesn't) and 0/8-vs-2.

```python
import numpy as np

def build_weights():
    # ---------- conv1: 3x3 ink-density average ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, 1:4, 1:4] = 1.0 / 9.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---------- conv2: ch0-13 ink offsets, ch14-15 ring/hole detectors ----------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(14):                       # ink delta samplers
        a = 1 + k // 4                        # a in {1,2,3,4}
        b = 1 + k % 4                         # b in {1,2,3,4}
        conv2_w[k, 0, a, b] = 1.0
    ring = np.full((5, 5), 1.0 / 16.0, np.float32)  # hole detector on pooled ink map
    ring[1:4, 1:4] = -1.0 / 9.0                      # +border, -interior
    conv2_b = np.zeros((16,), dtype=np.float32)
    for k in (14, 15):
        conv2_w[k, 0, :, :] = ring
        conv2_b[k] = -0.20                    # strict threshold -> only real holes fire

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
        for k in range(14):                   # ink part
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
        for k in (14, 15):                     # hole part
            for R in range(4):
                for C in range(4):
                    v[k * 16 + R * 4 + C] = scale_hole * (H[d][R, C] - Hbar[R, C])
        fc_w[d] = v

    fc_b = np.array([1.756, -1.128, 0.397, -0.282, -2.098,
                     1.605, 1.172, 1.899, 1.030, -0.704], dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
