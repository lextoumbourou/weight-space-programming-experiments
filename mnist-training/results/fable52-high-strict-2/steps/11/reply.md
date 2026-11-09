**Step 11 approach:** first classifier built from the measured features. Steps 9 and 10 gave me, for each digit, how often each of six zone features is present. The horizontal ones are very clean and the vertical ones less so:

| digit | top H | mid H | bottom H | upper-left V | upper-right V | lower-right V |
|---|---|---|---|---|---|---|
| 0 | 0.85 | 0.02 | 0.99 | 0.65 | 0.68 | 0.61 |
| 1 | 0.03 | 0.00 | 0.05 | 0.01 | 0.51 | 0.03 |
| 2 | 0.93 | 0.55 | 0.92 | 0.16 | 0.88 | 0.38 |
| 3 | 0.99 | 0.88 | 0.96 | 0.09 | 0.68 | 0.89 |
| 4 | 0.06 | 0.94 | 0.10 | 0.71 | 0.92 | 0.56 |
| 5 | 0.88 | 0.82 | 0.91 | 0.52 | 0.06 | 0.72 |
| 6 | 0.15 | 0.70 | 0.97 | 0.55 | 0.08 | 0.60 |
| 7 | 0.89 | 0.13 | 0.03 | 0.25 | 0.86 | 0.52 |
| 8 | 0.94 | 0.50 | 0.81 | 0.60 | 0.58 | 0.54 |
| 9 | 0.97 | 0.90 | 0.10 | 0.82 | 0.88 | 0.68 |

The fc layer in this step combines three things:

- **Six measured zone features, naive-Bayes style.** Each contributes log(1−P) when absent and rises linearly with the zone sum to about log(P) at a typical "present" value. The typical value of 2.5 is my estimate.
- **The step-7 hand-drawn Bernoulli template at reduced weight**, to supply the finer shape detail the six zones cannot.
- **A hand-set veto on 0 for diagonal or vertical ink in the central box.** This is unmeasured; it targets 8 versus 0, which the six features barely separate.

I also added small bias nudges for the classes the template under-predicted (8, 4, 6, 9) and over-predicted (1).

```python
import numpy as np
import math


def build_weights():
    ANG = [0.0, 45.0, 90.0, 135.0]   # orientation index: 0=H "-", 1=D1 "/", 2=V "|", 3=D2 "\"
    H, D1, V, D2 = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # conv1: 4 oriented bar detectors, each with two biases, so that after
    # ReLU+maxpool  S_o = chan(2o) - chan(2o+1) = clip((resp-T0)/(T1-T0),0,1)
    # is a saturated "stroke of orientation o is here" map (12x12).
    # ------------------------------------------------------------------
    T0, T1 = 1.5, 3.5
    sig = 1.2
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)
    for o in range(4):
        th = math.radians(ANG[o])
        k = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                u = c - 2.0
                v = r - 2.0
                d = abs(u * math.sin(th) + v * math.cos(th))
                k[r, c] = (1.0 - d * d / (sig * sig)) * math.exp(-d * d / (2 * sig * sig))
        k = k - k.mean()
        c1w[2 * o, 0] = k / (T1 - T0)
        c1w[2 * o + 1, 0] = k / (T1 - T0)
        c1b[2 * o] = -T0 / (T1 - T0)
        c1b[2 * o + 1] = -T1 / (T1 - T0)

    # ------------------------------------------------------------------
    # conv2: 4 banks x 4 orientations, each channel a single tap on S_o.
    # After the 2x2 max-pool, cell (i,j) of a bank with tap (ca,cb) says
    # "a stroke of orientation o is present in the 4x4 px box centred at
    #  row 4i+2ca+3.5, col 4j+2cb+3.5"  (value in [0,1]).
    #   bank 0 (P): tap (1,1) -> rows 5.5, 9.5,13.5,17.5 ; cols 5.5, 9.5,13.5,17.5
    #   bank 1 (Q): tap (3,2) -> rows 9.5,13.5,17.5,21.5 ; cols 7.5,11.5,15.5,19.5
    #   bank 2 (R): tap (2,2) -> rows 7.5,11.5,15.5,19.5 ; cols 7.5,11.5,15.5,19.5
    #   bank 3 (S): tap (2,1) -> rows 7.5,11.5,15.5,19.5 ; cols 5.5, 9.5,13.5,17.5
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)
    BANKS = [(1, 1), (3, 2), (2, 2), (2, 1)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            c2w[4 * bi + o, 2 * o, ca, cb] = 1.0
            c2w[4 * bi + o, 2 * o + 1, ca, cb] = -1.0
    P, Q, R, S = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # Hand-drawn digit prototypes (same as step 7): strokes in a nominal frame
    # (x right, y down, digit height 0..20).  (points, weight); weight<1 = optional.
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1):
        n = max(2, int(abs(a1 - a0) / 6.0) + 1)
        pts = []
        for k in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        return pts

    protos = {}
    protos[0] = [(arc(0, 10, 6.5, 10, -180, 180), 1.0)]
    protos[1] = [([(0, 0), (0, 20)], 1.0),
                 ([(3, 0), (-3, 20)], 0.5),
                 ([(0, 0), (-3, 3.5)], 0.35),
                 ([(-3.5, 20), (3.5, 20)], 0.3)]
    a2 = arc(0, 5.5, 5, 5.5, -170, 40)
    protos[2] = [(a2, 1.0),
                 ([a2[-1], (-5.5, 20)], 1.0),
                 ([(-5.5, 20), (6, 20)], 1.0),
                 ([(6, 20), (7, 17.5)], 0.4)]
    protos[3] = [(arc(-0.5, 5, 5, 5, -150, 90), 1.0),
                 (arc(-0.5, 15, 5.5, 5, -90, 150), 1.0)]
    protos[4] = [([(-3, 0), (-5.5, 11)], 1.0),
                 ([(-5.5, 11), (6.5, 11)], 1.0),
                 ([(2.5, 0), (2.5, 20)], 1.0)]
    protos[5] = [([(5.5, 0), (-3.5, 0)], 1.0),
                 ([(-3.5, 0), (-4.5, 8.5)], 1.0),
                 (arc(-0.5, 13.5, 5.5, 6.5, -135, 150), 1.0)]
    protos[6] = [([(3.5, 0), (0.5, 3.5), (-2.5, 7.5), (-4.3, 11.5), (-5, 14.5)], 1.0),
                 (arc(0, 14.5, 5, 5.5, -180, 180), 1.0)]
    protos[7] = [([(-6, 0), (5.5, 0)], 1.0),
                 ([(5.5, 0), (-1, 20)], 1.0),
                 ([(-6, 0), (-6, 3)], 0.4),
                 ([(-1.5, 10), (5, 10)], 0.35)]
    eight = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        a8 = 4.2 if math.cos(t) > 0 else 5.0
        eight.append((a8 * math.sin(2 * t), 10 - 10 * math.cos(t)))
    protos[8] = [(eight, 1.0)]
    protos[9] = [(arc(-0.5, 5.5, 4.5, 5.5, -180, 180), 1.0),
                 ([(4.2, 3), (3, 20)], 1.0)]

    def densify(Pp, w, out):
        for k in range(len(Pp) - 1):
            xa, ya = Pp[k]
            xb, yb = Pp[k + 1]
            L = math.hypot(xb - xa, yb - ya)
            if L < 1e-9:
                continue
            n = max(1, int(math.ceil(L / 0.5)))
            th = math.degrees(math.atan2(-(yb - ya), xb - xa)) % 180.0
            for q in range(n):
                f = (q + 0.5) / n
                out.append([xa + (xb - xa) * f, ya + (yb - ya) * f, th, w, L / n])

    def prep(strokes, shear=0.15):
        # slant right, scale centre-line box to 17.5 px, centre of mass to (13.5,13.5)
        Sx = []
        xs = []
        ys = []
        for (pts, w) in strokes:
            Pp = [(x + shear * (10.0 - y), y) for (x, y) in pts]
            Sx.append((Pp, w))
            if w >= 0.99:
                xs += [p[0] for p in Pp]
                ys += [p[1] for p in Pp]
        scale = 17.5 / max(max(xs) - min(xs), max(ys) - min(ys))
        samples = []
        for (Pp, w) in Sx:
            Pp = [(x * scale, y * scale) for (x, y) in Pp]
            densify(Pp, w, samples)
        tot = sum(s[3] * s[4] for s in samples)
        mx = sum(s[0] * s[3] * s[4] for s in samples) / tot
        my = sum(s[1] * s[3] * s[4] for s in samples) / tot
        for s in samples:
            s[0] += 13.5 - mx
            s[1] += 13.5 - my
        return np.array(samples, dtype=np.float64)

    # paint a prototype as an expected-presence map in [0,1] (by formula)
    sigT = 2.6
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))

    def template(samples):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        x = samples[:, 0]
        y = samples[:, 1]
        th = samples[:, 2]
        wl = samples[:, 3] * samples[:, 4]
        tune = []
        for o in range(4):
            d = np.abs(th - ANG[o])
            d = np.minimum(d, 180.0 - d)
            tune.append(np.clip(1.3 * (1.0 - (d / 42.0) ** 2), 0.0, 1.0))
        for bi, (ca, cb) in enumerate(BANKS):
            for i in range(4):
                cy = 4 * i + 2 * ca + 3.5
                for j in range(4):
                    cx = 4 * j + 2 * cb + 3.5
                    g = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigT * sigT))
                    for o in range(4):
                        T[4 * bi + o, i, j] = cT * float(np.sum(wl * tune[o] * g))
        return np.clip(T, 0.0, 1.0)

    # ------------------------------------------------------------------
    # fc part 1: hand-drawn Bernoulli template (as in step 7), reduced weight
    # ------------------------------------------------------------------
    EPS = 0.2
    BETA = 0.12
    W = np.zeros((10, 256), dtype=np.float64)
    B = np.zeros(10, dtype=np.float64)
    for dgt in range(10):
        T = template(prep(protos[dgt])).reshape(-1)
        p = EPS + (1.0 - 2.0 * EPS) * T
        W[dgt] = BETA * np.log(p / (1.0 - p))
        B[dgt] = BETA * float(np.sum(np.log(1.0 - p)))
    B = B - B.mean()

    # ------------------------------------------------------------------
    # fc part 2: six zone features with measured presence rates
    # (zone = sum of a few presence cells; "present" = sum > 1, measured in
    #  steps 9 and 10).  Naive-Bayes style, linearised in the zone sum r:
    #     contribution(r) = log(1-P) + (log P - log(1-P)) * r / R1
    # ------------------------------------------------------------------
    def zone(cells):
        z = np.zeros((16, 4, 4), dtype=np.float64)
        for (bank, o, i, j) in cells:
            z[4 * bank + o, i, j] = 1.0
        return z.reshape(-1)

    ZONES = [
        # horizontal stroke in the top band
        (zone([(P, H, 0, 1), (P, H, 0, 2), (P, H, 0, 3), (R, H, 0, 1), (R, H, 0, 2)]),
         [0.85, 0.04, 0.93, 0.96, 0.06, 0.88, 0.15, 0.89, 0.94, 0.96]),
        # horizontal stroke in the middle band
        (zone([(P, H, 2, 1), (P, H, 2, 2), (P, H, 2, 3), (R, H, 2, 1), (R, H, 2, 2)]),
         [0.04, 0.04, 0.55, 0.88, 0.94, 0.82, 0.70, 0.13, 0.50, 0.90]),
        # horizontal stroke in the bottom band
        (zone([(Q, H, 3, 0), (Q, H, 3, 1), (Q, H, 3, 2), (Q, H, 3, 3), (R, H, 3, 1), (R, H, 3, 2)]),
         [0.96, 0.05, 0.92, 0.96, 0.10, 0.91, 0.96, 0.04, 0.81, 0.10]),
        # vertical stroke in the upper left
        (zone([(S, V, 0, 0), (S, V, 0, 1), (S, V, 1, 0), (S, V, 1, 1), (R, V, 0, 0), (R, V, 1, 0)]),
         [0.65, 0.04, 0.16, 0.09, 0.71, 0.52, 0.55, 0.25, 0.60, 0.82]),
        # vertical stroke in the upper right
        (zone([(S, V, 0, 3), (S, V, 1, 3), (R, V, 0, 3), (R, V, 1, 3)]),
         [0.68, 0.51, 0.88, 0.68, 0.92, 0.06, 0.08, 0.86, 0.58, 0.88]),
        # vertical stroke in the lower right
        (zone([(S, V, 2, 3), (S, V, 3, 3), (R, V, 2, 3), (R, V, 3, 3)]),
         [0.61, 0.04, 0.375, 0.89, 0.56, 0.72, 0.60, 0.52, 0.54, 0.68]),
    ]
    R1 = 2.5      # typical zone sum when the stroke is present
    for (z, probs) in ZONES:
        for dgt in range(10):
            pr = min(0.96, max(0.04, probs[dgt]))
            lp = math.log(pr)
            lq = math.log(1.0 - pr)
            W[dgt] += (lp - lq) / R1 * z
            B[dgt] += lq

    # ------------------------------------------------------------------
    # fc part 3: hand-set veto -- diagonal or vertical ink in the central box
    # (x ~ 11.5..15.5, y ~ 7.5..17.5) speaks against 0 (helps 8 vs 0, 2 vs 0)
    # ------------------------------------------------------------------
    centre = zone([(S, o, i, 2) for o in (D1, V, D2) for i in (1, 2)] +
                  [(P, o, i, 2) for o in (D1, V, D2) for i in (1, 2)])
    W[0] += -0.8 * centre

    # small bias corrections for classes the hand-drawn template favoured /
    # disfavoured in step 7
    B += np.array([0.0, -0.5, 0.0, 0.0, 0.3, 0.0, 0.3, 0.0, 0.7, 0.3])

    ALPHA = 0.7
    fcw = ALPHA * W
    fcb = ALPHA * (B - B.mean())

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
