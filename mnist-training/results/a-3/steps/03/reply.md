## Step 3: replace line detectors with polarity-aware edge detectors

**What went wrong in steps 1 and 2:** accuracy stayed at about 60%. I think a big cause is the conv1 line detectors. Their negative flanks sit 2 px from the centre, so a bold stroke (4–5 px wide) gives almost no response. Bold digits lose most of their orientation features.

**What changes in this step:**
- **conv1:** all 8 channels become oriented edge detectors, one per gradient direction at 0°, 45°, …, 315°.
  - Each is a smoothed directional derivative: positive on the side where ink lies, negative on the background side.
  - They respond to stroke boundaries, so thick and thin strokes both produce features.
  - The polarity tells inside from outside. For example, the inner and outer edges of a loop point in opposite directions.
- **conv2:** channels 0–7 pass the 8 edge maps through with a small blur, as before. Channels 8–15 are unused for now.
- **fc templates:** for each hand-drawn stroke point, the code assigns the two stroke edges. The edge at p + 1.5·n has its gradient pointing along −n, and the edge at p − 1.5·n has it pointing along +n.
  - Each edge is matched to the edge channels with a cos² tuning and placed in the 4×4 grid.
- **Scoring:** the same naive-Bayes-style log-odds scoring as step 2.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors ----------------
    # channel k responds where ink INCREASES along direction alpha_k (x=col right, y=row down)
    alphas = [k * 45.0 for k in range(8)]
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    for k, al in enumerate(alphas):
        a = math.radians(al)
        gx, gy = math.cos(a), math.sin(a)
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                t = dx * gx + dy * gy          # coordinate across the edge
                s = -dx * gy + dy * gx         # coordinate along the edge
                w[r, c] = t * math.exp(-t * t / (2 * 1.0 ** 2)) * math.exp(-s * s / (2 * 1.5 ** 2))
        w /= w[w > 0].sum()                    # ideal step edge -> response ~1
        W1[k, 0] = w
        b1[k] = -0.15

    # ---------------- conv2: pass-through of the 8 edge maps with small blur ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(8):
        W2[j, j, 1:4, 1:4] = K
    # channels 8-15 unused

    # ---------------- fc: stroke templates ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    digits = {
        0: [(1.0, ellipse(10, 10, 6.5, 9.5))],
        1: [(1.0, [(11, 0.5), (9, 19.5)]),
            (0.6, [(14, 0.5), (6, 19.5)])],
        2: [(1.0, [(4, 5), (6, 1.5), (10, 0.5), (14, 1.5), (16, 5), (15, 9), (10, 14), (4, 19.5),
                   (10, 19.5), (17, 19.5)])],
        3: [(1.0, [(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
                   (15, 18), (11, 19.8), (4, 18.5)])],
        4: [(0.8, [(7, 0.5), (5, 7), (4, 12.5), (10, 12.5), (17, 12)]),
            (0.6, [(12, 0.5), (8, 6), (4, 12.5)]),
            (1.0, [(14, 2), (14, 8), (13.5, 19.5)])],
        5: [(1.0, [(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
                   (11, 19.8), (4, 18.5)])],
        6: [(1.0, [(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
                   (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)])],
        7: [(1.0, [(4, 1), (10, 0.5), (16, 0.5), (14, 6), (12, 11), (10, 19.5)]),
            (0.5, [(16, 0.5), (11, 10), (8, 19.5)])],
        8: [(1.0, ellipse(10, 5, 5, 4.7)), (1.0, ellipse(10, 14.7, 6, 5))],
        9: [(1.0, ellipse(10, 5.5, 5.5, 5)), (1.0, [(15.5, 5.5), (15, 11), (14, 19.5)]),
            (0.5, [(15.5, 5.5), (13, 12), (10, 19.5)])],
    }

    centers = [4 * r + 7.5 for r in range(4)]
    sig = 2.5
    NF = 8
    h = 1.5                                   # half stroke width (edge offset from centre line)
    alr = [math.radians(al) for al in alphas]
    T = np.zeros((10, NF, 4, 4))
    for d, strokes in digits.items():
        acc = np.zeros((NF, 4, 4))
        for wgt, poly in strokes:
            for (u0, v0), (u1, v1) in zip(poly[:-1], poly[1:]):
                x0, y0, x1, y1 = u0 + 4, v0 + 4, u1 + 4, v1 + 4
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.5))
                ds = L / n
                phi = math.atan2(y1 - y0, x1 - x0)
                nx, ny = -math.sin(phi), math.cos(phi)
                # two edges: at p + h*n gradient points -n ; at p - h*n gradient points +n
                sides = []
                for sgn in (+1, -1):
                    beta = math.atan2(-sgn * ny, -sgn * nx)
                    tune = np.array([max(0.0, math.cos(beta - a)) ** 2 for a in alr])
                    sides.append((sgn, tune))
                for i in range(n):
                    s = (i + 0.5) / n
                    x = x0 + s * (x1 - x0); y = y0 + s * (y1 - y0)
                    for sgn, tune in sides:
                        ex, ey = x + sgn * h * nx, y + sgn * h * ny
                        mr = np.array([math.exp(-(ey - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                        mc = np.array([math.exp(-(ex - cc) ** 2 / (2 * sig ** 2)) for cc in centers])
                        m = np.outer(mr, mc) * ds * wgt
                        acc += tune[:, None, None] * m[None]
        T[d] = 1.0 - np.exp(-acc / 1.5)

    # Bernoulli naive-Bayes style scoring
    gamma = 0.3
    scale = 1.5                                 # typical value of a "present" feature
    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    for d in range(10):
        p = 0.05 + 0.9 * T[d]
        L1 = np.log(p / (1 - p))
        L0 = np.log(1 - p)
        Wfc[d, :NF * 16] = gamma * L1.reshape(-1) / scale
        bfc[d] = gamma * L0.sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
