## Step 6: graded (blurred) features instead of presence features

**Diagnosis.** Five steps have all stuck at about 50%, whatever scoring rule I used, so the features are the bottleneck. I think the cause is the ink features:
- Each final ink feature is a max over a roughly 6×6 px window of a sharp ink map.
- So it reads "1" wherever any stroke comes close.
- For a 20×20 digit that is most of the central cells, for almost every digit.
- That leaves very little to tell classes apart. Whichever template happens to cover the most cells ("8") attracts everything.

**Fix: make the features roughly linear in local ink amount.** Each feature should measure how much ink, or how much stroke of a given orientation, is near the cell, rather than whether any is present.

**conv1** keeps the four oriented line detectors and the plus-shaped ink channel. The orientation bias is reduced to −0.05.

**conv2** uses a smooth 3×3 weighted average (weights 1,2,1 by 1,2,1, divided by 16) instead of single taps:
- Channels 0–3 average the four orientation maps at the centre position.
- Channels 4–12 average the ink map at 9 shifted positions, so the ink grid is sampled about every 2 px.

Each final feature then measures local stroke density over roughly a 6×6 px window. Those values are graded, not near-binary.

**Templates** are computed analytically from my stroke drawings. For each stroke point I add its length, weighted by orientation agreement, times a soft 6×6 window around the cell centre. This gives the expected density, linear in the strokes.

**fc** uses cosine matching, `logit_d = s·f·T_d/‖T_d‖` with `s = 10`. This ignores overall stroke thickness, which varies a lot between writers.

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
        w /= w[w > 0].sum()          # aligned 2px stroke -> ~0.9
        W1[k, 0] = w
        b1[k] = -0.05
    # channel 4: ink (plus-shaped average)
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125

    # ---------------- conv2: smooth 3x3 averages -> graded density ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    avg = np.outer([1, 2, 1], [1, 2, 1]) / 16.0
    chan_src = {}   # conv2 channel -> (conv1 channel, ky, kx) ; (ky,kx)=centre of 3x3 average
    for k in range(4):
        chan_src[k] = (k, 2, 2)
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3), (2, 1), (2, 3), (1, 2), (3, 2)]
    for i, (ky, kx) in enumerate(ink_taps):
        chan_src[4 + i] = (4, ky, kx)
    for ch, (src, ky, kx) in chan_src.items():
        W2[ch, src, ky - 1:ky + 2, kx - 1:kx + 2] = avg
    # channels 13-15 unused

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

    # ---------------- templates: expected local stroke density ----------------
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
                    T[dgt, ch, r, c] = np.sum(S * o * K) / 36.0 * 2.5   # ~ ink fraction
    # ---------------- fc: cosine matching ----------------
    s = 10.0
    Wfc = np.zeros((10, 256))
    bfc = np.zeros(10)
    for dgt in range(10):
        t = T[dgt].reshape(-1)
        Wfc[dgt] = s * t / (np.linalg.norm(t) + 1e-8)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
