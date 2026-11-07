## Step 2

The result collapsed almost everything onto digits **8** and **4** (the densest templates). That's the classic problem: an un-normalized dense template always wins the dot product because it simply overlaps more ink. Mean-centering alone wasn't enough.

Fix: make every template **zero-mean and unit L2 norm**, so each class competes on *shape similarity* (cosine-like) rather than raw ink coverage. I also drop the scale to a level where, by my magnitude estimate, the correct-class logit leads by ~1–2 (reasonable softmax separation instead of overconfident garbage).

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


def build_weights():
    scale = 2.0  # logit scale on unit-norm templates (tune from feedback)

    # conv1: 8 identical 5x5 averaging/blur kernels
    conv1_w = np.full((8, 1, 5, 5), 1.0 / 25.0, dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)

    # conv2: 16 delta kernels sampling input channel 0 at 16 sub-offsets
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for c in range(16):
        conv2_w[c, 0, c // 4, c % 4] = 1.0
    conv2_b = np.zeros((16,), dtype=np.float32)

    # zero-mean, unit-norm templates
    T = {}
    for d, rows in TEMPLATES.items():
        g = np.array([[1.0 if ch == '#' else 0.0 for ch in r] for r in rows],
                     dtype=np.float32)
        g = g - g.mean()
        n = np.linalg.norm(g)
        T[d] = g / n if n > 0 else g

    # fc: scatter each template onto the 256 features by sampled location
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        for c in range(16):
            ro, co = c // 4, c % 4
            for u in range(4):
                for v in range(4):
                    idx = c * 16 + u * 4 + v
                    r = min(ro + 2 * u, 11)
                    col = min(co + 2 * v, 11)
                    fc_w[d, idx] = scale * T[d][r, col]
    fc_b = np.zeros((10,), dtype=np.float32)

    return {
        "conv1.weight": conv1_w, "conv1.bias": conv1_b,
        "conv2.weight": conv2_w, "conv2.bias": conv2_b,
        "fc.weight": fc_w, "fc.bias": fc_b,
    }
```
