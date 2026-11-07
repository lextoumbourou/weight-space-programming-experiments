## Step 1: a hand-built baseline

**Approach.** The network compares each image against stroke templates I draw by hand.

**conv1: oriented line detectors.** Each layer-1 filter matches straight stroke pieces at one angle.
- Channels 0–3 detect lines at 0°, 45°, 90° and 135°.
  - Each filter has a Mexican-hat profile across the line and is constant along it.
  - Each filter is zero-mean, so flat ink or flat background gives no response.
  - Each is scaled so that a well-matched stroke 3 px wide gives a response of about 1.
- Channel 4 is a Gaussian blur, which acts as an "ink present" detector.
- Channels 5–7 are unused for now.

**conv2: copy into a 4×4 grid.** conv2 passes channels 0–4 straight through using only the centre weight. After the final max-pool, each of the 4×4 cells reports the strongest response in one non-overlapping 4×4-pixel block of stroke centres. The blocks start at input rows and columns 6, 10, 14 and 18. The 256 features therefore mean "how much stroke of orientation k is in grid cell (i, j)".

**fc: nearest template.**
- I describe each digit as hand-drawn polylines and ellipses in pixel coordinates.
- A small renderer turns those strokes into an expected feature map T_d. For each grid cell it records which orientations a stroke passing through that cell would activate. This renderer is my own geometry and never runs the network.
- The logits are a scaled nearest-template score: logit_d = β(f·T_d − κ/2·‖T_d‖²).
  - κ ≈ 0.7 is my guess at how strong real responses are relative to the template's value of 1.
  - β sets how confident the network is. I will tune it from the validation loss.

```python
import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors (ch 0-3) + ink/blur detector (ch 4)
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]          # line direction angle in (x=col, y=row-down) coords
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)   # ys: row offset, xs: col offset
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys        # signed distance from the line through centre
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))  # Mexican-hat profile across the line
        w = w - w.mean()                                # zero-mean: no response to flat ink/background
        w = w / w[w > 0].sum()                          # matched stroke -> response ~1
        W1[k, 0] = w
        b1[k] = -0.15                                   # suppress weak/partial responses
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()    # Gaussian blur = ink presence
    W1[4, 0] = g
    b1[4] = -0.1
    # channels 5-7 unused (zero weights, zero bias -> output 0)

    # ------------------------------------------------------------------
    # conv2: pass-through of conv1 channels 0-4 (centre tap only)
    # final 4x4 cell (i,j) = max over input stroke centres rows 4i+6..4i+9, cols 4j+6..4j+9
    # ------------------------------------------------------------------
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for c in range(5):
        W2[c, c, 2, 2] = 1.0

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes, points are (x=col, y=row) in the 28x28 image
    # ------------------------------------------------------------------
    def ell(cx, cy, rx, ry, a0=0.0, a1=360.0, n=28):
        a = np.radians(np.linspace(a0, a1, n))
        return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in a]

    digits = {
        0: [ell(14, 14, 5.5, 8.5)],
        1: [[(15.5, 5), (12.5, 23)]],
        2: [[(9, 9), (10.5, 6), (14, 5), (17.5, 6), (19, 9), (18, 12), (15, 15.5),
             (11, 19.5), (9, 22), (14, 22), (20, 22)]],
        3: [[(9, 6), (13, 5), (17, 5.5), (19, 8), (18, 11), (14, 13.5), (18, 15.5),
             (19.5, 18.5), (18, 21.5), (14, 23), (9, 22)]],
        4: [[(10, 5), (9.5, 15), (20, 15)], [(18, 5), (17, 23)]],
        5: [[(19, 5), (11, 5), (10, 13), (14, 12), (18, 13.5), (19.5, 17), (18, 21),
             (14, 23), (9, 21.5)]],
        6: [[(17, 5), (13, 8), (10.5, 12), (9.5, 16), (10, 20), (13, 23), (16.5, 22.5),
             (18.5, 19), (17.5, 15.5), (14, 14), (10.5, 16)]],
        7: [[(9, 5), (19.5, 5), (17, 11), (14.5, 17), (13, 23)]],
        8: [ell(14, 9.5, 4.0, 4.2), ell(14, 18.5, 5.0, 4.5)],
        9: [ell(14, 9.5, 4.5, 4.3), [(18.5, 10), (17.5, 16), (16, 23)]],
    }

    def cov(v, i):
        # how strongly a stroke at coordinate v is seen by grid cell i
        # cell i covers stroke centres 4i+6..4i+9, filter core reaches ~1.5 px further
        lo, hi = 4 * i + 4.5, 4 * i + 10.5
        dist = max(lo - v, 0.0, v - hi)
        return max(0.0, 1.0 - dist / 1.5)

    def render(polys):
        T = np.zeros((5, 4, 4))
        for P in polys:
            P = np.array(P, float)
            for a, b in zip(P[:-1], P[1:]):
                dx, dy = b - a
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(dy, dx)
                o = [max(0.0, math.cos(2 * (phi - math.radians(th)))) for th in thetas]
                n = max(2, int(L / 0.5) + 1)
                for t in np.linspace(0, 1, n):
                    x, y = a + t * (b - a)
                    hy = [cov(y, i) for i in range(4)]
                    hx = [cov(x, j) for j in range(4)]
                    for i in range(4):
                        for j in range(4):
                            sp = hy[i] * hx[j]
                            if sp <= 0:
                                continue
                            for k in range(4):
                                T[k, i, j] = max(T[k, i, j], o[k] * sp)
                            T[4, i, j] = max(T[4, i, j], sp)
        return T

    # ------------------------------------------------------------------
    # fc: nearest-template scoring  logit_d = beta*(f.T_d - kappa/2 ||T_d||^2)
    # ------------------------------------------------------------------
    beta, kappa = 0.4, 0.7
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        T = render(digits[d])
        full = np.zeros((16, 4, 4))
        full[:5] = T                     # conv2 channels 0-4 carry the features
        Wf[d] = beta * full.reshape(-1)  # (channel,row,col) flatten order
        bf[d] = -beta * kappa * 0.5 * np.sum(T ** 2)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
