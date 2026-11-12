# Step 4: add hole and concavity detectors to the oriented-edge features

**What the last three steps show.**
- The 4×4 grid of edge orientations cannot separate shapes such as 8 vs 2/7/9, 0 vs 2, 4 vs 1/9, or 3 vs 5.
- After three rounds of redrawing templates, accuracy is still only 59%.
- The missing information is structural: whether the digit has closed loops or concave bays, and where they are.

**conv1 is unchanged.** Its 8 polarity-edge channels already contain what is needed:
- channel 0: ink above the edge
- channel 1: ink below the edge
- channel 4: ink left of the edge
- channel 5: ink right of the edge

**conv2 keeps channels 0–3 and adds structural detectors.**
- Channels 0–3 are the orientation-energy maps, unchanged.
- Each new detector looks at a 5×5 window of pooled edges (about ±5 input pixels around its centre).
- It sums "walls" on each side, using the edge polarity that faces the empty centre.
- It penalises any edge at the centre, so the centre must be empty.
- A negative bias acts as a threshold.

| conv2 channel | Detects | Walls required | Typical digits |
|---|---|---|---|
| 4 | closed hole | all 4 sides | 0, 6, 8, 9 |
| 5 | U-shaped bay, open at the top | left, right, bottom; top wall penalised | open 4, bottom of 0 |
| 6 | ∩-shaped bay, open at the bottom | top, left, right | top of 0, under the top of 2 and 7 |
| 7 | ⊃-shaped bay, open to the left | top, right, bottom | the two bays of 3, lower bowl of 5 |
| 8 | ⊂-shaped bay, open to the right | top, left, bottom | upper part of 5 |
| 9 | two tall side walls with an empty middle | left and right | inside a tall 0 or an open 4 |

**fc.**
- The orientation templates from step 3 stay as they are.
- For the new channels I state by hand, for each digit, where each structure should appear (pixel coordinates with a weight).
- These spots are drawn onto the 4×4 grid with a Gaussian.
- The mean over digits is removed, and the result is scaled by beta = 3 before being added to the fc weights.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1: 4 orientations x 2 polarities of edge detectors =================
    # ch0: horizontal edge, ink ABOVE   ch1: horizontal edge, ink BELOW
    # ch2/3: "/" edges (two polarities)
    # ch4: vertical edge, ink LEFT      ch5: vertical edge, ink RIGHT
    # ch6/7: "\" edges (two polarities)
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    def edge_kernel(theta):
        K = np.zeros((5, 5))
        ct, st = math.cos(theta), math.sin(theta)
        for r in range(5):
            for c in range(5):
                u = c - 2
                v = -(r - 2)
                a = u * ct + v * st        # along stroke
                n = -u * st + v * ct       # across stroke (positive side = +K responds to ink)
                K[r, c] = n * math.exp(-a * a / (2 * 1.5 ** 2) - n * n / (2 * 1.0 ** 2))
        K /= K[K > 0].sum()
        return K

    for k, th in enumerate(thetas):
        K = edge_kernel(th)
        conv1_w[2 * k, 0] = K
        conv1_w[2 * k + 1, 0] = -K
        conv1_b[2 * k] = -0.25
        conv1_b[2 * k + 1] = -0.25

    INK_ABOVE, INK_BELOW, INK_LEFT, INK_RIGHT = 0, 1, 4, 5

    # ================= conv2 =================
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    # ch0..3: orientation energy maps (sum of both polarities, 3x3 blur)
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15

    w = 0.2
    def wall(c, side, wt):
        # Adds a "wall" on one side of the 5x5 window (pool1 units, centre = (2,2)),
        # using the edge polarity whose ink lies on the far side (facing the empty centre).
        if side == 'L':
            conv2_w[c, INK_LEFT, 1:4, 0:2] += wt
        elif side == 'R':
            conv2_w[c, INK_RIGHT, 1:4, 3:5] += wt
        elif side == 'T':
            conv2_w[c, INK_ABOVE, 0:2, 1:4] += wt
        elif side == 'B':
            conv2_w[c, INK_BELOW, 3:5, 1:4] += wt

    def empty_centre(c, pen=0.4):
        conv2_w[c, :, 2, 2] -= pen   # any edge at the centre -> not a hole/bay

    # ch4: closed hole (all four walls)
    for s in 'LRTB':
        wall(4, s, w)
    empty_centre(4)
    conv2_b[4] = -1.0
    # ch5..8: bays (three walls, fourth side penalised)
    bays = {5: ('LRB', 'T'),   # U, open at top
            6: ('LRT', 'B'),   # n, open at bottom
            7: ('TRB', 'L'),   # open to the left  (like the bays of a 3)
            8: ('TLB', 'R')}   # open to the right (upper part of a 5)
    for c, (walls_on, open_side) in bays.items():
        for s in walls_on:
            wall(c, s, w)
        wall(c, open_side, -2 * w)
        empty_centre(c)
        conv2_b[c] = -0.6
    # ch9: tall left+right walls with empty middle (interior of a tall 0 / open 4)
    conv2_w[9, INK_LEFT, 0:5, 0:2] += 0.15
    conv2_w[9, INK_RIGHT, 0:5, 3:5] += 0.15
    empty_centre(9)
    conv2_b[9] = -0.7
    # ch10..15 unused

    # ================= fc =================
    cell_c = np.array([7.5 + 4 * m for m in range(4)])   # final cell centres (input pixels)

    def ellipse(cx, cy, rx, ry, n=40):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    # ---- (a) orientation stroke templates (as in step 3) ----
    protos = {
        0: [(1.0, [ellipse(14, 14, 6.0, 9.0)])],
        1: [(1.0, [[(14, 4), (14, 24)]])],
        2: [(1.0, [[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17),
                    (9, 21), (8, 23), (13, 22.5), (21, 23)]])],
        3: [(1.0, [[(8, 6), (12, 4), (17, 4), (19, 7), (18, 11), (13, 13)],
                   [(13, 13), (18, 14), (20, 18), (18, 22), (13, 24), (8, 22)]])],
        4: [(0.5, [[(14, 4), (8, 15), (20, 15)], [(17, 7), (17, 24)]]),
            (0.5, [[(8, 5), (8, 15), (20, 15)], [(18, 4), (18, 24)]])],
        5: [(1.0, [[(19, 4), (10, 4), (9, 12)],
                   [(9, 12), (14, 11), (18, 13), (20, 17), (18, 22), (13, 23), (8, 21)]])],
        6: [(1.0, [[(17, 4), (12, 8), (9, 14), (9, 19), (12, 23), (16, 23), (19, 20),
                    (18, 15), (14, 13), (10, 16)]])],
        7: [(1.0, [[(7, 5), (20, 5), (17, 11), (14, 17), (13, 24)]])],
        8: [(1.0, [[(17, 5), (14, 4), (11, 5), (10, 8), (12, 11), (16, 14), (19, 17),
                    (19, 21), (15, 24), (11, 23), (9, 20), (10, 16), (13, 13), (17, 10),
                    (18, 7), (17, 5)]])],
        9: [(1.0, [ellipse(13.5, 9, 5.0, 4.5), [(18.5, 9), (17, 24)]])],
    }
    sig = 2.5
    shears = [0.0, 0.3]

    def add_polys(T, polys, wgt, s):
        for poly in polys:
            pts = [(x + s * (14 - y), y) for (x, y) in poly]
            for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(-dy, dx) % math.pi
                ow = np.array([max(0.0, math.cos(2 * (phi - th))) ** 2 for th in thetas])
                ns = max(1, int(L / 0.5))
                for i in range(ns):
                    t = (i + 0.5) / ns
                    x = x0 + t * dx
                    y = y0 + t * dy
                    sy = np.exp(-(y - cell_c) ** 2 / (2 * sig ** 2))
                    sx = np.exp(-(x - cell_c) ** 2 / (2 * sig ** 2))
                    T += wgt * ow[:, None, None] * sy[None, :, None] * sx[None, None, :] * (L / ns)

    temps = np.zeros((10, 4, 4, 4))
    for d in range(10):
        T = np.zeros((4, 4, 4))
        for wgt, polys in protos[d]:
            for s in shears:
                add_polys(T, polys, wgt, s)
        temps[d] = T / np.linalg.norm(T)
    temps -= temps.mean(axis=0, keepdims=True)
    for d in range(10):
        temps[d] -= temps[d].mean()
        temps[d] /= np.linalg.norm(temps[d])

    alpha = 8.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        fc_w[d, :64] = alpha * temps[d].reshape(-1)

    # ---- (b) structural templates: where holes / bays should be, per digit ----
    # entries: (conv2 channel, x, y, weight); 4=hole 5=U 6=n 7=open-left 8=open-right 9=walls
    struct = {
        0: [(6, 14, 9, 1.0), (5, 14, 19, 1.0), (9, 14, 14, 1.0), (4, 14, 14, 0.6)],
        1: [],
        2: [(6, 12, 10, 0.5), (7, 12, 11, 0.5), (5, 18, 19, 0.5)],
        3: [(7, 13, 8.5, 1.0), (7, 13, 18.5, 1.0)],
        4: [(5, 13, 10, 1.0), (9, 13, 10, 0.7), (4, 13, 11, 0.5)],
        5: [(8, 13, 8, 0.8), (7, 13, 18, 1.0)],
        6: [(4, 14, 18.5, 1.0)],
        7: [(6, 12, 11, 0.4), (7, 12, 11, 0.4)],
        8: [(4, 14, 8.5, 1.0), (4, 14, 18.5, 1.0)],
        9: [(4, 14, 9, 1.0), (6, 12, 18, 0.4), (7, 12, 18, 0.4)],
    }
    S = np.zeros((10, 16, 4, 4))
    for d in range(10):
        for (c, x, y, wt) in struct[d]:
            sy = np.exp(-(y - cell_c) ** 2 / (2 * sig ** 2))
            sx = np.exp(-(x - cell_c) ** 2 / (2 * sig ** 2))
            S[d, c] += wt * sy[:, None] * sx[None, :]
    S[:, 4:10] -= S[:, 4:10].mean(axis=0, keepdims=True)   # only differences between digits
    beta = 3.0
    for d in range(10):
        for c in range(4, 10):
            fc_w[d, c * 16:(c + 1) * 16] = beta * S[d, c].reshape(-1)

    fc_b = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
