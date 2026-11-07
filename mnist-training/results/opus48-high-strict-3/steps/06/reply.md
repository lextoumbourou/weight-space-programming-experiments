## Step 6

The bias control **over-corrected**: digit 5 shot up to 2938 predictions and digit 8 collapsed to 45. Because the base classifier is weak, many images sit near decision boundaries, so bias shifts move large blocks at once (winner-take-all is unstable).

I'll keep the same feature/template weights and just **recalibrate the bias** using accumulated feedback from both steps, damping the two biggest swings (pull 5 back down, bring 8 back up without overshooting). Goal: predicted counts closer to ~1000 each.

```python
import numpy as np

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

# hand-tuned, damped rebalancing bias (from step4 & step5 prediction counts)
BIAS = np.array([0.80, -0.22, 0.74, 0.70, -0.27, 0.95, 0.37, 0.18, -0.10, 0.14],
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
