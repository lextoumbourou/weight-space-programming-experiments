**Step 1 plan.** This is a deliberately simple baseline, so the first confusion matrix tells me whether the feature scale and templates are roughly right.

- **conv1:** four oriented stroke detectors (horizontal, "/", vertical, "\"), each stored twice with a low and a high threshold. The difference of the two copies after pooling is a saturated "stroke of this orientation is here" signal in [0, 1], which should be largely independent of pen thickness.
- **conv2:** channels 0–3 take that difference and sum it over a tapered 5x5 window. After the last pooling, each of the 4x4 cells says roughly how much stroke of each orientation lies in a ~12 px window around it. Channels 4–15 are left at zero for later steps.
- **fc:** for each digit I describe a prototype by hand as a few lines and arcs and draw it straight into the (orientation, cell) weight grid. Each template is scaled to unit length, so the logit is a normalised correlation and a mis-guessed overall feature scale does not favour heavy or light digits. Biases are zero.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors x 2 thresholds
    #   channel k   (k=0..3): orientation k, bias -t0
    #   channel k+4         : same filter,  bias -t1
    #   orientation 0: horizontal stroke, 1: "/" , 2: vertical, 3: "\"
    #   pooled(k) - pooled(k+4) = clip(resp - t0, 0, t1 - t0)  -> saturated
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
    # conv2: channels 0..3 = tapered 5x5 sum of the saturated orientation map
    #        channels 4..15 unused (zero) for now
    # ------------------------------------------------------------------
    k1 = np.array([0.5, 1.0, 1.0, 1.0, 0.5])
    K2 = np.outer(k1, k1)
    w2 = np.zeros((16, 8, 5, 5))
    b2 = np.zeros(16)
    for k in range(4):
        w2[k, k] = K2 / (t1 - t0)          # + low-threshold copy
        w2[k, k + 4] = -K2 / (t1 - t0)     # - high-threshold copy  => saturation at 1

    # ------------------------------------------------------------------
    # fc: hand-drawn stroke templates, drawn into (orientation, 4x4 cell) space
    # coordinates: u to the right, v downwards, digit spans v in [-1, 1]
    # ------------------------------------------------------------------
    def arc(cx, cy, rx, ry, a0, a1, n=48):
        # angle 0 = right, 90 = bottom, 180 = left, 270 = top (v points down)
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    def poly(*pts):
        return np.array(pts, dtype=float)

    tt = np.linspace(0, 2 * np.pi, 96)
    eight = np.stack([0.45 * np.sin(2 * tt) * (1 + 0.12 * np.cos(tt)), np.cos(tt)], 1)

    digits = {
        0: ([arc(0, 0, 0.62, 1.0, 0, 360)], 0.12),
        1: ([poly((0, -1), (0, 1))], 0.18),
        2: ([arc(0, -0.5, 0.5, 0.5, 200, 400),                 # top hook
             poly((0.38, -0.18), (-0.55, 0.97)),               # diagonal down-left
             poly((-0.55, 0.97), (0.6, 0.97))], 0.12),         # base
        3: ([arc(-0.05, -0.5, 0.48, 0.5, 200, 450),            # upper bowl
             arc(-0.05, 0.5, 0.55, 0.5, 270, 520)], 0.12),     # lower bowl
        4: ([poly((-0.4, -1.0), (-0.6, 0.1)),                  # left arm
             poly((-0.6, 0.1), (0.65, 0.1)),                   # crossbar
             poly((0.3, -0.9), (0.3, 1.0))], 0.12),            # stem
        5: ([poly((0.55, -1.0), (-0.3, -1.0)),                 # top bar
             poly((-0.3, -1.0), (-0.4, -0.1)),                 # short vertical
             arc(-0.05, 0.42, 0.55, 0.58, 230, 520)], 0.12),   # bowl
        6: ([poly((0.35, -1.0), (-0.1, -0.6), (-0.4, -0.1), (-0.5, 0.47)),  # descending curve
             arc(0, 0.47, 0.5, 0.53, 0, 360)], 0.12),          # bottom loop
        7: ([poly((-0.6, -1.0), (0.5, -1.0)),                  # top bar
             poly((0.5, -1.0), (0.05, 1.0))], 0.12),           # diagonal stem
        8: ([eight], 0.12),                                    # figure eight with X crossing
        9: ([arc(-0.05, -0.5, 0.45, 0.5, 0, 360),              # top loop
             poly((0.4, -0.6), (0.3, 1.0))], 0.12),            # stem
    }

    centres = np.array([7.5, 11.5, 15.5, 19.5])   # input-pixel centres of the 4 final cells

    def Kwin(d):
        # effective spatial window of one final cell (conv2 taper + pooling)
        return np.clip((6.5 - np.abs(d)) / 3.0, 0.0, 1.0)

    def tune(delta):
        # saturated orientation tuning of the conv1 detectors (degrees off preferred)
        return np.clip((41.0 - delta) / 14.0, 0.0, 1.0)

    mass = [0.7, 0.85, 0.7, 0.85]                 # pooled cells lit per pixel of stroke length

    def template(strokes, slant):
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
        # centre the drawing by its centre of mass, as MNIST does
        x = pts[:, 0] - (pts[:, 0] * ds).sum() / ds.sum() + 13.5
        y = pts[:, 1] - (pts[:, 1] * ds).sum() / ds.sum() + 13.5
        Ky = Kwin(y[:, None] - centres[None, :])
        Kx = Kwin(x[:, None] - centres[None, :])
        T = np.zeros((4, 4, 4))
        for k in range(4):
            d = np.abs(pts[:, 2] - 45.0 * k)
            d = np.minimum(d, 180.0 - d)
            w = tune(d) * mass[k] * ds
            T[k] = np.einsum('n,ni,nj->ij', w, Ky, Kx)
        return T

    alpha = 0.3                                   # logit scale (temperature)
    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for d in range(10):
        strokes, sl = digits[d]
        T = template(strokes, sl)
        T = T / np.linalg.norm(T)                 # unit-length template -> normalised correlation
        fcw[d, :64] = alpha * T.reshape(-1)       # channels 0..3, (channel,row,col) order

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
