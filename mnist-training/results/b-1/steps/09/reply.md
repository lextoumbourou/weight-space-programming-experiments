## Step 9: add hole (closed-loop) detectors

**Why change approach.** Template matching alone has plateaued at about 50%. The step 8 confusions are mostly between digits that differ in whether they have a closed loop and where it is:
- 8, 9 and 2 are often predicted as 1.
- 2 and 5 are often predicted as 6.
- 9 is often predicted as 0.

Loops are a structural cue that holds up across positions and stroke thickness.

**What this step adds.** conv2 channels 13–15 become hole detectors that work on the pooled ink map (12×12, cells of 2 px). Each one fires when the centre cell is empty but there is ink on all four sides at a set offset:
- **ReLU threshold:** the output is `ReLU(Σ side ink − 2.6 − 2·centre ink)`.
- **Channel 13, small hole:** the four directly adjacent cells, about 2 px away. This suits the loops of 6, 8 and 9.
- **Channel 14, medium hole:** sides 2 cells away, about 4 px, averaged over 3 cells each. This suits 0.
- **Channel 15, tall narrow hole:** sides 1 cell away horizontally and 2 cells away vertically. This suits narrow 0s.

After the final max-pool, the 4×4 position of each hole tells the fc layer where it is: top half or bottom half.

**fc hole weights:**
- A small hole in the top half favours 9 and 8.
- A small hole in the bottom half favours 6 and 8.
- A medium or tall hole favours 0.
- Any hole counts against 1, 2, 3, 5 and 7.
- Classes 0, 6, 8 and 9 get a small negative bias, so they lose a little when no hole is seen.

These weights are added to the step 8 template logits, which are kept unchanged.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    Y, X = np.meshgrid(off, off, indexing='ij')
    # 0: horizontal, 1: vertical, 2: "\" (down-right), 3: "/" (up-right)
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        d = np.abs(-math.sin(th) * X + math.cos(th) * Y)
        g = np.exp(-d ** 2 / (2 * 0.8 ** 2))
        w = g - g.mean()
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.05
    # channel 4: ink (plus-shaped average)
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125

    # ---------------- conv2 ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    avg = np.outer([1, 2, 1], [1, 2, 1]) / 16.0
    chan_src = {}
    for k in range(4):                                   # 0-3 orientation density
        chan_src[k] = (k, 2, 2)
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3), (2, 1), (2, 3), (1, 2), (3, 2)]
    for i, (ky, kx) in enumerate(ink_taps):              # 4-12 ink density at 9 shifts
        chan_src[4 + i] = (4, ky, kx)
    for ch, (src, ky, kx) in chan_src.items():
        W2[ch, src, ky - 1:ky + 2, kx - 1:kx + 2] = avg

    # 13-15 hole detectors on pooled ink (conv1 channel 4)
    # ch13 small: centre empty, ink in 4 direct neighbours
    W2[13, 4, 2, 2] = -2.0
    for (yy, xx) in [(2, 1), (2, 3), (1, 2), (3, 2)]:
        W2[13, 4, yy, xx] += 1.0
    b2[13] = -2.6
    # ch14 medium: sides 2 cells away, 3 cells per side
    W2[14, 4, 2, 2] = -2.0
    for d in (-1, 0, 1):
        W2[14, 4, 2 + d, 0] += 1 / 3.0
        W2[14, 4, 2 + d, 4] += 1 / 3.0
        W2[14, 4, 0, 2 + d] += 1 / 3.0
        W2[14, 4, 4, 2 + d] += 1 / 3.0
    b2[14] = -2.6
    # ch15 tall narrow: left/right 1 cell away, top/bottom 2 cells away
    W2[15, 4, 2, 2] = -2.0
    W2[15, 4, 1, 2] -= 0.5      # interior should also be empty just above/below centre
    W2[15, 4, 3, 2] -= 0.5
    for d in (-1, 0, 1):
        W2[15, 4, 2 + d, 1] += 1 / 3.0
        W2[15, 4, 2 + d, 3] += 1 / 3.0
    W2[15, 4, 0, 2] += 1.0
    W2[15, 4, 4, 2] += 1.0
    b2[15] = -2.6

    # ---------------- digit strokes (x=col, y=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        t = np.linspace(0, 2 * math.pi, n + 1)
        return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in t]

    digits = {
        0: [ellipse(14, 14, 6.0, 9.5)],
        1: [[(16, 4.5), (12, 23.5)]],
        2: [[(8, 9), (10, 6), (14, 4.5), (18, 5.5), (20, 9), (18, 13), (13, 18), (8, 23), (14, 23), (21, 23)]],
        3: [[(8, 6), (12, 4.5), (17, 5), (19, 8), (17, 12), (12, 13.5), (17, 15), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        4: [[(11, 4.5), (8, 16), (21, 16)], [(18, 8), (18, 23.5)]],
        5: [[(20, 4.5), (10, 4.5), (9, 13), (14, 12), (19, 14), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        6: [[(17, 4.5), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23.5), (18, 21), (19, 17), (16, 14), (12, 14), (9, 17)]],
        7: [[(8, 5), (20, 5), (17, 11), (14, 17), (12, 23.5)]],
        8: [ellipse(14, 9, 4.0, 4.3), ellipse(14, 18.5, 4.8, 5.0)],
        9: [ellipse(14, 9.5, 5.5, 5.0), [(19, 10), (18, 17), (16, 23.5)]],
    }

    def sample(strokes):
        pts, angs, steps = [], [], []
        for poly in strokes:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.25))
                phi = math.atan2(y1 - y0, x1 - x0)
                for j in range(n):
                    t = (j + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
                    angs.append(phi)
                    steps.append(L / n)
        return np.array(pts), np.array(angs), np.array(steps)

    def box(t, h, soft):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- templates (channels 0-12) ----------------
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        P, A, S = sample(strokes)
        for ch, (src, ky, kx) in chan_src.items():
            if src < 4:
                o = np.maximum(0.0, np.cos(2 * (A - thetas[src])))
            else:
                o = np.ones_like(A)
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    K = box(P[:, 0] - cx, 3.0, 0.8) * box(P[:, 1] - cy, 3.0, 0.8)
                    T[dgt, ch, r, c] = np.sum(S * o * K) / 36.0 * 2.5

    # ---------------- fc part 1: projected templates (scale invariant) ----------------
    s = 3.0
    Tf = T.reshape(10, -1)
    mu = Tf.mean(axis=0)
    mm = np.dot(mu, mu)
    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    for dgt in range(10):
        w = Tf[dgt] - (np.dot(Tf[dgt], mu) / mm) * mu
        w = w / (np.linalg.norm(w) + 1e-8)
        Wfc[dgt] = (s * w).reshape(16, 4, 4)
    Wfc[:, 13:16] = 0.0

    # ---------------- fc part 2: hole rules ----------------
    small_top = {9: 2.0, 8: 1.5, 0: 0.3, 4: 0.3, 6: -1.0}
    small_bot = {6: 2.0, 8: 1.5, 0: 0.3, 9: -1.0, 2: -0.5}
    big = {0: 2.0, 8: 0.5, 6: 0.5, 9: 0.5, 4: 0.0}
    for dgt in range(10):
        Wfc[dgt, 13, 0:2, :] = small_top.get(dgt, -1.5)
        Wfc[dgt, 13, 2:4, :] = small_bot.get(dgt, -1.5)
        Wfc[dgt, 14, :, :] = big.get(dgt, -1.0)
        Wfc[dgt, 15, :, :] = big.get(dgt, -1.0)
    for dgt in (0, 6, 8, 9):
        bfc[dgt] -= 0.4

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.reshape(10, 256).astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
