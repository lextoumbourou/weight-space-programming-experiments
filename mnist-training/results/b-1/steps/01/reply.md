## Step 1: a hand-built baseline

**Layer 1 (conv1).** Five of the eight filters are used.
- Channels 0 to 3 are zero-mean oriented line detectors for the four stroke directions: horizontal, vertical, "\" and "/".
- Channel 4 is a small ink-blob detector.
- Channels 5 to 7 are unused (all zeros).

**Layer 2 (conv2).** This layer only sorts and places features; it does not combine them.
- Channels 0 to 3 copy the four orientation maps, lightly smoothed over a 3×3 area. After the final pooling each one is a 4×4 map of "is there a stroke of this direction here".
- Channels 4 to 8 copy the ink map using five different single-tap offsets. This gives five shifted 4×4 grids, so ink is sampled on a finer, overlapping grid with about 2-pixel spacing.
- Channels 9 to 15 are unused.

I worked out where each pooled cell sits on the input:

- For a channel whose single tap is at kernel row `ky`, final cell `r` is centred near input row `4r + 2·ky + 3.5`. The same formula holds for columns.
- With the centre tap (`ky = 2`), the 4×4 grid spans roughly input rows and columns 4 to 23. That is the 20×20 box the digit is fitted into.

**Output layer (fc).** I describe each digit as hand-drawn polylines and ellipses in input pixel coordinates. From each description the code computes a feature-space template analytically:
- For every 4×4 cell and every channel, it adds up how much stroke of the matching orientation passes near that cell.
- That amount is turned into a "presence" value between 0 and 1.
- The fc layer then acts as a nearest-template classifier: `logit_d = s·(f·T_d − ½‖T_d‖²)`, which equals `−(s/2)·‖f − T_d‖²` plus a constant shared by all classes.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    Y, X = np.meshgrid(off, off, indexing='ij')        # Y = row offset (down), X = col offset (right)
    # orientation of the stroke direction in image coords (x right, y down)
    # 0: horizontal, 1: vertical, 2: "\" (down-right), 3: "/" (up-right)
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        d = np.abs(-math.sin(th) * X + math.cos(th) * Y)   # distance from line through centre
        g = np.exp(-d ** 2 / (2 * 0.8 ** 2))
        w = g - g.mean()                                   # zero-mean: flat ink gives ~0
        w /= w[w > 0].sum()                                # aligned 2px stroke -> ~1
        W1[k, 0] = w
        b1[k] = -0.1                                       # suppress weak responses
    # channel 4: ink blob (plus-shaped average)
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125
    # channels 5-7 unused (zero)

    # ---------------- conv2: route features to 4x4 grids ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    sm = np.outer([0.5, 1, 0.5], [0.5, 1, 0.5]) / 4.0
    for k in range(4):                                     # orientation pass-through, smoothed
        W2[k, k, 1:4, 1:4] = sm
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3)]   # shifted ink grids
    for i, (ky, kx) in enumerate(ink_taps):
        W2[4 + i, 4, ky, kx] = 1.0
    # channels 9-15 unused

    # tap position per used conv2 channel (for computing cell centres)
    chan_tap = {0: (2, 2), 1: (2, 2), 2: (2, 2), 3: (2, 2)}
    for i, t in enumerate(ink_taps):
        chan_tap[4 + i] = t

    # ---------------- digit stroke descriptions (input pixel coords x=col, y=row) ----------------
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
        8: [ellipse(14, 9, 4.5, 4.5), ellipse(14, 18.5, 5.5, 5.0)],
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

    def box(t, h, soft=0.7):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- templates in feature space ----------------
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        P, A, S = sample(strokes)
        for ch, (ky, kx) in chan_tap.items():
            if ch < 4:
                o = np.maximum(0.0, np.cos(2 * (A - thetas[ch])))   # orientation match
                h = 3.5
                scale = 0.7                                         # detectors respond < 1
            else:
                o = np.ones_like(A)
                h = 3.0
                scale = 1.0
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    acc = np.sum(S * o * box(P[:, 0] - cx, h) * box(P[:, 1] - cy, h))
                    T[dgt, ch, r, c] = scale * (1.0 - math.exp(-0.4 * acc))

    # ---------------- fc: nearest-template classifier ----------------
    s = 0.5
    Wfc = np.zeros((10, 256))
    bfc = np.zeros(10)
    for dgt in range(10):
        t = T[dgt].reshape(-1)          # (channel,row,col) flatten order matches nn.Flatten
        Wfc[dgt] = s * t
        bfc[dgt] = -0.5 * s * np.sum(t ** 2)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
