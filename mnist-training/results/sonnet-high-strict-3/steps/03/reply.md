Step 2 still predicted almost everything as 2, 5 or 8. I think there are two causes:

1. **Hole detector too small.** My conv1 ring (radius 2 px) can't see the 8–10 px hole of a 0. Class 0 never won because of this. I now detect loops in conv2 as a ring of ink-blob responses around an empty centre, at two sizes. That covers loops at roughly digit scale.
2. **Class offsets.** Features that are positive on every image give classes with more net-positive weight a head start. I now:
   - add negative conv2 biases so features are sparse and zero on background;
   - subtract half of each class/channel's mean over the 16 cells from the fc weights;
   - keep the class-mean subtraction and row normalisation, with a larger scale.

```python
import numpy as np
import math


def build_weights():
    # ---------------- conv1: 8 hand-made 5x5 filters ----------------
    w1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    rr, cc = np.meshgrid(np.arange(-2, 3), np.arange(-2, 3), indexing="ij")

    def bar(dr, dc):
        n = math.hypot(dr, dc)
        dr, dc = dr / n, dc / n
        perp = rr * dc - cc * dr
        g = np.exp(-perp ** 2 / (2 * 0.9 ** 2))
        g = g - g.mean()
        return g / g[g > 0].sum()

    w1[0, 0] = bar(1, 0)    # 0: vertical stroke
    w1[1, 0] = bar(0, 1)    # 1: horizontal stroke
    w1[2, 0] = bar(-1, 1)   # 2: "/" diagonal
    w1[3, 0] = bar(1, 1)    # 3: "\" diagonal
    g = np.exp(-(rr ** 2 + cc ** 2) / (2 * 1.3 ** 2))
    w1[4, 0] = g / g.sum()  # 4: ink blob
    colg = np.exp(-cc ** 2 / (2 * 1.5 ** 2))
    prof = np.array([-1, -1, 0, 1, 1], dtype=np.float32)[:, None] * colg
    w1[5, 0] = prof / prof[prof > 0].sum()   # 5: ink below, empty above
    w1[6, 0] = -w1[5, 0]                     # 6: ink above, empty below
    w1[7, 0] = w1[5, 0].T                    # 7: ink right, empty left (unused)

    # ---------------- conv2: 16 channels ----------------
    w2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.15, dtype=np.float32)
    r2, c2 = np.meshgrid(np.arange(-2, 3), np.arange(-2, 3), indexing="ij")
    rad2 = np.sqrt(r2 ** 2 + c2 ** 2)

    def mask(kind):
        m = np.zeros((5, 5), dtype=np.float32)
        if kind == "full":
            m[:, :] = 1
        elif kind == "top":
            m[0:3, :] = 1
        elif kind == "bot":
            m[2:5, :] = 1
        elif kind == "left":
            m[:, 0:3] = 1
        elif kind == "right":
            m[:, 2:5] = 1
        elif kind == "center":
            m[1:4, 1:4] = 1
        return 2.0 * m / m.sum()

    spec = [
        (0, 0, "full"), (1, 1, "full"), (2, 2, "full"), (3, 3, "full"),
        (4, 4, "full"), (6, 5, "full"), (7, 6, "full"),
        (8, 1, "top"), (9, 1, "bot"), (10, 0, "left"), (11, 0, "right"),
        (12, 4, "center"), (14, 2, "bot"), (15, 3, "top"),
    ]
    for o, c, k in spec:
        w2[o, c] = mask(k)

    def loop(radius):
        # ring of ink-blob responses around an empty centre
        ring = np.exp(-(rad2 - radius) ** 2 / (2 * 0.6 ** 2))
        ring = ring / ring.sum()
        cen = np.exp(-rad2 ** 2 / (2 * 0.6 ** 2))
        cen = cen / cen.sum()
        return 2.0 * (ring - 1.2 * cen)

    w2[5, 4] = loop(2.0)    # 5: large loop (like a 0 / 8 / 6 / 9 hole)
    w2[13, 4] = loop(1.2)   # 13: small loop
    b2[5] = -0.3
    b2[13] = -0.3

    # ---------------- fc ----------------
    W = np.zeros((10, 16, 4, 4), dtype=np.float32)

    def s(cls, ch, rows, cols, val):
        for r in rows:
            for c in cols:
                W[cls, ch, r, c] += val

    R = range(4)
    mid = [1, 2]
    top = [0, 1]
    bot = [2, 3]
    left = [0, 1]
    right = [2, 3]

    # 0
    s(0, 5, mid, mid, 1.5); s(0, 13, mid, mid, 0.7); s(0, 12, mid, mid, -1.0)
    s(0, 0, mid, R, 0.5); s(0, 10, R, R, 0.2); s(0, 11, R, R, 0.2)
    s(0, 1, R, R, 0.1)
    # 1
    s(1, 0, R, mid, 1.0); s(1, 1, R, R, -0.7); s(1, 5, R, R, -1.0)
    s(1, 4, R, [0, 3], -0.5); s(1, 4, R, mid, 0.3)
    # 2
    s(2, 9, bot, R, 1.0); s(2, 2, mid, R, 1.0); s(2, 8, [0], R, 0.5)
    s(2, 14, bot, R, 0.5); s(2, 5, R, R, -0.8); s(2, 0, R, R, -0.3)
    # 3
    s(3, 15, top, R, 0.7); s(3, 11, R, right, 0.7); s(3, 5, R, R, -0.8)
    s(3, 10, R, left, -0.5); s(3, 1, R, R, 0.4)
    # 4
    s(4, 0, R, right, 0.7); s(4, 1, mid, R, 0.7); s(4, 5, top, R, 0.5)
    s(4, 2, [0, 1, 2], left, 0.7); s(4, 9, [3], R, -0.5)
    # 5
    s(5, 8, [0], R, 1.0); s(5, 10, top, R, 0.7); s(5, 9, bot, R, 0.5)
    s(5, 11, bot, R, 0.5); s(5, 5, R, R, -1.0)
    # 6
    s(6, 10, [1, 2, 3], R, 0.7); s(6, 5, bot, R, 1.0); s(6, 13, bot, R, 0.7)
    s(6, 2, top, R, 0.5); s(6, 11, top, R, -0.5)
    # 7
    s(7, 8, [0, 1], R, 1.0); s(7, 2, [1, 2, 3], R, 1.0); s(7, 5, R, R, -1.0)
    s(7, 9, [3], R, -0.7); s(7, 10, R, R, -0.3)
    # 8
    s(8, 5, R, mid, 0.8); s(8, 13, R, mid, 0.8); s(8, 2, mid, R, 0.5)
    s(8, 3, mid, R, 0.5); s(8, 12, mid, mid, 0.5)
    # 9
    s(9, 5, top, R, 1.2); s(9, 13, top, R, 0.5); s(9, 5, bot, R, -0.7)
    s(9, 11, [1, 2, 3], R, 0.7); s(9, 10, bot, R, -0.5)

    # partial removal of per-channel cell mean (cancels uniform activity offsets)
    cm = W.mean(axis=(2, 3), keepdims=True)
    W = W - 0.5 * cm
    Wf = W.reshape(10, 256).astype(np.float64)
    Wf = Wf - Wf.mean(axis=0, keepdims=True)
    norms = np.sqrt((Wf ** 2).sum(axis=1, keepdims=True)) + 1e-9
    Wf = Wf / norms * 3.0
    bf = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2,
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf,
    }
```
