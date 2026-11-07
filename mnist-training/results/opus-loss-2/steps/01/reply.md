## Step 1: hand-built stroke-orientation features matched against drawn digit templates

**What the layers do**

- **conv1 (stroke detectors).**
  - Channels 0–3 are line detectors at four orientations: horizontal, "\", vertical and "/". Each kernel has a Gaussian profile across the line and sums to zero inside a circular 5×5 window. It is scaled so that an ideal stroke 2–3 px wide gives a response of about 1. A small negative bias removes weak edge responses.
  - Channel 4 is a plain ink detector (3×3 average).
  - Channels 5–7 are unused (all zero) for now.
- **conv2 (spatial pooling).** Channels 0–4 each sum the matching conv1 map over the centre 3×3 of the kernel. After max-pooling, every feature says how much of that stroke type is in each cell of a 4×4 grid.
  - Each cell looks at about an 8×8 pixel region.
  - The cell centres sit at image rows and columns 7.5, 11.5, 15.5 and 19.5.
  - Channels 5–15 are unused (all zero).
- **fc (template matching).** I draw each digit by hand as polylines and arcs in pixel coordinates.
  - For each drawing I add up how much stroke of each orientation passes near each cell centre. This uses Gaussian spatial weights directly in feature space. The network is never run on anything.
  - I squash these totals into a "presence" score between 0 and 1.
  - I scale each digit's template to unit length and subtract the average over all digits. That average-subtracted template is the class weight vector.

The overall scale of the logits is a guess, and I will adjust it from the loss.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    # Preferred line directions (x right, y down):
    # 0 = horizontal, pi/4 = "\" (down-right), pi/2 = vertical, 3pi/4 = "/"
    phis = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]
    for k, phi in enumerate(phis):
        vals = {}
        for r in range(5):
            for c in range(5):
                x, y = c - 2, r - 2
                if x * x + y * y <= 5:  # circular window
                    # perpendicular distance from the line through the centre
                    d = abs(-math.sin(phi) * x + math.cos(phi) * y)
                    vals[(r, c)] = math.exp(-d * d / 2.0)
        m = np.mean(list(vals.values()))
        for (r, c), v in vals.items():
            W1[k, 0, r, c] = v - m           # zero-sum kernel: ignores flat ink
        W1[k] /= W1[k][W1[k] > 0].sum()      # ideal stroke -> response ~1
        b1[k] = -0.15                         # suppress weak edge responses
    # channel 4: ink detector (3x3 mean)
    W1[4, 0, 1:4, 1:4] = 1.0 / 9.0
    b1[4] = 0.0
    # channels 5-7 unused (zero)

    # ---------------- conv2: spatial summing of each conv1 map ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    for k in range(5):
        W2[k, k, 1:4, 1:4] = 1.0 / 3.0   # sum over centre 3x3 of the pooled map
    # channels 5-15 unused (zero)

    # ---------------- digit stroke drawings (pixel coords, x=col, y=row) ----------------
    def seg(p0, p1):
        p0 = np.array(p0, float); p1 = np.array(p1, float)
        L = np.linalg.norm(p1 - p0)
        n = max(2, int(L / 0.25) + 1)
        t = np.linspace(0, 1, n)[:, None]
        return p0 + (p1 - p0) * t

    def arc(cx, cy, rx, ry, t0, t1):
        n = int(abs(t1 - t0) * max(rx, ry) / 0.25) + 2
        t = np.linspace(t0, t1, n)
        return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], axis=1)

    PI = math.pi
    digits = {
        0: [arc(14, 14, 6, 9.5, 0, 2 * PI)],
        1: [seg((15.5, 4.5), (12.5, 23.5))],
        2: [arc(14, 10, 5.5, 5, -PI, 0.5),
            seg((18.8, 12.4), (8, 23)),
            seg((8, 23), (21, 22.5))],
        3: [arc(13.5, 8.8, 5, 4.3, -2.6, PI / 2),
            seg((10.5, 13.2), (13.5, 13.1)),
            arc(13.5, 18.5, 6, 5.4, -PI / 2, 2.6)],
        4: [seg((15, 4.5), (7.5, 17)),
            seg((7.5, 17), (21, 17)),
            seg((17.5, 9), (17, 23.5))],
        5: [seg((19.5, 4.5), (10.5, 4.5)),
            seg((10.5, 4.5), (9.5, 12.5)),
            arc(13.5, 17.2, 6, 5.8, -2.2, 2.6)],
        6: [arc(19, 16, 9.5, 11.5, -1.75, -PI),
            arc(14, 18.3, 5, 5, 0, 2 * PI)],
        7: [seg((8, 5), (20.5, 5)),
            seg((20.5, 5), (12.5, 23.5))],
        8: [arc(14, 9, 4.5, 4.5, 0, 2 * PI),
            arc(14, 18.5, 5.5, 5, 0, 2 * PI)],
        9: [arc(13.5, 9.5, 5, 5, 0, 2 * PI),
            seg((18.5, 10), (16.5, 23.5))],
    }

    # Cell centres of the final 4x4 grid in input-pixel coordinates
    centres = 7.5 + 4.0 * np.arange(4)
    sig = 3.0

    def template(strokes):
        T = np.zeros((5, 4, 4))
        for pts in strokes:
            d = pts[1:] - pts[:-1]
            mid = 0.5 * (pts[1:] + pts[:-1])
            ds = np.linalg.norm(d, axis=1)
            ang = np.arctan2(d[:, 1], d[:, 0])
            # spatial weight of each sample for each cell (i=row, j=col)
            gy = np.exp(-(mid[:, 1][:, None] - centres[None, :]) ** 2 / (2 * sig ** 2))
            gx = np.exp(-(mid[:, 0][:, None] - centres[None, :]) ** 2 / (2 * sig ** 2))
            g = gy[:, :, None] * gx[:, None, :]          # (N,4,4)
            for k, phi in enumerate(phis):
                ow = np.maximum(0.0, np.cos(2 * (ang - phi))) ** 2
                T[k] += np.tensordot(ds * ow, g, axes=(0, 0))
            T[4] += np.tensordot(ds, g, axes=(0, 0))      # ink
        return 1.0 - np.exp(-T / 3.0)                      # saturate -> presence

    temps = np.zeros((10, 5, 4, 4))
    for dgt in range(10):
        t = template(digits[dgt])
        temps[dgt] = t / np.linalg.norm(t)
    temps -= temps.mean(axis=0, keepdims=True)

    # ---------------- fc: template correlation ----------------
    scale = 4.0
    Wf = np.zeros((10, 256), dtype=np.float64)
    for dgt in range(10):
        for ch in range(5):
            Wf[dgt, ch * 16:(ch + 1) * 16] = scale * temps[dgt, ch].reshape(16)
    bf = np.zeros(10, dtype=np.float64)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
