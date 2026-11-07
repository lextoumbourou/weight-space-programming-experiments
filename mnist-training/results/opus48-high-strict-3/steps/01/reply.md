## Step 1

My plan: build an explicit coarse-template matcher.

- **conv1**: all 8 filters are a 5×5 averaging (blur) kernel. Since the input is non-negative, ReLU passes everything, and after max-pool I get an 8×12×12 map where channel 0 is essentially a coarse "ink-density" image of the digit (all channels identical).
- **conv2**: each of the 16 output channels is a single delta (a 1 at position `(ro,co)` of its 5×5 window) reading only input-channel 0. This just samples the 12×12 ink map at 16 different sub-offsets, so after ReLU + max-pool the 16×4×4 = 256 features are a resampled version of the coarse ink image.
- **fc**: I hand-draw a 12×12 ink template for each digit, mean-center it, and place its value into each of the 256 features according to which image location that feature samples. So each logit ≈ correlation of the input with a digit template.

I start with a modest scale and will tune it from the loss/confusion feedback.

```python
import numpy as np

# 12x12 hand-drawn ink templates for each digit (row 0 = top). '#' = ink.
TEMPLATES = {
    0: ["............",
        "...#####....",
        "..##...##...",
        "..#.....#...",
        "..#.....#...",
        "..#.....#...",
        "..#.....#...",
        "..#.....#...",
        "..##...##...",
        "...#####....",
        "............",
        "............"],
    1: ["............",
        ".....##.....",
        "....###.....",
        "...#.##.....",
        ".....##.....",
        ".....##.....",
        ".....##.....",
        ".....##.....",
        ".....##.....",
        "...######...",
        "............",
        "............"],
    2: ["............",
        "...#####....",
        "..##...##...",
        ".......##...",
        "......##....",
        ".....##.....",
        "....##......",
        "...##.......",
        "..##........",
        "..########..",
        "............",
        "............"],
    3: ["............",
        "..######....",
        ".......##...",
        ".......##...",
        "....###.....",
        "....###.....",
        ".......##...",
        ".......##...",
        "..##...##...",
        "...#####....",
        "............",
        "............"],
    4: ["............",
        ".....###....",
        "....#.##....",
        "...#..##....",
        "..#...##....",
        "..########..",
        "......##....",
        "......##....",
        "......##....",
        "......##....",
        "............",
        "............"],
    5: ["............",
        "..#######...",
        "..##........",
        "..##........",
        "..#####.....",
        ".......##...",
        ".......##...",
        ".......##...",
        "..##..##....",
        "...####.....",
        "............",
        "............"],
    6: ["............",
        "....####....",
        "...##.......",
        "..##........",
        "..##........",
        "..######....",
        "..##...##...",
        "..#.....#...",
        "..##...##...",
        "...#####....",
        "............",
        "............"],
    7: ["............",
        "..########..",
        ".......##...",
        "......##....",
        "......##....",
        ".....##.....",
        ".....##.....",
        "....##......",
        "....##......",
        "....##......",
        "............",
        "............"],
    8: ["............",
        "...#####....",
        "..##...##...",
        "..##...##...",
        "...#####....",
        "...#####....",
        "..##...##...",
        "..##...##...",
        "..##...##...",
        "...#####....",
        "............",
        "............"],
    9: ["............",
        "...#####....",
        "..##...##...",
        "..#.....#...",
        "..##...##...",
        "...######...",
        ".......##...",
        "......##....",
        ".....##.....",
        "...###......",
        "............",
        "............"],
}


def build_weights():
    scale = 0.3  # overall logit scale (tune from loss feedback)

    # ---- conv1: 8 identical 5x5 averaging (blur) kernels ----
    conv1_w = np.full((8, 1, 5, 5), 1.0 / 25.0, dtype=np.float32)
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---- conv2: 16 delta kernels, each reads input channel 0 at a sub-offset ----
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for c in range(16):
        ro = c // 4          # row offset 0..3
        co = c % 4           # col offset 0..3
        conv2_w[c, 0, ro, co] = 1.0
    conv2_b = np.zeros((16,), dtype=np.float32)

    # Build 12x12 mean-centered templates
    T = {}
    for d, rows in TEMPLATES.items():
        g = np.array([[1.0 if ch == '#' else 0.0 for ch in row] for row in rows],
                     dtype=np.float32)
        T[d] = g - g.mean()

    # ---- fc: map each of 256 features to the image location it samples ----
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        for c in range(16):
            ro = c // 4
            co = c % 4
            for u in range(4):
                for v in range(4):
                    idx = c * 16 + u * 4 + v
                    r = min(ro + 2 * u, 11)   # sampled image row in 12x12 map
                    col = min(co + 2 * v, 11) # sampled image col
                    fc_w[d, idx] = scale * T[d][r, col]
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
