**Step 8: zero-mean prototypes over all channels.**

Every nearest-prototype variant has either sunk to one class or relied on a bias that depends on how much ink a digit expects. Step 7 sent 8 of every 10 images to class 8.

The fix is to centre each class's prototype across all 80 used entries (5 channels × 16 cells). A score of Σ f·(μ_d − mean μ_d) does not depend on the total amount of ink a class expects. Adding a constant to every cell of a prototype leaves the scores unchanged for an image with uniform features, and the centred prototype has negative weight where a class expects less ink than average. This is the same idea that gave the best result so far (step 2, 43.6%), now with drawn oriented stroke templates instead of hand-written 4x4 grids. Because the score has no bias and each prototype is centred, the overall gain does not change the argmax. The constant `SCALE` only sets logit magnitude, so the loss is sensible.

```python
import numpy as np
import math


def _arc(cx, cy, rx, ry, a0, a1, n=24):
    # Points along an elliptical arc (angles in degrees, 90 = top, y grows downward).
    pts = []
    for t in np.linspace(a0, a1, n):
        th = math.radians(t)
        pts.append((cx + rx * math.cos(th), cy - ry * math.sin(th)))
    return pts


def _ellipse(cx, cy, rx, ry, n=36):
    return _arc(cx, cy, rx, ry, 0.0, 360.0, n)


def _digit_strokes():
    # Hand-described strokes for each digit, in pixel coordinates of the 28x28 field
    # (x = column, y = row). The digit fills roughly rows 4..24 and columns 6..22.
    S = {}
    S[0] = [_ellipse(14, 14, 6, 10)]
    S[1] = [[(15.0, 4.0), (13.0, 24.0)]]
    S[2] = [_arc(14, 10, 6, 6, 160, -30) + [(8.0, 23.0), (20.0, 23.0)]]
    S[3] = [_arc(14, 9, 5.5, 5.0, 150, -90), _arc(14, 18.5, 6.0, 5.5, 90, -150)]
    S[4] = [[(17.0, 4.0), (8.0, 17.0), (21.0, 17.0)], [(17.0, 4.0), (17.0, 24.0)]]
    S[5] = [[(19.0, 5.0), (9.0, 5.0), (9.0, 12.5)], _arc(14, 18.0, 6.0, 6.0, 125, -140)]
    S[6] = [_ellipse(14, 18.5, 5.5, 5.5), _arc(16, 14, 8, 10, 180, 75)]
    S[7] = [[(8.0, 5.0), (20.0, 5.0), (12.0, 24.0)]]
    S[8] = [_ellipse(14, 9, 4.5, 4.5), _ellipse(14, 18.5, 5.5, 5.5)]
    S[9] = [_ellipse(14, 10.5, 5.5, 5.5), [(19.5, 10.5), (16.0, 24.0)]]
    return S


def _rasterize_oriented(polylines):
    # Returns five 28x28 canvases: [total ink, vertical, horizontal, '/', '\'].
    # Each segment's ink is split across orientations by its direction:
    #   vertical   weight = dy^2 / L^2
    #   horizontal weight = dx^2 / L^2
    #   '/'        weight = 2*max(0, -dx*dy) / L^2   (image y grows downward)
    #   '\'        weight = 2*max(0,  dx*dy) / L^2
    H = W = 28
    rows, cols = np.mgrid[0:H, 0:W]
    xs = cols.astype(np.float64)
    ys = rows.astype(np.float64)
    total = np.zeros((H, W))
    orient = [np.zeros((H, W)) for _ in range(4)]
    for poly in polylines:
        for k in range(len(poly) - 1):
            x0, y0 = poly[k]
            x1, y1 = poly[k + 1]
            dx, dy = x1 - x0, y1 - y0
            L2 = dx * dx + dy * dy
            if L2 < 1e-12:
                continue
            t = np.clip(((xs - x0) * dx + (ys - y0) * dy) / L2, 0.0, 1.0)
            px = x0 + t * dx - xs
            py = y0 + t * dy - ys
            ink = np.clip(1.5 - np.sqrt(px * px + py * py), 0.0, 1.0)
            w = [dy * dy / L2,
                 dx * dx / L2,
                 2.0 * max(0.0, -dx * dy) / L2,
                 2.0 * max(0.0, dx * dy) / L2]
            total = np.maximum(total, ink)
            for m in range(4):
                orient[m] = np.maximum(orient[m], ink * w[m])
    return [total] + orient


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters of size 1x5x5 (input is 1 channel)
    # ------------------------------------------------------------------
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)

    def line_profile(dist):
        if dist == 0:
            return 0.125
        if dist == 1:
            return 0.0625
        if dist == 2:
            return -0.0625
        return 0.0

    for r in range(5):
        for c in range(5):
            c1w[0, 0, r, c] = line_profile(abs(c - 2))          # ch0 vertical stroke
            c1w[1, 0, r, c] = line_profile(abs(r - 2))          # ch1 horizontal stroke
            c1w[2, 0, r, c] = line_profile(abs(r + c - 4))      # ch2 '/' diagonal
            c1w[3, 0, r, c] = line_profile(abs(r - c))          # ch3 '\' diagonal
            c1w[4, 0, r, c] = 0.1 if (abs(r - 2) <= 1 and abs(c - 2) <= 1) else -0.02
            c1w[5, 0, r, c] = 0.04                              # ch5 local ink average
            if c >= 3:                                          # ch6 edge
                c1w[6, 0, r, c] = 0.1
            elif c <= 1:
                c1w[6, 0, r, c] = -0.1
            if r <= 1:                                          # ch7 edge
                c1w[7, 0, r, c] = 0.1
            elif r >= 3:
                c1w[7, 0, r, c] = -0.1

    c1b[:] = [-0.25, -0.25, -0.25, -0.25, -0.2, 0.0, -0.2, -0.2]

    # ------------------------------------------------------------------
    # conv2: 16 filters of size 8x5x5
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    # out 0..3: 3x3 blur of the oriented stroke channels (vertical, horizontal, '/', '\')
    for k in range(4):
        c2w[k, k, 1:4, 1:4] = 1.0 / 9.0
    # out 4: hole detector (unused by fc)
    for r in range(5):
        for c in range(5):
            centre = (1 <= r <= 3) and (1 <= c <= 3)
            c2w[4, 5, r, c] = -1.0 / 9.0 if centre else 1.0 / 16.0
    # out 5: 3x3 blur of ink presence
    c2w[5, 5, 1:4, 1:4] = 1.0 / 9.0
    c2w[6, 6, 1:4, 1:4] = 1.0 / 9.0
    c2w[7, 7, 1:4, 1:4] = 1.0 / 9.0
    for k in range(8):
        c2w[8 + k, k, :, :] = 1.0 / 25.0

    # ------------------------------------------------------------------
    # fc: 256 -> 10. Flatten index = channel*16 + row*4 + col.
    # Used channels: 5 = total ink, 0 = vertical, 1 = horizontal, 2 = '/', 3 = '\'.
    # Score_d = sum over used entries of f * (mu_d - mean(mu_d)), no bias.
    # ------------------------------------------------------------------
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)

    USED = [5, 0, 1, 2, 3]
    canvas_index = {5: 0, 0: 1, 1: 2, 2: 3, 3: 4}  # which rasterised canvas feeds each channel
    SCALE = 10.0   # logit magnitude only; argmax is unaffected

    idx = np.concatenate([np.arange(ch * 16, (ch + 1) * 16) for ch in USED])

    strokes = _digit_strokes()

    for d in range(10):
        canvases = _rasterize_oriented(strokes[d])
        vec = np.zeros(256, dtype=np.float64)
        for ch in USED:
            canvas = canvases[canvas_index[ch]]
            # Mean value over the 12x12 receptive window of each final cell.
            # Cell (i, j) covers input rows and columns 4i+2 .. 4i+13.
            occ = np.zeros((4, 4), dtype=np.float64)
            for i in range(4):
                for j in range(4):
                    occ[i, j] = canvas[4 * i + 2:4 * i + 14, 4 * j + 2:4 * j + 14].mean()
            vec[ch * 16:(ch + 1) * 16] = occ.reshape(16)

        # Centre the prototype over all used entries so that a class's total
        # expected ink does not shift its score.
        m = vec[idx].mean()
        fcw[d, idx] = SCALE * (vec[idx] - m)
        fcb[d] = 0.0

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
