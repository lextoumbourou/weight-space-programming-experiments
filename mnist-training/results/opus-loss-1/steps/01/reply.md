# Step 1: hand-built baseline network

**What this step tries.** The network is set up as a stroke-orientation feature extractor followed by template matching.

**conv1: oriented line detectors**
- Channels 0–3 detect lines at 4 orientations: horizontal, vertical, "\" and "/".
- Each kernel is a Gaussian ridge with zero mean, so solid blobs give no response.
- The positive part of each kernel is scaled to sum to 1. Each has a small negative bias to suppress weak responses.
- Channel 4 is a plain ink detector: a 5×5 average.
- Channels 5–7 are unused.

**conv2: places those maps on a 4×4 grid**
- I worked out the receptive-field geometry. Final cell r covers input rows of roughly 4r+4 to 4r+11, and columns follow the same rule. This tiles the 20×20 digit box.
- Channels 0–3 take a 3×3 average of each orientation map. This is a broad, shift-tolerant measure of how much stroke is present.
- Channels 4–7 use only the centre tap. This is a narrower test of whether a stroke is present.
- Channel 8 is a centre-tap ink-presence feature.

**fc: Gaussian-style template classifier**
- I describe each digit by hand as polylines and arcs in pixel coordinates.
- From those strokes I compute, by formula, the feature value I would expect in each (orientation, cell). This is done directly from the stroke description; nothing is passed through the network.
- With μ_d as the expected feature vector for digit d, the classifier uses logit_d = (f·μ_d − ½‖μ_d‖²)/σ².

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    # orientation angle phi: stroke direction (dy, dx) = (sin phi, cos phi), y = row (down)
    phis = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]  # horiz, vert, "\", "/"
    sig = 1.2
    for k, phi in enumerate(phis):
        K = np.zeros((5, 5))
        for u in range(-2, 3):          # row offset
            for v in range(-2, 3):      # col offset
                d = abs(u * math.cos(phi) - v * math.sin(phi))  # distance from line through centre
                K[u + 2, v + 2] = math.exp(-d * d / (2 * sig * sig))
        K -= K.mean()                   # zero-mean: flat ink regions give 0
        K /= K[K > 0].sum()             # an ideal stroke gives a response of about 1
        W1[k, 0] = K
        b1[k] = -0.15                   # suppress weak / off-orientation responses
    # channel 4: plain ink density (5x5 average)
    W1[4, 0] = 1.0 / 25.0
    b1[4] = 0.0
    # channels 5-7 unused (all zero)

    # ---------------- conv2: put the features on a 4x4 grid ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for k in range(4):
        W2[k, k, 1:4, 1:4] = 1.0 / 9.0   # ch 0-3: broad 3x3 average of orientation k
        W2[4 + k, k, 2, 2] = 1.0         # ch 4-7: centre tap only (narrow localisation)
    W2[8, 4, 2, 2] = 1.0                 # ch 8: ink presence (centre tap)
    # channels 9-15 unused

    # ---------------- digit stroke descriptions (pixel coords: y=row, x=col) ----------------
    def seg(p0, p1):
        (y0, x0), (y1, x1) = p0, p1
        L = math.hypot(y1 - y0, x1 - x0)
        n = max(1, int(math.ceil(L / 0.5)))
        th = math.atan2(y1 - y0, x1 - x0)
        ds = L / n
        return [(y0 + (y1 - y0) * (i + 0.5) / n, x0 + (x1 - x0) * (i + 0.5) / n, th, ds)
                for i in range(n)]

    def poly(*pts):
        out = []
        for a, b in zip(pts[:-1], pts[1:]):
            out += seg(a, b)
        return out

    def arc(cy, cx, ry, rx, t0, t1):
        # x = cx + rx cos t, y = cy - ry sin t (t in degrees, 90 = top)
        n = max(8, int(abs(t1 - t0) / 6))
        P = []
        for i in range(n + 1):
            t = math.radians(t0 + (t1 - t0) * i / n)
            P.append((cy - ry * math.sin(t), cx + rx * math.cos(t)))
        return poly(*P)

    strokes = {
        0: arc(14, 14, 9, 6.5, 0, 360),
        1: poly((4, 15), (23, 13)),
        2: arc(9, 14, 5, 5.5, 160, -30) + poly((11.5, 18.8), (23, 8), (23, 20)),
        3: arc(8.5, 13.5, 4.5, 5, 150, -90) + arc(18, 13.5, 5, 5.5, 90, -150),
        4: poly((4, 11), (15.5, 7), (15.5, 21)) + poly((5, 18), (23, 18)),
        5: poly((4, 20), (4, 10), (12, 9)) + arc(17, 13, 5.5, 6, 120, -140),
        6: poly((4, 18), (9, 12), (15, 9)) + arc(18, 14, 5, 5.5, 180, -180),
        7: poly((5, 8), (5, 20), (23, 12)),
        8: arc(9, 14, 4.5, 4.5, 0, 360) + arc(18.5, 14, 5, 5.5, 0, 360),
        9: arc(9, 14, 5, 5.5, 0, 360) + poly((9, 19.5), (23, 17)),
    }

    # ---------------- expected feature values per digit (computed from strokes) ----------------
    centres = [4 * r + 7.5 for r in range(4)]   # centre of final cell r in input pixels

    def soft(z, half):
        return np.array([math.exp(-(max(0.0, abs(z - c) - half)) ** 2 / (2 * 1.5 ** 2))
                         for c in centres])

    mu = np.zeros((10, 16, 4, 4))
    for d in range(10):
        A = np.zeros((4, 4, 4))
        B = np.zeros((4, 4, 4))
        I = np.zeros((4, 4))
        for (y, x, th, ds) in strokes[d]:
            sAy, sAx = soft(y, 3.0), soft(x, 3.0)
            sBy, sBx = soft(y, 2.0), soft(x, 2.0)
            spA = np.outer(sAy, sAx)
            spB = np.outer(sBy, sBx)
            I = np.maximum(I, spB)
            for k, phi in enumerate(phis):
                ow = max(0.0, math.cos(2 * (th - phi)))   # orientation match
                A[k] += ow * spA * ds / 6.0                # amount of stroke in the cell
                B[k] = np.maximum(B[k], ow * spB)          # stroke present in the cell
        mu[d, 0:4] = 0.35 * np.minimum(A, 1.0)   # 3x3 average features, about 0.35 for a full stroke
        mu[d, 4:8] = 0.7 * B                     # centre-tap features, about 0.7 peak
        mu[d, 8] = 0.55 * I                      # ink presence

    # ---------------- fc: Gaussian template classifier ----------------
    s2 = 0.4
    M = mu.reshape(10, 256)                      # (channel, row, col) flatten order
    Wfc = M / s2
    bfc = -0.5 * (M ** 2).sum(axis=1) / s2

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
```
