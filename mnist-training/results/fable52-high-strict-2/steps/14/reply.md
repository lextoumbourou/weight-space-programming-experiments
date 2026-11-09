**Step 14 approach:** full classifier using all twelve measured zone features. Step 13 gave the last three sets of presence rates:

| digit | upper-right V or "\\" | mid-left V | far bottom-right H |
|---|---|---|---|
| 0 | 0.97 | 0.98 | 0.30 |
| 1 | 0.52 | 0.00 | 0.01 |
| 2 | 0.92 | 0.32 | 0.64 |
| 3 | 0.88 | 0.10 | 0.24 |
| 4 | 0.93 | 0.62 | 0.02 |
| 5 | 0.35 | 0.37 | 0.17 |
| 6 | 0.34 | 0.93 | 0.38 |
| 7 | 0.93 | 0.12 | 0.01 |
| 8 | 0.85 | 0.38 | 0.10 |
| 9 | 0.98 | 0.60 | 0.01 |

This step is the step-11 classifier (81.7%) with these changes:

- **Six more measured features added**, the three from step 12 and the three above, in the same naive-Bayes form.
- **The guessed centre veto on 0 is removed**, because step 12 showed half of all 0s have a "/" diagonal in the central box.
- **Overlapping features are down-weighted.** The two upper-right features share cells, as do the two lower-left ones, so each gets weight 0.75. The weak centre "/" feature gets 0.6.
- **The "typical present" value now depends on zone size**, between 1.2 and 3.0. These are my estimates, not measurements.
- **Output scale reduced slightly** (0.7 → 0.6), since more features means more over-counting.

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
    # Hand-drawn digit prototypes (same as step 7/11): strokes in a nominal
    # frame (x right, y down, digit height 0..20). (points, weight); weight<1 = optional.
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
    # fc part 2: twelve zone features with measured presence rates
    # (zone = sum of a few presence cells; presence rates per digit measured
    #  in steps 9, 10, 12, 13).  Naive-Bayes style, linearised in the zone sum r:
    #     contribution(r) = fw * [ log(1-P) + (log P - log(1-P)) * r / R1 ]
    # R1 = typical zone sum when present, fw = weight (<1 for overlapping zones)
    # ------------------------------------------------------------------
    def zone(cells):
        z = np.zeros((16, 4, 4), dtype=np.float64)
        for (bank, o, i, j) in cells:
            z[4 * bank + o, i, j] = 1.0
        return z.reshape(-1)

    ZONES = [
        # horizontal stroke in the top band
        (zone([(P, H, 0, 1), (P, H, 0, 2), (P, H, 0, 3), (R, H, 0, 1), (R, H, 0, 2)]),
         2.5, 1.0, [0.85, 0.03, 0.93, 0.99, 0.06, 0.88, 0.15, 0.89, 0.94, 0.97]),
        # horizontal stroke in the middle band
        (zone([(P, H, 2, 1), (P, H, 2, 2), (P, H, 2, 3), (R, H, 2, 1), (R, H, 2, 2)]),
         2.5, 1.0, [0.02, 0.004, 0.55, 0.88, 0.94, 0.82, 0.70, 0.13, 0.50, 0.90]),
        # horizontal stroke in the bottom band
        (zone([(Q, H, 3, 0), (Q, H, 3, 1), (Q, H, 3, 2), (Q, H, 3, 3), (R, H, 3, 1), (R, H, 3, 2)]),
         2.5, 1.0, [0.99, 0.05, 0.92, 0.96, 0.10, 0.91, 0.97, 0.03, 0.81, 0.10]),
        # vertical stroke in the upper left
        (zone([(S, V, 0, 0), (S, V, 0, 1), (S, V, 1, 0), (S, V, 1, 1), (R, V, 0, 0), (R, V, 1, 0)]),
         2.5, 1.0, [0.65, 0.01, 0.16, 0.09, 0.71, 0.52, 0.55, 0.25, 0.60, 0.82]),
        # vertical stroke in the upper right
        (zone([(S, V, 0, 3), (S, V, 1, 3), (R, V, 0, 3), (R, V, 1, 3)]),
         2.2, 0.75, [0.68, 0.51, 0.88, 0.68, 0.92, 0.06, 0.08, 0.86, 0.58, 0.88]),
        # vertical stroke in the lower right
        (zone([(S, V, 2, 3), (S, V, 3, 3), (R, V, 2, 3), (R, V, 3, 3)]),
         2.2, 1.0, [0.61, 0.03, 0.375, 0.89, 0.56, 0.72, 0.60, 0.52, 0.54, 0.68]),
        # "/" diagonal in the central box (weak feature)
        (zone([(S, D1, 1, 2), (S, D1, 2, 2), (P, D1, 1, 2), (P, D1, 2, 2)]),
         2.0, 0.6, [0.52, 0.68, 0.63, 0.88, 0.59, 0.56, 0.91, 0.52, 0.94, 0.82]),
        # "\" diagonal in the central box (crossing of the 8)
        (zone([(S, D2, 1, 2), (S, D2, 2, 2), (P, D2, 1, 2), (P, D2, 2, 2)]),
         2.0, 1.0, [0.05, 0.07, 0.24, 0.47, 0.28, 0.64, 0.28, 0.145, 0.83, 0.29]),
        # vertical or "/" stroke in the lower left
        (zone([(S, o, i, j) for o in (V, D1) for i in (2, 3) for j in (0, 1)]),
         3.0, 0.75, [0.98, 0.40, 0.81, 0.375, 0.68, 0.52, 0.92, 0.235, 0.87, 0.41]),
        # vertical or "\" stroke in the upper right
        (zone([(S, o, i, 3) for o in (V, D2) for i in (0, 1)] +
              [(R, o, i, 3) for o in (V, D2) for i in (0, 1)]),
         3.0, 0.75, [0.97, 0.52, 0.92, 0.88, 0.93, 0.35, 0.34, 0.93, 0.85, 0.98]),
        # vertical stroke on the left just below mid height
        (zone([(S, V, 2, 0), (S, V, 2, 1), (R, V, 2, 0), (Q, V, 2, 0)]),
         1.8, 0.75, [0.98, 0.003, 0.32, 0.10, 0.62, 0.37, 0.93, 0.12, 0.38, 0.60]),
        # horizontal stroke at the far bottom right (base of the 2)
        (zone([(Q, H, 3, 3), (R, H, 3, 3)]),
         1.2, 1.0, [0.30, 0.01, 0.64, 0.24, 0.02, 0.17, 0.38, 0.01, 0.095, 0.005]),
    ]
    for (z, r1, fw, probs) in ZONES:
        for dgt in range(10):
            pr = min(0.96, max(0.04, probs[dgt]))
            lp = math.log(pr)
            lq = math.log(1.0 - pr)
            W[dgt] += fw * (lp - lq) / r1 * z
            B[dgt] += fw * lq

    # small bias corrections (same as step 11) for classes the hand-drawn
    # template favoured / disfavoured
    B += np.array([0.0, -0.5, 0.0, 0.0, 0.3, 0.0, 0.3, 0.0, 0.7, 0.3])

    ALPHA = 0.6
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
