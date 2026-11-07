# Step 18: bias tweaks and L1-balanced contrast for 3/5 and 7/9

**What step 17 showed.** Every contrast pair moved in the opposite direction from the one intended:
- 3s improved (708 → 809 correct), but 5s got worse.
- 9s improved, but more 7s and 4s were read as 9.

**Why.** I normalised each part to unit L2 norm. A unit-L2 vector's response to spread-out ink grows with its L1 sum, which is roughly the square root of its support. The larger curve parts (3's upper curve, 9's loop) therefore had larger responses to generic ink, and the B-class won whatever the image showed. The effect was large even at a = 0.06, so these part features are powerful if balanced correctly.

**Fix.** I normalise each part to unit L1 sum instead. Then D = L1(A) − L1(B) gives exactly zero response to uniform ink. I keep only the two pairs most worth fixing, 3/5 and 7/9, at a = 0.08 (in logit units, times s).

**Biases.** I also apply small bias corrections from the step-15 prediction counts:

| Digit | Count in step 15 | Change |
|---|---|---|
| 1 | Predicted too often | −0.2 |
| 4 | Predicted too rarely | +0.1 |
| 2 | Predicted too rarely | +0.1 |
| 6 | Predicted too rarely | +0.1 |
| 0 | Predicted a little too often | −0.1 |

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]  # direction (cos,sin), x right, y down
    for k, th in enumerate(thetas):
        G = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                dy, dx = i - 2, j - 2
                d = -dx * math.sin(th) + dy * math.cos(th)   # across the line
                l = dx * math.cos(th) + dy * math.sin(th)    # along the line
                G[i, j] = math.exp(-d * d / (2 * 0.81)) * math.exp(-l * l / 8.0)
        G -= G.mean()                       # zero-sum: uniform ink -> 0
        G *= 1.25 / G[G > 0].sum()
        W1[k, 0] = G
        b1[k] = -0.25
    # channels 4..7 unused (zero)

    # ---------------- conv2: routing / shifting ----------------
    # channel ch = o*4 + sy*2 + sx copies orientation map o, tap at (1+sy, 1+sx)
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for o in range(4):
        for sy in range(2):
            for sx in range(2):
                W2[o * 4 + sy * 2 + sx, o, 1 + sy, 1 + sx] = 1.0

    # ---------------- hand-drawn digit prototypes (x right, y down) ----------------
    def ellipse(cx, cy, rx, ry, a0=0.0, a1=360.0, n=48):
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * t / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * t / n))) for t in range(n + 1)]

    protos = {
        0: [ellipse(14, 14, 6.0, 9)],
        1: [[(15, 4.5), (13.5, 23)]],
        2: [[(8.5, 9), (9.5, 6.5), (12, 5), (15, 4.8), (18, 6), (19.5, 8.5), (19, 11.5), (16.5, 15),
             (13, 18.5), (10, 21), (8, 23), (12, 23), (16, 23), (21, 23)]],
        3: [[(8.5, 6), (12, 4.5), (16, 4.8), (18.5, 7), (18, 10), (15, 12.5), (11.5, 13.5),
             (15.5, 14.5), (19, 17), (19, 20.5), (16, 23), (12, 23.5), (8, 21.5)]],
        4: [[(12, 4.5), (10, 9), (7.5, 15), (13, 15.5), (21, 15.5)], [(18, 6), (18, 23)]],
        5: [[(20, 4.5), (10.5, 4.5), (9.5, 12.5), (13, 11.5), (17, 12), (19.5, 15), (19.5, 19),
             (17, 22.5), (13, 23.5), (8.5, 21.5)]],
        6: [[(17, 4.5), (13, 7.5), (10, 11.5), (8.5, 16), (9, 20), (11.5, 23), (15, 23), (18, 21),
             (19, 17.5), (17, 14.5), (13.5, 14), (10, 15.5), (9, 17)]],
        7: [[(7, 5), (20.5, 5), (17.5, 11), (14.5, 17), (13, 23)]],
        8: [[(17, 6), (14, 4.5), (11, 6), (10.5, 9), (13, 12), (17, 15), (18.5, 18.5), (16.5, 22),
             (13, 23), (9.5, 21.5), (9, 18), (11, 15), (13, 13), (16, 10.5), (17.5, 8), (17, 6)]],
        9: [ellipse(13.5, 9, 5, 4.5), [(18.5, 9), (17, 23)]],
    }

    SHEAR = 0.12   # top of digit leans right
    BLUR = 5.0     # spatial fall-off (px)

    def sample(polys):
        pts = []
        for poly in polys:
            poly = [(x + SHEAR * (14 - y), y) for (x, y) in poly]
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                n = max(1, int(math.ceil(L / 0.5)))
                th = math.atan2(y1 - y0, x1 - x0)
                for k in range(n):
                    t = (k + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0), th))
        return np.array(pts)

    offsets = {}
    for d in range(10):
        P = sample(protos[d])
        offsets[d] = (13.8 - P[:, 0].mean(), 13.8 - P[:, 1].mean())

    def render(polys, d):
        P = sample(polys)
        P[:, 0] += offsets[d][0]
        P[:, 1] += offsets[d][1]
        T = np.zeros((4, 8, 8))
        for o, tho in enumerate(thetas):
            tune = np.cos(P[:, 2] - tho) ** 2
            for Y in range(8):
                cy = 2 * Y + 5.5
                ddy = np.maximum(0, np.abs(P[:, 1] - cy) - 1.5)
                for X in range(8):
                    cx = 2 * X + 5.5
                    ddx = np.maximum(0, np.abs(P[:, 0] - cx) - 1.5)
                    sp = np.maximum(0, 1 - np.sqrt(ddx ** 2 + ddy ** 2) / BLUR)
                    T[o, Y, X] = np.max(tune * sp)
        return T

    def unit2(T):
        return T / np.sqrt(np.sum(T ** 2))

    def unit1(T):
        return T / np.sum(T)

    # base: unit-norm cosine templates (identical to step 15)
    Wt = np.array([unit2(render(protos[d], d)) for d in range(10)])

    # ---------------- L1-balanced discriminating parts ----------------
    # D = L1(part A) - L1(part B): exactly 0 response to uniform ink
    pairs = [
        (5, [[(10.5, 4.5), (9.5, 12.5)]],                        # 5: upper-left vertical
         3, [[(16, 4.8), (18.5, 7), (18, 10), (15, 12.5)]]),     # 3: upper-right curve
        (7, [[(7, 5), (12, 5)]],                                 # 7: top-left bar
         9, [ellipse(13.5, 9, 5, 4.5, 30, 210, 24)]),            # 9: left/bottom of loop
    ]
    a = 0.08
    for (A, pa, B, pb) in pairs:
        D = unit1(render(pa, A)) - unit1(render(pb, B))
        Wt[A] += a * D
        Wt[B] -= a * D

    # ---------------- fc ----------------
    scale = 0.9
    s = 10.0 * scale
    #                       0     1     2     3     4     5     6     7     8      9
    class_bias = np.array([-0.1, -1.6, 0.3, 0.35, 1.15, 0.8, -0.6, 0.0, 0.05, -0.35]) * scale
    Wfc = np.zeros((10, 256))
    bfc = class_bias.copy()
    for dgt in range(10):
        for o in range(4):
            for sy in range(2):
                for sx in range(2):
                    ch = o * 4 + sy * 2 + sx
                    for r in range(4):
                        for c in range(4):
                            Wfc[dgt, ch * 16 + r * 4 + c] = s * Wt[dgt, o, 2 * r + sy, 2 * c + sx]

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
```
