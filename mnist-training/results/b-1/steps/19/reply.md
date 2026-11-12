## Step 19: add hole detectors that fire only on exact fits

**Where things stand.** Calibrating the class offsets brought the best result so far: 67.3% accuracy, loss 1.10. The remaining large confusions are mostly between digits that differ in their closed loops:

| Confusion | Count |
|---|---|
| 5→8 | 258 |
| 8→3 | 230 |
| 8→2 | 194 |
| 4→9 | 178 |
| 5→3 / 3→5 | 139 / 175 |
| 7→9 | 128 |
| 0→8 | 123 |

8 has two holes and 9 a top hole, while 4 is usually open. 0 has one large hole, and 6 a bottom hole. Ink-density templates cannot see this.

**Why the step 9 detectors failed.** They used the dilated ink map and lenient sums. Thick open strokes could make up for a missing wall, so 3s and 5s fired as holes.

**The new design:**
- **conv1 channel 5:** a raw single-pixel ink channel. After max-pooling, each 2 px cell has a value of at most 1.
- **conv2 hole detectors:** a wall cell can then contribute at most 1. Each detector puts a fixed number of wall cells on every side. A missing wall cannot be compensated, and any ink inside the hole kills the response.

There are three detectors:

| Channel | Shape | Interior (2 px cells) |
|---|---|---|
| 13 (A) | 1-cell hole | One empty cell, with ink in its 4 direct neighbours |
| 14 (B) | 2×2-cell hole | Four empty cells, with 2 wall cells per side |
| 15 (E) | Tall hole, aimed at 0 | 3 cells tall by 2 wide, with walls all round |

All three have a bias of −3.2. So they fire, with a value up to about 0.8, only when all four walls are present.

**fc weights for holes.** Weights are about half the strength of step 9:
- A or B in the top half favours 9 and 8.
- A or B in the bottom half favours 6 and 8.
- The tall hole favours 0.
- Any hole counts against the open digits.

The cosine template part and the calibrated offsets are kept from step 18. I expect to recalibrate the offsets in the next step.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1 ----------------
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
    # channel 4: ink (plus-shaped average) -> density features
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125
    # channel 5: raw pixel ink (centre tap) -> hole detection, pooled cell value <= 1
    W1[5, 0, 2, 2] = 1.0

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

    # 13 (A): 1-cell hole. centre empty, 4 direct neighbours inked.
    W2[13, 5, 2, 2] = -3.0
    for (yy, xx) in [(2, 1), (2, 3), (1, 2), (3, 2)]:
        W2[13, 5, yy, xx] = 1.0
    b2[13] = -3.2
    # 14 (B): 2x2-cell hole at rows 2-3, cols 2-3; walls of 2 cells per side (0.5 each)
    for yy in (2, 3):
        for xx in (2, 3):
            W2[14, 5, yy, xx] = -1.5
    for yy in (2, 3):
        W2[14, 5, yy, 1] = 0.5
        W2[14, 5, yy, 4] = 0.5
    for xx in (2, 3):
        W2[14, 5, 1, xx] = 0.5
        W2[14, 5, 4, xx] = 0.5
    b2[14] = -3.2
    # 15 (E): tall hole rows 1-3, cols 1-2; walls: left col 0, right col 3 (1/3 each),
    #         top row 0, bottom row 4 (0.5 each)
    for yy in (1, 2, 3):
        for xx in (1, 2):
            W2[15, 5, yy, xx] = -1.0
        W2[15, 5, yy, 0] = 1 / 3.0
        W2[15, 5, yy, 3] = 1 / 3.0
    for xx in (1, 2):
        W2[15, 5, 0, xx] = 0.5
        W2[15, 5, 4, xx] = 0.5
    b2[15] = -3.2

    # ---------------- digit strokes (x=col, y=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        t = np.linspace(0, 2 * math.pi, n + 1)
        return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in t]

    digits = {
        0: [ellipse(14, 14, 6.0, 9.5)],
        1: [[(16, 4.5), (12, 23.5)]],
        2: [[(8, 9), (10, 6), (14, 4.5), (18, 5.5), (20, 9), (18, 13), (13, 18), (8, 23), (14, 23), (21, 23)]],
        3: [[(8, 6), (12, 4.5), (17, 5), (19, 8), (17, 12), (12, 13.5), (17, 15), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        4: [[(10, 4.5), (8, 15), (20, 15)], [(17, 6), (17, 23.5)]],
        5: [[(20, 4.5), (10, 4.5), (9, 13), (14, 12), (19, 14), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        6: [[(17, 4.5), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23.5), (18, 21), (19, 17), (16, 14), (12, 14), (9, 17)]],
        7: [[(8, 5), (20, 5), (14, 23.5)]],
        8: [ellipse(14.5, 8.5, 4.0, 4.0), ellipse(13.5, 18.5, 5.0, 5.0)],
        9: [ellipse(14, 9, 4.5, 4.5), [(18.5, 10), (15, 23.5)]],
    }
    xscale = {0: 1.25, 1: 1.0, 2: 1.15, 3: 1.15, 4: 1.2, 5: 1.15, 6: 1.15, 7: 1.15, 8: 1.3, 9: 1.3}

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

    # ---------------- templates (orientation 0-3, ink 4-12) ----------------
    COM = 13.8
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        sx = xscale[dgt]
        strokes = [[(14 + (x - 14) * sx, y) for (x, y) in poly] for poly in strokes]
        P, A, S = sample(strokes)
        com = (P * S[:, None]).sum(0) / S.sum()
        P = P - com + COM
        for ch in range(13):
            src, ky, kx = chan_src[ch]
            if src < 4:
                o = np.maximum(0.0, np.cos(2 * (A - thetas[src])))
            else:
                o = np.ones_like(A)
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    K = box(P[:, 0] - cx, 3.0, 1.5) * box(P[:, 1] - cy, 3.0, 1.5)
                    T[dgt, ch, r, c] = np.sum(S * o * K) / 36.0 * 2.5

    # ---------------- fc part 1: two-part cosine + calibrated offsets ----------------
    s = 10.0
    lam_ori = 0.5
    beta = {0: 0.0140, 1: -0.0019, 2: 0.0073, 3: 0.0075, 4: 0.0273,
            5: 0.0097, 6: -0.0110, 7: 0.0068, 8: -0.0095, 9: -0.0051}
    ink = np.zeros((16, 4, 4), dtype=bool); ink[4:13] = True
    ori = np.zeros((16, 4, 4), dtype=bool); ori[0:4] = True

    def unit(v):
        return v / (np.linalg.norm(v) + 1e-8)

    mu = T.mean(axis=0)
    mu_ink = unit(np.where(ink, mu, 0.0))
    mu_ori = unit(np.where(ori, mu, 0.0))

    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    for dgt in range(10):
        ti = unit(np.where(ink, T[dgt], 0.0))
        to = unit(np.where(ori, T[dgt], 0.0))
        b = beta[dgt]
        Wfc[dgt] = s * ((ti + b * mu_ink) + lam_ori * (to + b * mu_ori))

    # ---------------- fc part 2: hole rules (channels 13-15) ----------------
    hs = 0.5
    small_top = {9: 2.0, 8: 1.5, 4: 0.5, 0: 0.5, 6: -1.0}
    small_bot = {6: 2.0, 8: 1.5, 0: 0.5, 2: 0.3, 9: -1.0}
    tall = {0: 2.0, 6: 0.5, 9: 0.5, 8: 0.0, 4: 0.0}
    for dgt in range(10):
        for ch in (13, 14):
            Wfc[dgt, ch, 0:2, :] = hs * small_top.get(dgt, -1.0)
            Wfc[dgt, ch, 2:4, :] = hs * small_bot.get(dgt, -1.0)
        Wfc[dgt, 15, :, :] = hs * tall.get(dgt, -1.0)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.reshape(10, 256).astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
