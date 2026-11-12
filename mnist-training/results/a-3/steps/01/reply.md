## Step 1: baseline hand-built network

**What this step tries:** a simple pipeline of stroke-orientation detectors followed by template matching.

- **conv1 (channels 0–3)** are 5×5 oriented line detectors at 0°, 45°, 90° and 135°. Each one has a positive ridge along the line and negative flanks, so its weights sum to zero. That way a uniform ink patch gives no response.
- **conv1 channel 4** is a plain 3×3 ink detector.
- **conv1 channels 5–7** are unused (all zeros) for now.
- **conv2 channels 0–4** pass conv1 channels 0–4 straight through, with a small 3×3 spatial blur. After the final max-pool, these give a 4×4 grid of "is orientation k present here" features. The grid cells are centred near input rows and columns 7.5, 11.5, 15.5 and 19.5.
- **conv2 channels 5–15** are unused (all zeros) for now.
- **fc** does template matching. I describe each digit by hand as polyline strokes in a 20×20 box placed in the 28×28 frame.
  - For each stroke point, the formula works out which orientation channel its direction matches and which grid cell it falls in. This gives an expected-feature template for each digit.
  - No convolution is ever applied to these templates.
  - Each template is mean-centred and normalised to unit length, then multiplied by a logit scale.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    thetas = [0.0, 45.0, 90.0, 135.0]   # 0=horizontal, 45="\", 90=vertical, 135="/" (y points down)
    for k, th in enumerate(thetas):
        t = math.radians(th)
        ux, uy = math.cos(t), math.sin(t)      # direction along the line (x=col, y=row)
        nx, ny = -math.sin(t), math.cos(t)     # normal to the line
        raw = np.zeros((5, 5)); taper = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                d = dx * nx + dy * ny          # distance across the line
                a = dx * ux + dy * uy          # distance along the line
                raw[r, c] = math.exp(-d * d / (2 * 0.9 ** 2))
                taper[r, c] = math.exp(-a * a / (2 * 2.0 ** 2))
        m = (taper * raw).sum() / taper.sum()
        w = taper * (raw - m)                  # zero-sum: ridge positive, flanks negative
        w /= w[w > 0].sum()                    # aligned full stroke -> response ~ <1
        W1[k, 0] = w
        b1[k] = -0.1                           # suppress weak responses
    # channel 4: ink detector (3x3 average)
    W1[4, 0, 1:4, 1:4] = 1.0 / 9.0
    # channels 5-7 unused (zero)

    # ---------------- conv2: pass-through with small blur ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)                       # centre 1, edges .5, corners .25
    for j in range(5):
        W2[j, j, 1:4, 1:4] = K
    # channels 5-15 unused

    # ---------------- fc: stroke-described digit templates ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    # strokes in a 20x20 box (u = col, v = row), mapped to input via +4
    digits = {
        0: [ellipse(10, 10, 6.5, 9.5)],
        1: [[(11, 0.5), (9, 19.5)]],
        2: [[(4, 5), (6, 1.5), (10, 0.5), (14, 1.5), (16, 5), (15, 9), (10, 14), (4, 19.5),
             (10, 19.5), (17, 19.5)]],
        3: [[(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
             (15, 18), (11, 19.8), (4, 18.5)]],
        4: [[(7, 0.5), (5, 7), (4, 12.5), (10, 12.5), (17, 12)],
            [(14, 2), (14, 8), (13.5, 19.5)]],
        5: [[(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
             (11, 19.8), (4, 18.5)]],
        6: [[(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
             (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)]],
        7: [[(4, 1), (10, 0.5), (16, 0.5), (14, 6), (12, 11), (10, 19.5)]],
        8: [ellipse(10, 5, 5, 4.7), ellipse(10, 14.7, 6, 5)],
        9: [ellipse(10, 5.5, 5.5, 5), [(15.5, 5.5), (15, 11), (14, 19.5)]],
    }

    centers = [4 * r + 7.5 for r in range(4)]  # input-pixel centres of the 4x4 pooled grid
    sig = 2.5
    NF = 5                                     # feature channels used (4 orientations + ink)
    T = np.zeros((10, NF, 4, 4))
    for d, strokes in digits.items():
        acc = np.zeros((NF, 4, 4))
        for poly in strokes:
            for (u0, v0), (u1, v1) in zip(poly[:-1], poly[1:]):
                x0, y0, x1, y1 = u0 + 4, v0 + 4, u1 + 4, v1 + 4
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.5))
                ds = L / n
                phi = math.atan2(y1 - y0, x1 - x0)
                orient = [max(0.0, math.cos(2 * (phi - math.radians(th)))) ** 2 for th in thetas]
                for i in range(n):
                    s = (i + 0.5) / n
                    x = x0 + s * (x1 - x0); y = y0 + s * (y1 - y0)
                    mr = np.array([math.exp(-(y - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                    mc = np.array([math.exp(-(x - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                    m = np.outer(mr, mc) * ds
                    for k in range(4):
                        acc[k] += orient[k] * m
                    acc[4] += 0.5 * m              # ink channel, down-weighted
        T[d] = 1.0 - np.exp(-acc / 1.5)            # saturating "presence" template

    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    alpha = 3.0                                    # logit scale
    for d in range(10):
        v = T[d].reshape(-1)                       # (channel, row, col) order, channels 0..4
        v = v - v.mean()
        v = v / (np.linalg.norm(v) + 1e-8)
        Wfc[d, :NF * 16] = alpha * v

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
