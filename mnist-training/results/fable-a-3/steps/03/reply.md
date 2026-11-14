**Step 3 plan.** Accuracy rose to 70% once absence of strokes counted, so I am leaning further on that vote and fixing three things the confusion matrix points to:

1. **Stronger presence/absence vote** (0.08 → 0.16), with the correlation vote reduced slightly (0.30 → 0.25). At 0.08 a single mismatched feature costs only 0.16 logit.
2. **Slant tolerance.** 0→2, 1→2 and 4→9 look like slanted strokes lighting a neighbouring orientation channel that the template marks as "must be absent". Where a template expects a stroke in a cell, the two neighbouring orientations in that cell are now "don't care" (weight ≈ 0). The default slant of the drawings is also raised a little.
3. **Bias corrections from the column sums.** 3 is predicted about 630 times too often and 1 about 290 times too often, while 4, 8 and 0 are under-predicted. I am applying modest biases in the opposite direction, at roughly half the size the counts suggest, because the other changes will also shift this.

The conv layers are unchanged from step 2.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors x 2 thresholds
    #   channel k   (k=0..3): orientation k, bias -t0
    #   channel k+4         : same filter,  bias -t1
    #   orientation 0: horizontal stroke, 1: "/" , 2: vertical, 3: "\"
    #   pooled(k) - pooled(k+4) = clip(resp - t0, 0, t1 - t0)  -> saturated map M_k
    # ------------------------------------------------------------------
    prof = np.array([-0.75, 0.25, 1.0, 0.25, -0.75])   # across-stroke profile (zero sum)
    Hf = np.tile(prof[:, None], (1, 5))                # horizontal stroke detector
    Vf = Hf.T.copy()                                   # vertical stroke detector
    dv = [1.0, 0.4, -0.45, -0.9, -0.95]                # diagonal profile by |offset| (zero sum)
    D1 = np.zeros((5, 5))
    D2 = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            D1[r, c] = dv[abs((r - 2) + (c - 2))]      # "/" : ridge on r + c = 4
            D2[r, c] = dv[abs((r - 2) - (c - 2))]      # "\" : ridge on r = c
    filts = [Hf, D1, Vf, D2]
    t0, t1 = 0.45, 0.75                                # response of an ideal stroke is ~1
    w1 = np.zeros((8, 1, 5, 5))
    b1 = np.zeros(8)
    for k in range(4):
        w1[k, 0] = filts[k] / 5.0
        b1[k] = -t0
        w1[k + 4, 0] = filts[k] / 5.0
        b1[k + 4] = -t1

    # ------------------------------------------------------------------
    # conv2:
    #   channels 0..3 : stroke amount of orientation k in a tapered 5x5 window (count)
    #   channels 4..7 : emptiness  E_k = ReLU(1 - amount/tau)  (1 = no stroke of orientation k here)
    #   channels 8..15: unused (zero)
    # ------------------------------------------------------------------
    k1 = np.array([0.5, 1.0, 1.0, 1.0, 0.5])
    K2 = np.outer(k1, k1)
    tau = 2.5                                          # stroke mass at which "present" saturates
    w2 = np.zeros((16, 8, 5, 5))
    b2 = np.zeros(16)
    for k in range(4):
        w2[k, k] = K2 / (t1 - t0)                      # count: + low-threshold copy
        w2[k, k + 4] = -K2 / (t1 - t0)                 #        - high-threshold copy
        w2[4 + k, k] = -K2 / ((t1 - t0) * tau)         # emptiness: 1 - count/tau
        w2[4 + k, k + 4] = K2 / ((t1 - t0) * tau)
        b2[4 + k] = 1.0

    # ------------------------------------------------------------------
    # hand-drawn digit prototypes (u right, v down, digit spans v in [-1, 1])
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=48):
        # angle 0 = right, 90 = bottom, 180 = left, 270 = top (v points down)
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    def poly(*pts):
        return np.array(pts, dtype=float)

    tt = np.linspace(0, 2 * np.pi, 96)
    eight = np.stack([0.45 * np.sin(2 * tt) * (1 + 0.12 * np.cos(tt)), np.cos(tt)], 1)

    SL = 0.18   # default rightward lean of the drawings
    digits = {
        0: ([arc(0, 0, 0.62, 1.0, 0, 360)], SL),
        1: ([poly((0, -1), (0, 1))], 0.25),
        2: ([arc(0, -0.5, 0.5, 0.5, 200, 400),                 # top hook
             poly((0.38, -0.18), (-0.55, 0.97)),               # diagonal down-left
             poly((-0.55, 0.97), (0.6, 0.97))], SL),           # base
        3: ([arc(-0.05, -0.5, 0.48, 0.5, 200, 450),            # upper bowl
             arc(-0.05, 0.5, 0.55, 0.5, 270, 520)], SL),       # lower bowl
        4: ([poly((-0.4, -1.0), (-0.6, 0.1)),                  # left arm
             poly((-0.6, 0.1), (0.65, 0.1)),                   # crossbar
             poly((0.3, -0.9), (0.3, 1.0))], SL),              # stem
        5: ([poly((0.55, -1.0), (-0.3, -1.0)),                 # top bar
             poly((-0.3, -1.0), (-0.4, -0.1)),                 # short vertical
             arc(-0.05, 0.42, 0.55, 0.58, 230, 520)], SL),     # bowl
        6: ([poly((0.35, -1.0), (-0.1, -0.6), (-0.4, -0.1), (-0.5, 0.47)),  # descending curve
             arc(0, 0.47, 0.5, 0.53, 0, 360)], SL),            # bottom loop
        7: ([poly((-0.6, -1.0), (0.5, -1.0)),                  # top bar
             poly((0.5, -1.0), (0.05, 1.0))], SL),             # diagonal stem
        8: ([eight], SL),                                      # figure eight with X crossing
        9: ([arc(-0.05, -0.5, 0.45, 0.5, 0, 360),              # top loop
             poly((0.4, -0.6), (0.3, 1.0))], SL),              # stem
    }

    centres = np.array([7.5, 11.5, 15.5, 19.5])   # input-pixel centres of the 4 final cells

    def Kcount(d):
        # spatial window of a count cell (max over the 2x2 pooled conv2 units)
        return np.clip((6.5 - np.abs(d)) / 3.0, 0.0, 1.0)

    def Kpres(d):
        # spatial window of a presence cell (stroke must be seen by all pooled units)
        return np.clip((4.5 - np.abs(d)) / 2.0, 0.0, 1.0)

    def tune(delta):
        # saturated orientation tuning of the conv1 detectors (degrees off preferred)
        return np.clip((41.0 - delta) / 14.0, 0.0, 1.0)

    mass = [0.7, 0.85, 0.7, 0.85]                 # pooled cells lit per pixel of stroke length

    def stroke_points(strokes, slant):
        # turn the drawing into small directed stroke elements, centred like MNIST
        segs = []
        for s in strokes:
            s = np.array(s, dtype=float).copy()
            s[:, 0] -= slant * s[:, 1]            # lean to the right (top shifts right)
            segs.append(s)
        allp = np.concatenate(segs)
        sc = 17.0 / (allp[:, 1].max() - allp[:, 1].min())   # 20px box minus stroke width
        pts = []
        for s in segs:
            s = s * sc
            for a, b in zip(s[:-1], s[1:]):
                L = float(np.hypot(b[0] - a[0], b[1] - a[1]))
                if L < 1e-9:
                    continue
                n = max(1, int(math.ceil(L / 0.25)))
                th = math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0])) % 180.0
                for m in range(n):
                    p = a + (b - a) * (m + 0.5) / n
                    pts.append((p[0], p[1], th, L / n))
        pts = np.array(pts)
        ds = pts[:, 3]
        x = pts[:, 0] - (pts[:, 0] * ds).sum() / ds.sum() + 13.5   # centre of mass -> image centre
        y = pts[:, 1] - (pts[:, 1] * ds).sum() / ds.sum() + 13.5
        return x, y, pts[:, 2], ds

    def draw(x, y, th, ds, Kfun):
        # draw the strokes into the (orientation, row, col) grid with spatial brush Kfun
        Ky = Kfun(y[:, None] - centres[None, :])
        Kx = Kfun(x[:, None] - centres[None, :])
        T = np.zeros((4, 4, 4))
        for k in range(4):
            d = np.abs(th - 45.0 * k)
            d = np.minimum(d, 180.0 - d)
            w = tune(d) * mass[k] * ds
            T[k] = np.einsum('n,ni,nj->ij', w, Ky, Kx)
        return T

    alpha = 0.25     # scale of the correlation (count) vote
    aB = 0.16        # scale of the presence/absence vote

    # bias corrections read off the step-2 confusion matrix (3 and 1 over-predicted;
    # 4, 8 and 0 under-predicted)
    extra_bias = np.array([0.10, -0.10, 0.0, -0.30, 0.20, 0.0, 0.0, 0.0, 0.20, 0.0])

    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for d in range(10):
        strokes, sl = digits[d]
        x, y, th, ds = stroke_points(strokes, sl)

        # (a) correlation template on count channels 0..3 (unit length)
        T = draw(x, y, th, ds, Kcount)
        T = T / np.linalg.norm(T)
        fcw[d, 0:64] = alpha * T.reshape(-1)

        # (b) presence/absence vote on emptiness channels 4..7
        #     P = how strongly this digit expects a stroke of that orientation in that cell
        P = np.clip(draw(x, y, th, ds, Kpres) / tau, 0.0, 1.0)
        # slant tolerance: next to an expected stroke, the two neighbouring orientations
        # in the same cell become "don't care" (P = 0.5 -> q = 0.5 -> weight 0)
        nb = np.maximum(np.roll(P, 1, axis=0), np.roll(P, -1, axis=0))
        P = np.maximum(P, 0.5 * nb)
        q = 0.12 + 0.76 * P
        # logit = sum log q  +  E * log((1-q)/q)   (E = 1 when the stroke is missing)
        fcw[d, 64:128] = aB * np.log((1.0 - q) / q).reshape(-1)
        fcb[d] = aB * np.log(q).sum() + extra_bias[d]

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
