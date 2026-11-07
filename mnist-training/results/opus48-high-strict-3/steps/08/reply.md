## Step 8

Bias tuning has plateaued around 41% — the ceiling of plain template-correlation. Time to improve the **templates themselves** using the structure in the confusion matrix. The biggest leaks are **9→4 (558)** and **8→2 (316)**, which happen because those templates overlap the confuser's ink.

I'm introducing explicit **anti-regions** (`o` = strong negative weight) that mark "this digit should *not* have ink here, but its confuser does":
- **4**: negative at the top-left (9's closed top loop lives there; 4's top is open) → breaks 9→4.
- **2**: negative at the lower-right (8's lower loop lives there; 2 sweeps left) → breaks 8→2.
- **0**: negative in the center hole → separates 0 from 8.
- **1**: cleaned to a pure vertical + base (removed the top flag that mimicked 7's bar).

I keep the well-calibrated balanced bias and will recalibrate next step if appeals shift.

```python
import numpy as np

# '#' = +1 ink, 'o' = -1 anti-region (should be empty), '.' = neutral(0)
TEMPLATES = {
    0: ["............","...#####....","..##...##...","..#.ooo.#...","..#.ooo.#...",
        "..#.ooo.#...","..#.ooo.#...","..#.ooo.#...","..##...##...","...#####....",
        "............","............"],
    1: ["............",".....##.....",".....##.....",".....##.....",".....##.....",
        ".....##.....",".....##.....",".....##.....",".....##.....","...######...",
        "............","............"],
    2: ["............","...#####....","..##...##...",".......##...","......##....",
        ".....##.....","....##..oo..","...##...oo..","..##....oo..","..########..",
        "............","............"],
    3: ["............","..######....",".......##...",".......##...","....###.....",
        "....###.....",".......##...",".......##...","..##...##...","...#####....",
        "............","............"],
    4: ["............","...oo.##....","...o..##....","...#..##....","..#...##....",
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


def _val(ch):
    return 1.0 if ch == '#' else (-1.0 if ch == 'o' else 0.0)


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
        g = np.array([[_val(ch) for ch in r] for r in rows], dtype=np.float32)
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
