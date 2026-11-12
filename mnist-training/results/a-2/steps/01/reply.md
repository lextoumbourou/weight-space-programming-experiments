## Step 1: a baseline built from oriented strokes and hand-drawn digit templates

**What I'm trying.** The network gets a hand-set "orientation map" pipeline, followed by template matching in feature space.

- **conv1** detects local stroke orientation.
  - Channels 0–3 are line detectors at 0°, 45° (`\`), 90° and 135° (`/`). Each is an elongated Gaussian ridge made zero-mean.
  - Channel 4 is a blurred ink-intensity channel.
  - Channels 5–7 are off for now.
- **conv2** passes channels 0–4 through with a Gaussian blur. The max-pools then give a coarse 4×4 map of each orientation. The final cell centres sit at input rows and columns 7.5, 11.5, 15.5 and 19.5.
- **fc** holds one template per digit.
  - I describe each digit by hand as strokes: line segments and elliptical arcs in 28×28 pixel coordinates.
  - For every 4×4 cell and orientation channel, the template value is the stroke length near that cell, weighted by how well the stroke direction matches the channel's orientation. This is computed from the stroke geometry only, not by running the network on anything.
  - The templates are saturated, normalised to unit length and mean-subtracted across classes. A global scale sets the logit size.
- conv2 channels 5–15 are unused for now. I'll use them in later steps once I see the confusion matrix.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + intensity ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')   # V = row offset (down), U = col offset (right)
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)     # distance along line direction
        perp = -U * math.sin(th) + V * math.cos(th)   # distance across the line
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()                 # zero-sum: flat regions (ink or background) give ~0
        K /= K[K > 0].sum()           # a well-aligned stroke gives roughly 1
        W1[k, 0] = K
        b1[k] = -0.05                 # small threshold to suppress weak responses
    G = np.exp(-(U**2 + V**2) / 2.0)
    G /= G.sum()
    W1[4, 0] = G                      # channel 4: local ink density
    # channels 5-7: unused (all zero -> output 0)

    # ---------------- conv2: blur-and-pass-through of channels 0..4 ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    G2 = np.exp(-(U**2 + V**2) / (2 * 1.0**2))
    G2 /= G2.sum()
    for c in range(5):
        W2[c, c] = G2
    # channels 5-15 unused for now

    # ---------------- stroke descriptions of digits (x=col, y=row, 28x28 coords) ----------------
    def seg(p0, p1):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(L / 0.5))
        t = (np.arange(n) + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        ang = np.full(n, math.atan2(y1 - y0, x1 - x0))
        ds = np.full(n, L / n)
        return x, y, ang, ds

    def arc(cx, cy, rx, ry, t0, t1):
        t0r, t1r = math.radians(t0), math.radians(t1)
        n = max(8, int(abs(t1 - t0) / 3))
        t = t0r + (t1r - t0r) * (np.arange(n) + 0.5) / n
        dt = abs(t1r - t0r) / n
        x = cx + rx * np.cos(t)
        y = cy + ry * np.sin(t)
        dx = -rx * np.sin(t)
        dy = ry * np.cos(t)
        ang = np.arctan2(dy, dx)
        ds = np.hypot(dx, dy) * dt
        return x, y, ang, ds

    digits = {
        0: [arc(14, 14, 5.5, 8.5, 0, 360)],
        1: [seg((15, 4.5), (13, 23.5))],
        2: [arc(14, 10, 5, 5, 180, 390), seg((18.3, 12.5), (9, 22.5)), seg((9, 22.5), (20, 22.5))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [seg((10, 4.5), (8, 16)), seg((8, 16), (20, 16)), seg((17, 5), (17, 23.5))],
        5: [seg((10, 5), (19, 5)), seg((10, 5), (9.5, 13)), arc(13.5, 17.5, 5.5, 5, 228, 510)],
        6: [seg((17, 4.5), (10.5, 12)), seg((10.5, 12), (8.5, 18)), arc(13.5, 18, 5, 4.5, 0, 360)],
        7: [seg((8, 5), (20, 5)), seg((20, 5), (12, 23.5))],
        8: [arc(14, 9, 4, 4.5, 0, 360), arc(14, 18.5, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 4.5, 0, 360), seg((19, 10), (16, 23.5))],
    }

    # ---------------- templates in feature space (16 ch x 4 x 4) ----------------
    centers = [4 * i + 7.5 for i in range(4)]   # input-pixel centre of each final 4x4 cell
    sigma = 3.0
    T = np.zeros((10, 16, 4, 4))
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes])
        y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes])
        ds = np.concatenate([s[3] for s in strokes])
        for r in range(4):
            for c in range(4):
                prox = np.exp(-((x - centers[c])**2 + (y - centers[r])**2) / (2 * sigma**2)) * ds
                for k, th in enumerate(thetas):
                    tune = np.cos(a - th)**4          # orientation tuning (sign-invariant)
                    raw = np.sum(prox * tune)
                    T[d, k, r, c] = 1 - math.exp(-raw / 3.0)
                T[d, 4, r, c] = 0.5 * (1 - math.exp(-np.sum(prox) / 3.0))
    Tf = T.reshape(10, 256)
    Tf = Tf / np.linalg.norm(Tf, axis=1, keepdims=True)   # unit-norm templates
    Tf = Tf - Tf.mean(axis=0, keepdims=True)              # keep only class-discriminative part

    scale = 20.0
    Wfc = scale * Tf
    bfc = np.zeros(10)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
