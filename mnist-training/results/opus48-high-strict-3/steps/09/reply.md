## Step 9

The anti-regions backfired badly (41.6%→35.3%): penalizing the center of **0**, lower-right of **2**, and top-left of **4** destroyed those digits' own recall (0: 707→232, 2: 565→156, 4: 401→177). The *only* clear win was 9 (182→419, and 9→4 collapsed) — but that same change gutted 4.

Lesson: aggressive negative regions hurt self-recall more than they help. I'm **reverting to the original templates** that reached 41.6%, combined with the properly balanced bias I calibrated from step-7's prediction frequencies. This should recover ~42% and give a clean baseline before making smaller, safer tweaks.

```python
import numpy as np

# original (recall-preserving) templates
TEMPLATES = {
    0: ["............","...#####....","..##...##...","..#.....#...","..#.....#...",
        "..#.....#...","..#.....#...","..#.....#...","..##...##...","...#####....",
        "............","............"],
    1: ["............",".....##.....","....###.....","...#.##.....",".....##.....",
        ".....##.....",".....##.....",".....##.....",".....##.....","...######...",
        "............","............"],
    2: ["............","...#####....","..##...##...",".......##...","......##....",
        ".....##.....","....##......","...##.......","..##........","..########..",
        "............","............"],
    3: ["............","..######....",".......##...",".......##...","....###.....",
        "....###.....",".......##...",".......##...","..##...##...","...#####....",
        "............","............"],
    4: ["............",".....###....","....#.##....","...#..##....","..#...##....",
        "..########..","......##....","......##....","......##....","......##....",
        "............","............"],
    5: ["............","..#######...","..##........","..##........","..#####.....",
        ".......##...",".......##...",".......##...","..##..##....","...####.....",
        "............","............"],
    6: ["............","....####....","...##.......","..##........","..##........",
        "..######....","..##...##...","..#.....#...","..##...##...","...#####....",
        "............","............"],
    7: ["............","..########..",".......##...","......##....","......##....",
        ".....##.....",".....##.....","....##......","....##......","....##......",
        "............","............"],
    8: ["............","...#####....","..##...##...","..##...##...","...#####....",
        "...#####....","..##...##...","..##...##...","..##...##...","...#####....",
        "............","............"],
    9: ["............","...#####....","..##...##...","..#.....#...","..##...##...",
        "...######...",".......##...","......##....",".....##.....","...###......",
        "............","............"],
}

BIAS = np.array([0.89, -0.07, 0.70, 0.63, -0.24, 0.87, 0.28, 0.18, -0.22, 0.04],
                dtype=np.float32)


def build_weights():
    scale = 2.0

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    for k in range(8):
        conv1_w[k, 0, 2, 2] = 1.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for c in range(16):
        conv2_w[c, 0, c // 4, c % 4] = 1.0
    conv2_b = np.zeros((16,), dtype=np.float32)

    T = {}
    for d, rows in TEMPLATES.items():
        g = np.array([[1.0 if ch == '#' else 0.0 for ch in r] for r in rows],
                     dtype=np.float32)
        g = g - g.mean()
        n = np.linalg.norm(g)
        T[d] = g / n if n > 0 else g

    cnt = np.zeros((12, 12), dtype=np.float32)
    for c in range(16):
        ro, co = c // 4, c % 4
        for u in range(4):
            for v in range(4):
                cnt[min(ro + 2 * u, 11), min(co + 2 * v, 11)] += 1.0
    cnt[cnt == 0] = 1.0

    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        for c in range(16):
            ro, co = c // 4, c % 4
            for u in range(4):
                for v in range(4):
                    idx = c * 16 + u * 4 + v
                    r = min(ro + 2 * u, 11)
                    col = min(co + 2 * v, 11)
                    fc_w[d, idx] = scale * T[d][r, col] / cnt[r, col]

    fc_b = BIAS.copy()

    return {
        "conv1.weight": conv1_w, "conv1.bias": conv1_b,
        "conv2.weight": conv2_w, "conv2.bias": conv2_b,
        "fc.weight": fc_w, "fc.bias": fc_b,
    }
```
