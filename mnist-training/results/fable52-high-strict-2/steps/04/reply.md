**Step 4 approach:** this step is a measurement, not a classifier, so its accuracy will be meaningless. Step 3 showed that my guess for how strongly a "present" stroke responds is off: the bias-compensated bonuses still turned 6 and 3 into attractors. Rather than keep guessing, I am using this step's confusion matrix as a histogram of two feature responses per true class.

The predicted column k encodes two quantities, with a = k mod 5 and b = k div 5:

- **a (5 bins):** response of the "horizontal stroke at the bottom" evidence feature, with bin edges at 0.5, 1.2, 2.2 and 3.5. Digits 0, 2, 3, 5, 6, 8 should have this stroke and 1, 4, 7, 9 should not, so this gives the present and absent levels.
- **b (2 bins):** whether the "stroke tip pointing up at the top" feature exceeds 0.25. This should fire for 1, 4 and 6, and tells me whether the ending detectors work at all.

The conv layers are unchanged from step 3. I will use the result to set thresholds and strengths for the evidence features in the following steps.

```python
import numpy as np
import math


def build_weights():
    ANG = [0.0, 45.0, 90.0, 135.0]   # orientation index: 0=H "-", 1=D1 "/", 2=V "|", 3=D2 "\"
    H, D1, V, D2 = 0, 1, 2, 3

    # ------------------------------------------------------------------
    # conv1: 4 oriented bar detectors, each with two biases, so that after
    # ReLU+maxpool  S_o = chan(2o) - chan(2o+1) = clip((resp-T0)/(T1-T0),0,1)
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
    # conv2 (unchanged): 0-11 blurred orientation maps (3 banks),
    # 12-15 stroke-ending detectors (up, down, left, right)
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    def put(ch, o, a, b, val):
        c2w[ch, 2 * o, a, b] += val
        c2w[ch, 2 * o + 1, a, b] -= val

    BANKS = [(2, 2), (1, 2), (3, 2)]
    for bi, (ca, cb) in enumerate(BANKS):
        for o in range(4):
            for a in range(5):
                for b in range(5):
                    put(4 * bi + o, o, a, b,
                        0.32 * math.exp(-((a - ca) ** 2 + (b - cb) ** 2) / 2.0))

    ch = 12   # tip pointing up, tip at kernel tap (1,2)
    put(ch, V, 1, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 1, 2, 0.6); put(ch, D1, 2, 1, 0.4)
    put(ch, D2, 1, 2, 0.6); put(ch, D2, 2, 3, 0.4)
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 0, b, -1.0)
        put(ch, H, 1, b, -0.7)
    ch = 13   # tip pointing down, tip at (3,2)
    put(ch, V, 3, 2, 0.6); put(ch, V, 2, 2, 0.4)
    put(ch, D1, 3, 2, 0.6); put(ch, D1, 2, 3, 0.4)
    put(ch, D2, 3, 2, 0.6); put(ch, D2, 2, 1, 0.4)
    for b in (1, 2, 3):
        for o in range(4):
            put(ch, o, 4, b, -1.0)
        put(ch, H, 3, b, -0.7)
    ch = 14   # tip pointing left, tip at (2,1)
    put(ch, H, 2, 1, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 0, -1.0)
        put(ch, V, a, 1, -0.7)
    ch = 15   # tip pointing right, tip at (2,3)
    put(ch, H, 2, 3, 0.6); put(ch, H, 2, 2, 0.4)
    for a in (1, 2, 3):
        for o in range(4):
            put(ch, o, a, 4, -1.0)
        put(ch, V, a, 3, -0.7)
    TIP_TAP = {12: (1, 2), 13: (3, 2), 14: (2, 1), 15: (2, 3)}

    # ------------------------------------------------------------------
    # Painting strokes into the 16x4x4 feature space (same as before)
    # ------------------------------------------------------------------
    def densify(P, w, out, oris=None):
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

    sigT = 2.6
    cT = 1.0 / (sigT * math.sqrt(2 * math.pi))

    def template(samples):
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
        return T

    def stroke_feat(pts, oris=None):
        smp = []
        densify(pts, 1.0, smp, oris)
        T = template(np.array(smp, dtype=np.float64)).reshape(-1)
        return T / (np.linalg.norm(T) + 1e-9)

    def tip_feat(chn, pts):
        T = np.zeros((16, 4, 4), dtype=np.float64)
        ta, tb = TIP_TAP[chn]
        for (tx, ty) in pts:
            for i in range(4):
                cy = 4 * i + 2 * ta + 3.5
                for j in range(4):
                    cx = 4 * j + 2 * tb + 3.5
                    T[chn, i, j] += math.exp(-((tx - cx) ** 2 + (ty - cy) ** 2) / (2 * 2.0 * 2.0))
        T = T.reshape(-1)
        return T / (np.linalg.norm(T) + 1e-9)

    # ------------------------------------------------------------------
    # PROBE fc layer.
    # xA = response of the "horizontal stroke at the bottom" evidence feature
    # xB = response of the "tip pointing up at the top" evidence feature
    # output index k = a + 5*b, where
    #   a = number of thresholds in tA that xA exceeds (0..4)
    #   b = 1 if xB > tB else 0
    # (logit_k = a*xA - sum(tA[:a]) + b*(xB - tB); the argmax picks the bins)
    # ------------------------------------------------------------------
    NA = stroke_feat([(9, 21.8), (16, 21.8)])
    NB = tip_feat(12, [(14, 5), (17, 5)])
    tA = [0.5, 1.2, 2.2, 3.5]
    tB = 0.25
    cum = [0.0]
    for t in tA:
        cum.append(cum[-1] + t)

    SCALE = 5.0
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for b in range(2):
        for a in range(5):
            kcls = a + 5 * b
            fcw[kcls] = SCALE * (a * NA + b * NB)
            fcb[kcls] = SCALE * (-cum[a] - b * tB)

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
