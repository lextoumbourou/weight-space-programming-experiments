**Step 5 approach:** rebuild the fc evidence around what the step-4 measurement showed.

What the measurement showed:

- **Stroke evidence is usable.** The "horizontal stroke at the bottom" feature mostly reads 1.2–2.2 (up to 3.5) for digits that have it (0, 2, 3, 5, 6), and below 0.5 for about 90% of 1s and 7s. 4 and 9 mostly sit between 0.5 and 1.2, which I read as leakage from nearby strokes. A threshold near 1.0 separates the two groups.
- **The up-tip detector is not selective.** It fires on 1 (85%) and 4 (91%) as intended, but also on 9 (69%), 0, 7, 8 (about 50% each), and it misses 6 (10%).

Changes in this step:

- **Symmetric thresholded evidence.** Each evidence stroke k adds `g·s·(response − θ)` to a class, where s is +1 if the digit has that stroke, −1 if it lacks it, and fractional if unsure. Giving bonuses to only some of the "have" classes was the flaw in steps 2–3.
- **Eleven stroke items** with hand-estimated signatures replace the old vetoes and bonuses. Only the bottom-bar signature is measured; the rest are my estimates.
- **Stronger inhibition in the ending detectors**, so loop tops and corners stop looking like tips. Tips are no longer used as evidence; they remain only inside the templates.

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
    # conv2
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    def put(ch, o, a, b, val):
        # weight 'val' on the saturated orientation map S_o at kernel tap (a,b)
        c2w[ch, 2 * o, a, b] += val
        c2w[ch, 2 * o + 1, a, b] -= val

    # channels 0-11: blurred orientation maps, 3 banks with different kernel centres
    # (bank centre (ca,cb) -> pooled cell (i,j) centred at pixel row 4i+2ca+3.5, col 4j+2cb+3.5)
    BANKS = [(2, 2), (1, 2), (3, 2)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            for a in range(5):
                for b in range(5):
                    put(4 * bi + o, o, a, b,
                        0.32 * math.exp(-((a - ca) ** 2 + (b - cb) ** 2) / 2.0))

    # channels 12-15: stroke-ending detectors.  Inhibition is now stronger and
    # wider (whole row/column beyond the tip, and any bar crossing at the tip),
    # so that loop tops and corners no longer look like free stroke ends.
    INH = -1.5
    ch = 12   # tip pointing up, tip at kernel tap (1,2)
    put(ch, V, 1, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 1, 2, 0.6); put(ch, D1, 2, 1, 0.4)
    put(ch, D2, 1, 2, 0.6); put(ch, D2, 2, 3, 0.4)
    for b in range(5):
        for o in range(4):
            put(ch, o, 0, b, INH)
        put(ch, H, 1, b, INH)
    ch = 13   # tip pointing down, tip at (3,2)
    put(ch, V, 3, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 3, 2, 0.6); put(ch, D1, 2, 3, 0.4)
    put(ch, D2, 3, 2, 0.6); put(ch, D2, 2, 1, 0.4)
    for b in range(5):
        for o in range(4):
            put(ch, o, 4, b, INH)
        put(ch, H, 3, b, INH)
    ch = 14   # tip pointing left, tip at (2,1)
    put(ch, H, 2, 1, 0.6); put(ch, H, 2, 2, 0.4)
    for a in range(5):
        for o in range(4):
            put(ch, o, a, 0, INH)
        put(ch, V, a, 1, INH)
    ch = 15   # tip pointing right, tip at (2,3)
    put(ch, H, 2, 3, 0.6); put(ch, H, 2, 2, 0.4)
    for a in range(5):
        for o in range(4):
            put(ch, o, a, 4, INH)
        put(ch, V, a, 3, INH)
    TIP_TAP = {12: (1, 2), 13: (3, 2), 14: (2, 1), 15: (2, 3)}

    # ------------------------------------------------------------------
    # Hand-drawn digit prototypes: strokes in a nominal frame
    # (x right, y down, digit height 0..20, x centred near 0).
    # Each stroke: (polyline points, weight, tip_at_start, tip_at_end)
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1):
        n = max(2, int(abs(a1 - a0) / 6.0) + 1)
        pts = []
        for k in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        return pts

    protos = {}
    protos[0] = [(arc(0, 10, 6.5, 10, -180, 180), 1.0, False, False)]
    protos[1] = [([(0, 0), (0, 20)], 1.0, True, True),
                 ([(3, 0), (-3, 20)], 0.5, True, True)]
    a2 = arc(0, 5.5, 5, 5.5, -170, 40)
    protos[2] = [(a2, 1.0, True, False),
                 ([a2[-1], (-5.5, 20)], 1.0, False, False),
                 ([(-5.5, 20), (6, 20)], 1.0, False, True)]
    protos[3] = [(arc(-0.5, 5, 5, 5, -150, 90), 1.0, True, False),
                 (arc(-0.5, 15, 5.5, 5, -90, 150), 1.0, False, True)]
    protos[4] = [([(-3, 0), (-5.5, 11)], 1.0, True, False),
                 ([(-5.5, 11), (6.5, 11)], 1.0, False, True),
                 ([(2.5, 0), (2.5, 20)], 1.0, True, True)]
    protos[5] = [([(5.5, 0), (-3.5, 0)], 1.0, True, False),
                 ([(-3.5, 0), (-4.5, 8.5)], 1.0, False, False),
                 (arc(-0.5, 13.5, 5.5, 6.5, -135, 150), 1.0, False, True)]
    protos[6] = [([(3.5, 0), (0.5, 3.5), (-2.5, 7.5), (-4.3, 11.5), (-5, 14.5)], 1.0, True, False),
                 (arc(0, 14.5, 5, 5.5, -180, 180), 1.0, False, False)]
    protos[7] = [([(-6, 0), (5.5, 0)], 1.0, True, False),
                 ([(5.5, 0), (-1, 20)], 1.0, False, True)]
    eight = []
    for k in range(73):
        t = 2 * math.pi * k / 72
        a8 = 4.2 if math.cos(t) > 0 else 5.0
        eight.append((a8 * math.sin(2 * t), 10 - 10 * math.cos(t)))
    protos[8] = [(eight, 1.0, False, False)]
    protos[9] = [(arc(-0.5, 5.5, 4.5, 5.5, -180, 180), 1.0, False, False),
                 ([(4.2, 3), (3, 20)], 1.0, False, True)]

    def densify(P, w, out, oris=None):
        # polyline -> samples [x, y, orientation(deg), weight*length]
        for k in range(len(P) - 1):
            xa, ya = P[k]
            xb, yb = P[k + 1]
            L = math.hypot(xb - xa, yb - ya)
            if L < 1e-9:
                continue
            n = max(1, int(math.ceil(L / 0.5)))
            th = math.degrees(math.atan2(-(yb - ya), xb - xa)) % 180.0
            for q in range(n):
                f = (q + 0.5) / n
                x = xa + (xb - xa) * f
                y = ya + (yb - ya) * f
                if oris is not None:
                    for a in oris:
                        out.append([x, y, a, w * L / n])
                else:
                    out.append([x, y, th, w * L / n])

    def prep(strokes, shear=0.15):
        # slant right, scale centre-line box to 17.5 px, centre of mass to (13.5,13.5)
        S = []
        xs = []
        ys = []
        for (pts, w, t0, t1) in strokes:
            P = [(x + shear * (10.0 - y), y) for (x, y) in pts]
            S.append((P, w, t0, t1))
            xs += [p[0] for p in P]
            ys += [p[1] for p in P]
        scale = 17.5 / max(max(xs) - min(xs), max(ys) - min(ys))
        samples = []
        tips = []
        for (P, w, t0, t1) in S:
            P = [(x * scale, y * scale) for (x, y) in P]
            densify(P, w, samples)
            if t0:
                tips.append([P[0][0], P[0][1], P[0][0] - P[1][0], P[0][1] - P[1][1], w])
            if t1:
                tips.append([P[-1][0], P[-1][1], P[-1][0] - P[-2][0], P[-1][1] - P[-2][1], w])
        tot = sum(s[3] for s in samples)
        mx = sum(s[0] * s[3] for s in samples) / tot
        my = sum(s[1] * s[3] for s in samples) / tot
        for s in samples:
            s[0] += 13.5 - mx
            s[1] += 13.5 - my
        for t in tips:
            t[0] += 13.5 - mx
            t[1] += 13.5 - my
        return np.array(samples, dtype=np.float64), tips

    # ------------------------------------------------------------------
    # Paint strokes directly into the 16x4x4 feature space (by formula)
    # ------------------------------------------------------------------
    sigT = 2.6
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))

    def clip01(x):
        return min(1.0, max(0.0, x))

    def template(samples, tips):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        x = samples[:, 0]
        y = samples[:, 1]
        th = samples[:, 2]
        wl = samples[:, 3]
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
        for (tx, ty, dx, dy, w) in tips:
            phi = math.degrees(math.atan2(abs(dy), abs(dx)))
            hw = clip01((50.0 - phi) / 25.0)
            vw = clip01((phi - 20.0) / 20.0)
            lst = []
            if vw > 0:
                lst.append((12 if dy < 0 else 13, vw))
            if hw > 0:
                lst.append((14 if dx < 0 else 15, hw))
            for (chn, ww) in lst:
                ta, tb = TIP_TAP[chn]
                for i in range(4):
                    cy = 4 * i + 2 * ta + 3.5
                    for j in range(4):
                        cx = 4 * j + 2 * tb + 3.5
                        T[chn, i, j] += w * ww * math.exp(
                            -((tx - cx) ** 2 + (ty - cy) ** 2) / (2 * 2.0 * 2.0))
        return T

    # base weights: unit-norm template per class (cosine matching)
    W = np.zeros((10, 256), dtype=np.float64)
    B = np.zeros(10, dtype=np.float64)
    for dgt in range(10):
        samples, tips = prep(protos[dgt])
        T = template(samples, tips).reshape(-1)
        W[dgt] = T / (np.linalg.norm(T) + 1e-9)

    # ------------------------------------------------------------------
    # Symmetric thresholded evidence.
    # Each item is a short stroke in absolute pixel coordinates (x=col, y=row)
    # painted into feature space and unit-normalised (N).  Its response r on an
    # image is about 1.2-2.2 when such a stroke is present, <0.5 when absent
    # (measured in step 4).  Class c gets  g * s_c * (r - theta),
    # s_c = +1 if the digit has the stroke, -1 if it lacks it, fractional if unsure.
    # ------------------------------------------------------------------
    def stroke_feat(pts, oris=None):
        smp = []
        densify(pts, 1.0, smp, oris)
        T = template(np.array(smp, dtype=np.float64), []).reshape(-1)
        return T / (np.linalg.norm(T) + 1e-9)

    EVID = [
        # A: horizontal stroke at the bottom
        (stroke_feat([(9, 21.8), (16, 21.8)]), 0.20, 1.0,
         {0: 1, 2: 1, 3: 1, 5: 1, 6: 1, 8: 0.3, 4: -0.6, 9: -0.7, 1: -1, 7: -1}),
        # B: horizontal stroke at the top
        (stroke_feat([(10.5, 5.5), (16, 5.5)]), 0.20, 1.0,
         {7: 1, 2: 1, 3: 1, 5: 1, 9: 1, 0: 0.5, 8: 0.3, 4: -1, 1: -1, 6: -0.8}),
        # C: horizontal stroke in the middle
        (stroke_feat([(10.5, 14), (16.5, 14)]), 0.20, 1.0,
         {4: 1, 5: 0.6, 6: 0.6, 9: 0.6, 3: 0.4, 2: -0.3, 0: -1, 1: -1, 7: -0.7}),
        # D: vertical stroke on the upper left
        (stroke_feat([(9.7, 7), (9.7, 12)]), 0.20, 1.0,
         {4: 0.8, 5: 0.7, 9: 0.8, 0: 1, 8: 0.6, 6: 0.3, 7: -0.8, 3: -0.8, 2: -0.5, 1: -1}),
        # E: vertical stroke on the upper right
        (stroke_feat([(17.5, 7), (17.5, 11.5)]), 0.20, 1.0,
         {0: 1, 9: 1, 3: 0.8, 2: 0.8, 7: 0.6, 8: 0.6, 4: 0.7, 5: -1, 6: -1, 1: -0.3}),
        # F: vertical stroke on the lower left
        (stroke_feat([(9.7, 15), (9.7, 19.5)]), 0.20, 1.0,
         {0: 1, 6: 1, 8: 0.6, 1: -0.8, 3: -0.7, 4: -0.8, 5: -0.7, 7: -1, 9: -1}),
        # G: vertical stroke on the lower right
        (stroke_feat([(17.7, 15), (17.7, 19.5)]), 0.20, 1.0,
         {0: 1, 3: 1, 5: 1, 6: 0.8, 8: 0.8, 2: -0.8, 1: -0.8, 7: -0.8}),
        # H: vertical stem through the lower centre
        (stroke_feat([(13.5, 16), (13.5, 21)]), 0.15, 1.0,
         {1: 1, 7: 0.8, 4: 0.5, 9: 0.5, 0: -1, 3: -0.7, 5: -0.7, 6: -0.8}),
        # J: horizontal stroke at the bottom right (end of the 2's base)
        (stroke_feat([(16.5, 21.5), (20.5, 21.5)]), 0.12, 1.0,
         {2: 1, 3: -0.4, 5: -0.4}),
        # K: "/" diagonal in the lower left (2's diagonal)
        (stroke_feat([(12.5, 16), (9, 20.5)]), 0.15, 1.0,
         {2: 1, 3: -0.8, 5: -0.8, 0: -0.5, 6: -0.5, 4: -0.5, 9: -0.5, 7: -0.3}),
        # M: cross bar sticking out to the right at mid height (4)
        (stroke_feat([(17, 15), (21, 15)]), 0.12, 0.8,
         {4: 1, 9: -0.6, 1: -0.5, 2: -0.3, 7: -0.3}),
    ]
    for (N, g, theta, sig_c) in EVID:
        for dgt, s in sig_c.items():
            W[dgt] += g * s * N
            B[dgt] -= g * s * theta

    ALPHA = 3.0
    fcw = ALPHA * W
    fcb = ALPHA * B

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
