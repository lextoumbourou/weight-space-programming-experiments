## Step 15 (final)

The temperature test was conclusive: scaling logits **down** (t=0.7) *raised* loss (1.834→1.893) while accuracy stayed exactly at 41.75% — confirming temperature-invariance of accuracy and that my predictions are slightly **under**confident. So loss is minimized by sharpening (t>1).

For the final network I use my best-accuracy config (the step-10 optimum, locked at 41.75%) with a modest temperature increase (t=1.3) to lower the cross-entropy without risking overshoot. Accuracy stays at its best; loss should dip below 1.834.

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

BIAS = np.array([0.89, -0.17, 0.78, 0.63, -0.34, 0.92, 0.28, 0.25, -0.30, 0.09],
                dtype=np.float32)

TEMP = 1.3  # sharpen logits to reduce loss (accuracy unchanged)


def build_weights():
    scale = 2.0 * TEMP

    # conv1: sharp center-delta -> crisp downsample
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    for k in range(8):
        conv1_w[k, 0, 2, 2] = 1.0
    conv1_b = np.zeros((8,), dtype=np.float32)

    # conv2: 16 delta kernels sampling input channel 0 at 16 sub-offsets
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for c in range(16):
        conv2_w[c, 0, c // 4, c % 4] = 1.0
    conv2_b = np.zeros((16,), dtype=np.float32)

    # zero-mean, unit-norm digit templates
    T = {}
    for d, rows in TEMPLATES.items():
        g = np.array([[1.0 if ch == '#' else 0.0 for ch in r] for r in rows],
                     dtype=np.float32)
        g = g - g.mean()
        n = np.linalg.norm(g)
        T[d] = g / n if n > 0 else g

    # per-position sampling multiplicity (equal-weight correlation)
    cnt = np.zeros((12, 12), dtype=np.float32)
    for c in range(16):
        ro, co = c // 4, c % 4
        for u in range(4):
            for v in range(4):
                cnt[min(ro + 2 * u, 11), min(co + 2 * v, 11)] += 1.0
    cnt[cnt == 0] = 1.0

    # fc: scatter templates onto 256 features, normalized by multiplicity
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

    fc_b = (BIAS * TEMP).astype(np.float32)

    return {
        "conv1.weight": conv1_w, "conv1.bias": conv1_b,
        "conv2.weight": conv2_w, "conv2.bias": conv2_b,
        "fc.weight": fc_w, "fc.bias": fc_b,
    }
```
