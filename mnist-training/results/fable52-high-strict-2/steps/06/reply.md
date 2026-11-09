**Step 6 approach:** another measurement step, so accuracy will again be meaningless. The largest remaining errors are 2→3 (337), 7→9 (259), 5→3 (112) and 9→3 (108). My hand-estimated signatures for the features that should separate those pairs evidently don't match the data, and I can't tell which from the confusion matrix alone.

This step reads out three of those features at once, each thresholded at 1.0. The predicted column k encodes which ones are present:

`k = G + 2·K + 4·D`

- **G:** vertical stroke on the lower right (expected for 3 and 5, not 2).
- **K:** "/" diagonal in the lower left (expected for 2, not 3).
- **D:** vertical stroke on the upper left (expected for 9, 4, 5, 0; not 7 or 3).

Columns 8 and 9 are unused. The conv layers are unchanged from step 5. I will use the per-class presence rates to correct the signature table in the next classifier step.

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
    # conv2 (same as step 5): 0-11 blurred orientation maps (3 banks),
    # 12-15 stroke-ending detectors
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

    # ------------------------------------------------------------------
    # PROBE fc layer: three evidence features, each thresholded at 1.0.
    # output index k = bG + 2*bK + 4*bD  (k = 0..7), where
    #   bG = 1 if "vertical stroke on the lower right" response > 1.0
    #   bK = 1 if "'/' diagonal in the lower left"     response > 1.0
    #   bD = 1 if "vertical stroke on the upper left"  response > 1.0
    # (logit_k = sum_i b_i * (x_i - theta_i); outputs 8 and 9 are disabled)
    # ------------------------------------------------------------------
    NG = stroke_feat([(17.7, 15), (17.7, 19.5)])
    NK = stroke_feat([(12.5, 16), (9, 20.5)])
    ND = stroke_feat([(9.7, 7), (9.7, 12)])
    feats = [NG, NK, ND]
    thetas = [1.0, 1.0, 1.0]

    SCALE = 5.0
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)
    for kcls in range(8):
        bits = [(kcls >> i) & 1 for i in range(3)]
        for i in range(3):
            if bits[i]:
                fcw[kcls] += SCALE * feats[i]
                fcb[kcls] -= SCALE * thetas[i]
    fcb[8] = -1000.0
    fcb[9] = -1000.0

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
