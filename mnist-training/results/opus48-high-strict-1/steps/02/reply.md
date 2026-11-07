## Step 2

Step 1 collapsed to a few classes — 4×4 ink is too coarse and under-discriminative. I'm making a big structural change to get **much higher effective resolution** into the fully-connected layer:

- **conv1**: channel 0 is still a 5×5 average → a 12×12 ink-density map after pooling.
- **conv2**: each of the 16 output channels is a **single-pixel ("delta") filter at a different offset** `(a,b)`, so channel `k` samples the ink map at a shifted position. After the final 2×2 max-pool, the 16 channels together sample the 12×12 ink map at ~100 distinct locations.
- **fc**: I hand-draw a 12×12 ink bitmap for each digit (drawn directly from strokes), mean-centre across digits, and place each template value at the fc weight for the channel/cell that reads that location. This makes the network a ~12×12 template matcher.

```python
import numpy as np

def build_weights():
    # ---------- conv1: channel 0 = 5x5 average -> 12x12 ink-density map ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, :, :] = 1.0 / 25.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---------- conv2: 16 delta filters at different offsets (a,b) ----------
    # channel k reads ink map shifted by (a_k, b_k); a_k=1+k//4, b_k=1+k%4 -> 1..4
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(16):
        a = 1 + k // 4
        b = 1 + k % 4
        conv2_w[k, 0, a, b] = 1.0   # pick a single location of the ink map
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

    # mean-centre templates across digits so shared ink cancels (keep shape)
    Tc = IMG - IMG.mean(axis=0, keepdims=True)

    # ---------- fc: route each template value to the channel/cell that reads it ----------
    scale = 2.5
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        for k in range(16):
            a = 1 + k // 4
            b = 1 + k % 4
            for R in range(4):
                for C in range(4):
                    p = 2 * R + a   # inkmap row sampled
                    q = 2 * C + b   # inkmap col sampled
                    idx = k * 16 + R * 4 + C
                    fc_w[d, idx] = scale * Tc[d, p, q]
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
