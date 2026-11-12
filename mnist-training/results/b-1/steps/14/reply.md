## Step 14: widen the templates to realistic digit widths

**What step 13 showed.** Aligning each template by its centre of mass helped clearly: ink-only accuracy went from 43.7% to 50.7%, and 7 is now recognised well (833 correct). The main remaining problem is that "0" attracts digits with loops or round parts: 9→0, 6→0 and 2→0.

**Diagnosis.** My strokes are drawn too narrow. MNIST scales each digit so its longer side is 20 px, and for most digits that is the height. Typical widths are about 15–17 px for 0 and 2, about 14 for 3 to 7, and about 12–14 for 8 and 9. My drawings are only 9–13 px wide, with 8 and 9 the narrowest. So the widest template, "0", came closest to wide real digits, and my 9 and 8 templates were far too thin.

**Changes in this step:**
- **Horizontal stretch per digit.** Each digit's strokes are scaled horizontally about x = 14 by a factor of 1.0 for "1", 1.15 for 2, 3, 5, 6 and 7, 1.2 for 4, 1.25 for 0, and 1.3 for 8 and 9.
- **Then centre of mass.** After stretching, the strokes are re-centred by centre of mass, as in step 13.
- **Slightly larger feature scale.** k goes from 2.0 to 2.3, reducing the advantage of large-mass templates on bold digits.
- **Features unchanged.** The fc still uses only the ink grid.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    Y, X = np.meshgrid(off, off, indexing='ij')
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
    for k in range(4):                                   # 0-3 orientation density (unused in fc)
        chan_src[k] = (k, 2, 2)
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3), (2, 1), (2, 3), (1, 2), (3, 2)]
    for i, (ky, kx) in enumerate(ink_taps):              # 4-12 ink density at 9 shifts
        chan_src[4 + i] = (4, ky, kx)
    for ch, (src, ky, kx) in chan_src.items():
        W2[ch, src, ky - 1:ky + 2, kx - 1:kx + 2] = avg

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
    # horizontal stretch so widths match typical MNIST digit widths
    xscale = {0: 1.25, 1: 1.0, 2: 1.15, 3: 1.15, 4: 1.2, 5: 1.15, 6: 1.15, 7: 1.15, 8: 1.3, 9: 1.3}

    def sample(strokes):
        pts, steps = [], []
        for poly in strokes:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.25))
                for j in range(n):
                    t = (j + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
                    steps.append(L / n)
        return np.array(pts), np.array(steps)

    def box(t, h, soft):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- ink templates (channels 4-12) ----------------
    COM = 13.8
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        sx = xscale[dgt]
        strokes = [[(14 + (x - 14) * sx, y) for (x, y) in poly] for poly in strokes]
        P, S = sample(strokes)
        com = (P * S[:, None]).sum(0) / S.sum()
        P = P - com + COM                       # centre of mass alignment (as MNIST)
        for ch in range(4, 13):
            src, ky, kx = chan_src[ch]
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    K = box(P[:, 0] - cx, 3.0, 1.5) * box(P[:, 1] - cy, 3.0, 1.5)
                    T[dgt, ch, r, c] = np.sum(S * K) / 36.0 * 2.5

    # ---------------- fc: nearest template, magnitude factor k ----------------
    k = 2.3
    s = 1.0
    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    for dgt in range(10):
        t = T[dgt]
        Wfc[dgt] = s * k * t
        bfc[dgt] = -s * 0.5 * k * k * np.sum(t ** 2)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.reshape(10, 256).astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
