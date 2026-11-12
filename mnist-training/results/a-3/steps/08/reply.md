## Step 8: add a second, shifted edge grid using the unused conv2 channels

**Where step 7 landed:** the class biases and smaller ε lifted accuracy to 72.9%. The main remaining confusions are 2→4 and 2→8, 3→5 and 3→8, 7→9, and 8→1. Many of these depend on exactly where an edge sits.

**What changes in this step:**
- **conv2 channels 8–15 copy the 8 edge maps again.** They use the same blur, moved one tap down and right. This shifts their 4×4 output grid by +2 input pixels in both row and column, so cells are centred at 9.5, 13.5, 17.5 and 21.5 instead of 7.5, 11.5, 15.5 and 19.5. Together the two grids sample edge positions twice as densely.
- **The fc layer is now 256 features.** I build templates for both grids from the same strokes, each with its own cell centres. The multinomial naive-Bayes scoring now uses all 256 features.
- **γ drops from 0.2 to 0.12**, because doubling the features roughly doubles the logits.
- **Class biases.** I keep last step's bias and add half of a further correction from step 7's predicted/true ratios. These stand now at: 1, 8 and 9 pulled down; 2, 3 and 5 pushed up.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors ----------------
    alphas = [k * 45.0 for k in range(8)]   # direction in which ink increases (x right, y down)
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    for k, al in enumerate(alphas):
        a = math.radians(al)
        gx, gy = math.cos(a), math.sin(a)
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                t = dx * gx + dy * gy
                s = -dx * gy + dy * gx
                w[r, c] = t * math.exp(-t * t / 2.0) * math.exp(-s * s / (2 * 1.5 ** 2))
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15

    # ---------------- conv2 ----------------
    # ch 0-7 : edge map j, 3x3 blur at taps 1..3  -> grid centres 4r+7.5
    # ch 8-15: edge map j, 3x3 blur at taps 2..4  -> grid shifted by +2 px (centres 4r+9.5)
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(8):
        W2[j, j, 1:4, 1:4] = K
        W2[8 + j, j, 2:5, 2:5] = K

    # ---------------- stroke skeletons (20x20 box: u=col, v=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48, tilt=0.0):
        pts = []
        for i in range(n + 1):
            t = 2 * math.pi * i / n
            x, y = rx * math.cos(t), ry * math.sin(t)
            xr = x * math.cos(tilt) - y * math.sin(tilt)
            yr = x * math.sin(tilt) + y * math.cos(tilt)
            pts.append((cx + xr, cy + yr))
        return pts

    digits = {
        0: [(1.0, ellipse(10, 10, 6.0, 9.5))],
        1: [(1.0, [(10.5, 0.5), (9.5, 19.5)]),
            (0.5, [(13, 0.5), (7, 19.5)]),
            (0.3, [(15, 0.5), (5, 19.5)])],
        2: [(1.0, [(4, 5), (6, 1.5), (10, 0.5), (14, 1.5), (16, 5), (15, 9), (10, 14), (4, 19.5),
                   (10, 19.5), (17, 19.5)])],
        3: [(1.0, [(4, 2.5), (8, 0.5), (13, 0.8), (15, 4), (13, 8), (9, 9.5), (13, 10.5), (16, 14),
                   (15, 18), (11, 19.8), (4, 18.5)])],
        4: [(0.8, [(7, 0.5), (5, 7), (4, 12.5), (10, 12.5), (17, 12)]),
            (0.5, [(12, 0.5), (8, 6), (4, 12.5)]),
            (1.0, [(14, 2), (14, 8), (13.5, 19.5)])],
        5: [(1.0, [(16, 0.5), (7, 0.5), (6, 5), (5, 9.5), (9, 8.5), (13, 9.5), (15.5, 13), (15, 17.5),
                   (11, 19.8), (4, 18.5)])],
        6: [(1.0, [(14, 0.5), (10, 2.5), (7, 6), (5, 11), (5, 15), (7, 18.5), (10, 19.8), (13, 19),
                   (15, 15.5), (14, 12), (10, 10.5), (6, 12.5), (5, 15)])],
        7: [(1.0, [(4, 1), (10, 0.5), (16, 0.5), (14, 6), (12, 11), (10, 19.5)]),
            (0.5, [(16, 0.5), (11, 10), (8, 19.5)])],
        8: [(1.0, ellipse(10.5, 5, 4.8, 4.7, tilt=-0.2)), (1.0, ellipse(9.5, 14.7, 5.6, 5, tilt=-0.2))],
        9: [(1.0, ellipse(10, 5.5, 5.5, 5)), (1.0, [(15.5, 5.5), (15, 11), (14, 19.5)]),
            (0.5, [(15.5, 5.5), (13, 12), (10, 19.5)])],
    }

    def sample(strokes):
        pts = []
        for wgt, poly in strokes:
            for (u0, v0), (u1, v1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(u1 - u0, v1 - v0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.4))
                phi = math.atan2(v1 - v0, u1 - u0)
                for i in range(n):
                    s = (i + 0.5) / n
                    pts.append([u0 + s * (u1 - u0), v0 + s * (v1 - v0), phi, wgt * L / n])
        P = np.array(pts)
        sc = 0.875
        P[:, 0] = 10 + (P[:, 0] - 10) * sc
        P[:, 1] = 10 + (P[:, 1] - 10) * sc
        P[:, 3] *= sc
        wsum = P[:, 3].sum()
        cx = (P[:, 0] * P[:, 3]).sum() / wsum
        cy = (P[:, 1] * P[:, 3]).sum() / wsum
        P[:, 0] += 14 - cx
        P[:, 1] += 14 - cy
        return P

    sig = 2.2
    NF = 8
    h = 1.4
    alr = np.radians(alphas)

    def templates(centers):
        T = np.zeros((10, NF, 4, 4))
        for d, strokes in digits.items():
            P = sample(strokes)
            acc = np.zeros((NF, 4, 4))
            for x, y, phi, w in P:
                nx, ny = -math.sin(phi), math.cos(phi)
                for sgn in (+1, -1):
                    beta = math.atan2(-sgn * ny, -sgn * nx)
                    tune = np.maximum(0.0, np.cos(beta - alr)) ** 2
                    ex, ey = x + sgn * h * nx, y + sgn * h * ny
                    mr = np.exp(-(ey - centers) ** 2 / (2 * sig ** 2))
                    mc = np.exp(-(ex - centers) ** 2 / (2 * sig ** 2))
                    acc += tune[:, None, None] * np.outer(mr, mc)[None] * w
            T[d] = 1.0 - np.exp(-acc / 1.5)
        return T

    TA = templates(np.array([4 * r + 7.5 for r in range(4)]))   # grid of conv2 ch 0-7
    TB = templates(np.array([4 * r + 9.5 for r in range(4)]))   # grid of conv2 ch 8-15
    T = np.concatenate([TA, TB], axis=1)                         # (10, 16, 4, 4) = fc layout

    # ---------------- fc: multinomial naive Bayes ----------------
    gamma = 0.12
    eps = 0.025
    LQ = np.zeros((10, 256))
    for d in range(10):
        q = T[d].reshape(-1) + eps
        q = q / q.sum()
        LQ[d] = np.log(q)
    LQ -= LQ.mean(axis=0, keepdims=True)
    Wfc = gamma * LQ

    # class-prior corrections accumulated from feedback
    bfc = np.array([0.247, -0.376, 0.65, 0.72, 0.139, 0.582, -0.098, 0.309, -0.52, -0.556])

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
