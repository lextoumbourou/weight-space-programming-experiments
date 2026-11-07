# Step 24: return to step 21 with larger bias corrections for 1 and 4

**What went wrong in step 23.** Sharpening the contrast parts made things worse:
- 3→5 rose to 247.
- 8→2 rose to 120.

The hand-placed contrast parts are not reliable. Real digits vary too much in where these small strokes sit. Wide parts blur into other strokes, and tight parts miss them.

**This step.** The early-stop rule may end the run here, and the last network that runs is the one scored. So I return to the step-21 configuration, the best so far at 75.1%: whole-digit templates, the seven peripheral L1-balanced pairs at 0.35, and the step-21 biases.

I make one targeted change. Step 21 still had two consistent imbalances in prediction counts:
- "1" was predicted about 1,280 times against about 1,135 true 1s.
- "4" was predicted about 856 times against about 980 true 4s.
- 4→1 alone accounts for 80 errors.

Earlier changes of ±0.1 to ±0.15 on these biases barely moved the counts, so I make larger moves:
- The "1" bias goes from −1.75 to −2.3.
- The "4" bias goes from 1.25 to 1.6.

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

    # base: unit-norm cosine templates
    Wt = np.array([unit2(render(protos[d], d)) for d in range(10)])

    # ---------------- L1-balanced discriminating parts (step-21 set) ----------------
    pairs = [
        (5, [[(10.5, 4.5), (9.5, 12.5)]],                            # 5: upper-left vertical
         3, [[(16, 4.8), (18.5, 7), (18, 10), (15, 12.5)]]),         # 3: upper-right curve
        (7, [[(7, 5), (12, 5)]],                                     # 7: top-left bar
         9, [ellipse(13.5, 9, 5, 4.5, 30, 210, 24)]),                # 9: left/bottom of loop
        (5, [[(20, 4.5), (13, 4.5)]],                                # 5: top bar
         6, [[(10, 11.5), (8.5, 16), (9, 20)]]),                     # 6: lower-left side
        (5, [[(10.5, 4.5), (9.5, 12.5)]],                            # 5: upper-left vertical
         8, [[(17, 6), (17.5, 8), (16, 10.5)]]),                     # 8: upper-right of top loop
        (2, [[(12, 23), (16, 23), (21, 23)]],                        # 2: flat bottom bar
         8, [[(17, 15), (18.5, 18.5), (17.5, 21)]]),                 # 8: lower-right loop side
        (8, [[(11, 6), (10.5, 9)], [(17, 15), (18.5, 18.5), (16.5, 22)]],  # 8: outer loop sides
         1, [[(15, 4.5), (13.5, 23)]]),                              # 1: central stroke
        (4, [[(12, 4.5), (10, 9), (7.5, 15)]],                       # 4: open upper-left stroke
         9, [ellipse(13.5, 9, 5, 4.5, 200, 340, 16)]),               # 9: top arc of loop
    ]
    a = 0.35
    for (A, pa, B, pb) in pairs:
        D = unit1(render(pa, A)) - unit1(render(pb, B))
        Wt[A] += a * D
        Wt[B] -= a * D

    # ---------------- fc ----------------
    scale = 0.9
    s = 10.0 * scale
    #                       0     1     2     3     4     5     6     7     8      9
    class_bias = np.array([-0.1, -2.3, 0.4, 0.35, 1.6, 0.8, -0.6, 0.0, 0.05, -0.35]) * scale
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
