# Step 1: a hand-built orientation-template classifier

**Plan**

- **conv1 (8 filters):** oriented line detectors at 0°, 22.5°, …, 157.5°. Each filter is zero-mean, so flat ink blobs and plain stroke edges give little or no response. A stroke about 2.5 px wide, aligned with the filter, gives a response of about 1. The bias of −0.2 removes weak responses.
- **conv2 (16 channels):** no new features yet. It only pools each orientation over space.
  - Channels 0–7 sum a 3×3 patch of the pooled conv1 map for orientation o. Each of the final 4×4 cells then covers stroke centres in an 8-pixel band. The bands step by 4 pixels and together span pixels 4–23 in each direction.
  - Channels 8–15 take only the centre tap, a sharper 4-pixel band.
- **fc (templates):** each digit is described as a few strokes (lines and elliptical arcs) in a normalised box with a slight rightward slant.
  - From each stroke's geometry I compute which orientation channel and which grid cell it should activate. This gives an expected 256-dimensional feature profile per digit.
  - The fc weights are these profiles after subtracting the mean over digits and normalising each to unit length. This is a cosine-similarity template matcher.
  - All biases start at 0.

The network is never run and no images are drawn. The templates are computed directly from the stroke descriptions.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    # Orientation o has line direction theta = o*22.5 deg in image coords
    # (x = column to the right, y = row downward).
    thetas = np.arange(8) * np.pi / 8
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    yy, xx = np.mgrid[-2:3, -2:3]          # dy = row offset, dx = column offset
    for o in range(8):
        nx, ny = -np.sin(thetas[o]), np.cos(thetas[o])   # unit normal to the line
        d = xx * nx + yy * ny                            # perpendicular distance
        g = np.exp(-d ** 2 / (2 * 1.1 ** 2))             # ridge profile
        g -= g.mean()                                    # zero-mean: blobs/edges ~ 0
        g /= (g * (np.abs(d) <= 1.25)).sum()             # ideal ~2.5px stroke -> 1
        w1[o, 0] = g
    b1 = np.full(8, -0.2, np.float32)                    # suppress weak responses

    # ---------------- conv2: spatial pooling per orientation ----------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    for o in range(8):
        w2[o, o, 1:4, 1:4] = 1.0     # ch 0-7: broad (8-pixel-band) cells
        w2[8 + o, o, 2, 2] = 1.0     # ch 8-15: sharp (4-pixel-band) cells
    b2 = np.zeros(16, np.float32)

    # ---------------- digit stroke descriptions ----------------
    # Coordinates (u, v) in [-1,1]^2, v downward (v=-1 is the top of the digit).
    def line(a, b, n=40):
        t = np.linspace(0, 1, n)[:, None]
        return np.array(a)[None] * (1 - t) + np.array(b)[None] * t

    def arc(cx, cy, rx, ry, a0, a1, n=120):
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    digits = {
        0: [arc(0, 0, 0.85, 1.0, 0, 360)],
        1: [line((0.15, -1), (-0.15, 1))],
        2: [arc(0, -0.45, 0.8, 0.55, 180, 380),
            line((0.75, -0.26), (-0.8, 0.95)),
            line((-0.8, 0.95), (0.9, 0.95))],
        3: [arc(0, -0.5, 0.75, 0.5, 200, 450),
            arc(0, 0.5, 0.8, 0.5, 270, 520)],
        4: [line((-0.25, -1), (-0.8, 0.35)),
            line((-0.8, 0.35), (0.8, 0.35)),
            line((0.45, -0.9), (0.45, 1))],
        5: [line((0.8, -1), (-0.45, -1)),
            line((-0.45, -1), (-0.55, -0.1)),
            arc(-0.05, 0.45, 0.75, 0.55, 240, 510)],
        6: [line((0.45, -1), (-0.65, 0.35)),
            arc(0, 0.45, 0.68, 0.55, 0, 360)],
        7: [line((-0.8, -1), (0.8, -1)),
            line((0.8, -1), (-0.15, 1))],
        8: [arc(0, -0.5, 0.6, 0.5, 0, 360),
            arc(0, 0.5, 0.75, 0.5, 0, 360)],
        9: [arc(0, -0.45, 0.7, 0.55, 0, 360),
            line((0.7, -0.45), (0.35, 1))],
    }

    def to_xy(p):
        # map normalised box to pixel coords, with a slight rightward slant at top
        u, v = p[:, 0], p[:, 1]
        return np.stack([14 + 7 * u - 1.5 * v, 14 + 9.5 * v], 1)

    def memb(z, lo, hi):
        # soft membership of coordinate z in band [lo, hi]
        out = np.maximum(0, np.maximum(lo - z, z - hi))
        return np.clip(1 - out / 2.0, 0, 1)

    # ---------------- expected features per digit ----------------
    F = np.zeros((10, 16, 4, 4))
    for dgt, polys in digits.items():
        for poly in polys:
            p = to_xy(poly)
            mid = 0.5 * (p[1:] + p[:-1])
            dv = p[1:] - p[:-1]
            ds = np.linalg.norm(dv, axis=1)
            ang = np.arctan2(dv[:, 1], dv[:, 0])
            for o in range(8):
                tune = np.maximum(0, np.cos(2 * (ang - thetas[o]))) ** 2
                for i in range(4):
                    myA = memb(mid[:, 1], 4 * i + 4, 4 * i + 11)
                    myB = memb(mid[:, 1], 4 * i + 6, 4 * i + 9)
                    for j in range(4):
                        mxA = memb(mid[:, 0], 4 * j + 4, 4 * j + 11)
                        mxB = memb(mid[:, 0], 4 * j + 6, 4 * j + 9)
                        F[dgt, o, i, j] += np.sum(ds * tune * myA * mxA)
                        F[dgt, 8 + o, i, j] += np.sum(ds * tune * myB * mxB)

    # ---------------- fc: normalised, mean-centred templates ----------------
    Fv = F.reshape(10, 256)                   # (channel,row,col) flatten order
    D = Fv - Fv.mean(axis=0, keepdims=True)
    D /= np.linalg.norm(D, axis=1, keepdims=True) + 1e-8
    alpha = 1.0                               # logit scale
    wfc = (alpha * D).astype(np.float32)
    bfc = np.zeros(10, np.float32)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2,
        "conv2.bias": b2,
        "fc.weight": wfc,
        "fc.bias": bfc,
    }
```
