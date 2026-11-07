## Step 4: blur the templates

Accuracy has stalled at about 62–63% across three settings of the template-size penalty α. The main limit now looks like the templates themselves, not the penalty.

My templates are crisp: a cell is marked as "fully present" only if a stroke passes through it exactly. Real handwritten digits vary in position and shape. The average real feature map for a class would therefore be blurrier: a stroke shows up in a given cell only some of the time. Nearest-template classification works best when each template looks like that blurry class average.

So in this step I widen the spatial soft-window fall-off of every template:
- **Before:** beyond the window edge, the template value fell off with a Gaussian of width 1 pixel.
- **Now:** it falls off with width 1.8 pixels, for both the tight and wide channels.
- **Orientation tuning:** this is also broadened, from `cos(2Δ)^1.5` to `cos(2Δ)^1`, where Δ is the angle between the stroke and the filter.

I keep α = 0.8 and s = 0.6, and the convolution filters are unchanged. That way this step isolates the effect of blurring the templates.

```python
import numpy as np
import math

# ---------------------------------------------------------------------------
# Stroke helpers: return arrays of (x=col, y=row) points in 28x28 coordinates
# ---------------------------------------------------------------------------
def _line(p0, p1, step=0.25):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    n = max(2, int(L / step) + 1)
    t = np.linspace(0, 1, n)
    return np.stack([p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t], 1)

def _arc(cx, cy, rx, ry, t0, t1, step=0.25):
    # t in degrees, math convention (y up), converted to row coordinates (y down)
    L = abs(t1 - t0) * math.pi / 180 * max(rx, ry)
    n = max(2, int(L / step) + 2)
    t = np.radians(np.linspace(t0, t1, n))
    return np.stack([cx + rx * np.cos(t), cy - ry * np.sin(t)], 1)

def _bez(p0, p1, p2, n=120):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = np.array(p0, float), np.array(p1, float), np.array(p2, float)
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

# Hand-described digit skeletons (digit roughly occupies rows/cols 4..23)
def _digit_strokes():
    S = {}
    S[0] = [_arc(14, 14, 6, 9.5, 0, 360)]
    S[1] = [_line((16, 4), (12.5, 23))]
    S[2] = [_arc(14, 9, 5.5, 4.5, 160, -30), _line((18.8, 11.3), (8, 22)), _line((8, 22), (21, 22))]
    S[3] = [_arc(13, 9, 6, 5, 150, -90), _arc(13, 18.5, 7, 5, 90, -150)]
    S[4] = [_line((10, 4), (7, 16)), _line((7, 16.5), (21, 16.5)), _line((17, 8), (17, 23))]
    S[5] = [_line((10, 4.5), (20, 4.5)), _line((10, 4.5), (9, 12)), _arc(13, 17, 7, 6, 135, -150)]
    S[6] = [_bez((18, 4), (9, 7), (8, 17)), _arc(14, 18, 6, 5.5, 0, 360)]
    S[7] = [_line((7, 5), (21, 5)), _line((21, 5), (12, 23))]
    S[8] = [_arc(14, 9, 5, 4.5, 0, 360), _arc(14, 18.5, 6, 5, 0, 360)]
    S[9] = [_arc(14, 9, 5.5, 5, 0, 360), _line((19.5, 9), (17, 23))]
    return S

ORIENTS = [k * math.pi / 6 for k in range(6)]   # 0,30,...,150 degrees (math convention)

BLUR = 1.8      # spatial fall-off (pixels) of template outside the window core
TUNE_POW = 1.0  # orientation tuning sharpness

def _soft(d, half):
    e = np.maximum(0.0, np.abs(d) - half)
    return np.exp(-e ** 2 / (2.0 * BLUR ** 2))

def _templates():
    INK, OR = 0.75, 0.55               # guessed feature magnitudes for ink / matched orientation
    centers = 4 * np.arange(4) + 7.5   # input-pixel centre of each final 4x4 grid cell
    S = _digit_strokes()
    T = np.zeros((10, 16, 4, 4))
    for d in range(10):
        tight = np.zeros((8, 4, 4))
        wide = np.zeros((8, 4, 4))
        for pts in S[d]:
            x, y = pts[:, 0], pts[:, 1]
            dx = np.gradient(x); dy = np.gradient(y)
            seg = np.hypot(dx, dy)
            theta = np.mod(np.arctan2(-dy, dx), math.pi)
            tun = np.zeros((len(x), 6))
            for k, ok in enumerate(ORIENTS):
                dl = np.mod(theta - ok + math.pi / 2, math.pi) - math.pi / 2
                tun[:, k] = np.maximum(0.0, np.cos(2 * dl)) ** TUNE_POW
            # tight windows (centre-tap channels)
            wy = _soft(y[:, None] - centers[None, :], 2.0)
            wx = _soft(x[:, None] - centers[None, :], 2.0)
            w = wy[:, :, None] * wx[:, None, :]                       # N x 4 x 4
            tight[0] = np.maximum(tight[0], INK * w.max(0))
            for k in range(6):
                tight[1 + k] = np.maximum(tight[1 + k], (OR * w * tun[:, k, None, None]).max(0))
            # wide windows (3x3-summed channels): roughly stroke length in window / 6
            wyw = _soft(y[:, None] - centers[None, :], 4.0)
            wxw = _soft(x[:, None] - centers[None, :], 4.0)
            ww = wyw[:, :, None] * wxw[:, None, :] * seg[:, None, None]
            wide[0] += INK * ww.sum(0) / 6.0
            for k in range(6):
                wide[1 + k] += OR * (ww * tun[:, k, None, None]).sum(0) / 6.0
        T[d, :8] = tight
        T[d, 8:] = np.minimum(wide, 1.5)
    return T

def build_weights():
    # ---------------- conv1: ink + 6 oriented line detectors ----------------
    c1w = np.zeros((8, 1, 5, 5), np.float32)
    c1b = np.zeros(8, np.float32)
    # ch0: ink detector (3x3 average)
    c1w[0, 0, 1:4, 1:4] = 1.0 / 9.0
    c1b[0] = -0.2
    # ch1..6: zero-mean ridge filters at 0,30,...,150 degrees
    yy, xx = np.mgrid[-2:3, -2:3].astype(np.float64)   # yy=row offset (down), xx=col offset
    for k, th in enumerate(ORIENTS):
        ux, uy = math.cos(th), -math.sin(th)            # line direction in (col,row)
        dist = np.abs(xx * uy - yy * ux)                 # perpendicular distance to line
        g = np.exp(-dist ** 2 / (2 * 0.8 ** 2))
        w = g - g.mean()
        w /= w[w > 0].sum()
        c1w[1 + k, 0] = w
        c1b[1 + k] = -0.15
    # ch7 unused (all zero)

    # ---------------- conv2: pass-through (tight) and 3x3 blurred (wide) ----------------
    c2w = np.zeros((16, 8, 5, 5), np.float32)
    c2b = np.zeros(16, np.float32)
    for c in range(8):
        c2w[c, c, 2, 2] = 1.0                 # tight copy of conv1 channel c
        c2w[8 + c, c, 1:4, 1:4] = 1.0 / 3.0   # wide blurred copy of conv1 channel c

    # ---------------- fc: template logits with tuned norm penalty ----------------
    T = _templates().reshape(10, 256)
    s = 0.6       # overall logit scale
    alpha = 0.8   # weight on |T|^2 penalty (estimated feature/template magnitude ratio)
    fcw = (2.0 * s * T).astype(np.float32)
    fcb = (-s * alpha * (T ** 2).sum(1)).astype(np.float32)

    return {
        "conv1.weight": c1w,
        "conv1.bias": c1b,
        "conv2.weight": c2w,
        "conv2.bias": c2b,
        "fc.weight": fcw,
        "fc.bias": fcb,
    }
```
