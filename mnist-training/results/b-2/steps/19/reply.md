# Step 19: weight all six structural channels from their measured class means

All six structural channels (4–9) have now been measured on the current network. Each has a top-half and a bottom-half scalar, giving 12 in total.

**Channel 9 (two side walls), from step 18.**
- It is mostly silent, except in 0, 1 and the top of 4 (open-topped 4s).
- So it carries only a little evidence: "0/1/4 rather than 2/3/5".

**This step, a real classifier.**
- The orientation templates, the step-14 class biases and the 0.55 temperature stay as they are.
- The hand-guessed templates for channels 5, 6, 8 and 9 are removed. All structural channels now use the measured Gaussian terms, as channels 4 and 7 did at step 14.
- For each of the 12 scalars, h = the sum of the channel map over the top or bottom two rows of cells, and μ_d is the hand-estimated class mean from its histogram. Each scalar adds k·μ_d·h − k·μ_d²/2 to the logit of digit d.
- The detectors are clearly correlated (they all respond to plain vertical walls, for instance). So I lower the shrink factor from 0.5 to 0.4: k = 0.4/0.15.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1: 4 orientations x 2 polarities of edge detectors =================
    # ch0: horizontal edge, ink ABOVE   ch1: horizontal edge, ink BELOW
    # ch2/3: "/" edges                  ch4: vertical edge, ink LEFT
    # ch5: vertical edge, ink RIGHT     ch6/7: "\" edges
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
                a = u * ct + v * st
                n = -u * st + v * ct
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

    # ================= conv2 (unchanged) =================
    # ch0..3 orientation energy; ch4 hole; ch5 U; ch6 n; ch7 open-left; ch8 open-right; ch9 side walls
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15

    w = 0.2
    def wall(c, side, wt):
        if side == 'L':
            conv2_w[c, INK_LEFT, 1:4, 0:2] += wt
        elif side == 'R':
            conv2_w[c, INK_RIGHT, 1:4, 3:5] += wt
        elif side == 'T':
            conv2_w[c, INK_ABOVE, 0:2, 1:4] += wt
        elif side == 'B':
            conv2_w[c, INK_BELOW, 3:5, 1:4] += wt

    def empty_centre(c, pen=0.4):
        conv2_w[c, :, 2, 2] -= pen

    for s in 'LRTB':
        wall(4, s, w)
    empty_centre(4)
    conv2_b[4] = -0.8
    bays = {5: ('LRB', 'T'), 6: ('LRT', 'B'), 7: ('TRB', 'L'), 8: ('TLB', 'R')}
    for c, (walls_on, open_side) in bays.items():
        for s in walls_on:
            wall(c, s, w)
        wall(c, open_side, -2 * w)
        empty_centre(c)
        conv2_b[c] = -0.5
    conv2_w[9, INK_LEFT, 0:5, 0:2] += 0.15
    conv2_w[9, INK_RIGHT, 0:5, 3:5] += 0.15
    empty_centre(9)
    conv2_b[9] = -0.7

    # ================= fc =================
    cell_c = np.array([7.5 + 4 * m for m in range(4)])

    def ellipse(cx, cy, rx, ry, n=40):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    S2 = [0.0, 0.3]
    protos = {
        0: [(1.0, [ellipse(14, 14, 6.0, 9.0)], S2)],
        1: [(1.0, [[(14, 4), (14, 24)]], [0.0, 0.3, 0.6])],
        2: [(1.0, [[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17),
                    (9, 21), (8, 23), (13, 22.5), (21, 23)]], S2)],
        3: [(1.0, [[(8, 6), (12, 4), (17, 4), (19, 7), (18, 11), (13, 13)],
                   [(13, 13), (18, 14), (20, 18), (18, 22), (13, 24), (8, 22)]], S2)],
        4: [(0.5, [[(14, 4), (8, 15), (20, 15)], [(17, 7), (17, 24)]], S2),
            (0.5, [[(8, 5), (8, 15), (20, 15)], [(18, 4), (18, 24)]], S2)],
        5: [(1.0, [[(19, 4), (10, 4), (9, 12)],
                   [(9, 12), (14, 11), (18, 13), (20, 17), (18, 22), (13, 23), (8, 21)]], S2)],
        6: [(0.5, [[(17, 4), (12, 8), (9, 14), (9, 19), (12, 23), (16, 23), (19, 20),
                    (18, 15), (14, 13), (10, 16)]], S2),
            (0.5, [[(16, 4), (11, 12), (9, 18), (11, 23), (15, 23), (18, 20), (17, 16),
                    (13, 15), (10, 18)]], S2)],
        7: [(0.5, [[(7, 5), (20, 5), (17, 11), (14, 17), (13, 24)]], S2),
            (0.5, [[(7, 5), (19, 5), (18, 10), (16.5, 24)]], S2)],
        8: [(1.0, [[(18, 6), (15, 4), (12, 5), (11, 8), (13, 11), (16, 14), (18, 18),
                    (17, 22), (13.5, 24), (10, 22), (9.5, 18), (12, 15), (16, 11),
                    (18.5, 8), (18, 6)]], S2)],
        9: [(1.0, [ellipse(14, 9, 4.5, 4.0), [(18.5, 9), (17, 24)]], S2)],
    }
    sig = 2.5

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
        for wgt, polys, shs in protos[d]:
            for s in shs:
                add_polys(T, polys, wgt / len(shs), s)
        temps[d] = T / np.linalg.norm(T)
    temps -= temps.mean(axis=0, keepdims=True)
    for d in range(10):
        temps[d] -= temps[d].mean()
        temps[d] /= np.linalg.norm(temps[d])

    temp = 0.55
    alpha = 8.0
    fc_w = np.zeros((10, 256))
    for d in range(10):
        fc_w[d, :64] = temp * alpha * temps[d].reshape(-1)

    fc_b = temp * np.array([-0.4, -0.8, 0.0, -0.6, 0.6, 0.0, 0.2, 0.0, 2.0, -0.5])

    # ---- measured class means (steps 12,13,15-18) of structural scalars ----
    # scalar = sum of the channel's 4x4 map over cell rows 0-1 ('top') or 2-3 ('bot')
    #            digit:  0      1      2      3      4      5      6      7      8      9
    mu = {
        (4, 'top'): [0.610, 0.017, 0.690, 0.197, 0.487, 0.252, 0.358, 0.284, 0.230, 0.323],
        (4, 'bot'): [0.830, 0.021, 0.170, 0.673, 0.296, 0.588, 0.181, 0.305, 0.211, 0.229],
        (5, 'top'): [0.134, 0.472, 0.314, 0.177, 0.742, 0.124, 0.478, 0.093, 0.175, 0.087],
        (5, 'bot'): [0.748, 0.478, 0.245, 0.117, 0.087, 0.117, 0.178, 0.208, 0.142, 0.135],
        (6, 'top'): [0.691, 0.438, 0.277, 0.133, 0.161, 0.165, 0.119, 0.385, 0.093, 0.091],
        (6, 'bot'): [0.168, 0.506, 0.084, 0.104, 0.767, 0.151, 0.095, 0.626, 0.386, 0.610],
        (7, 'top'): [0.378, 0.256, 0.877, 0.464, 0.124, 0.245, 0.161, 0.479, 0.194, 0.119],
        (7, 'bot'): [0.421, 0.254, 0.193, 0.892, 0.619, 0.755, 0.104, 0.653, 0.253, 0.613],
        (8, 'top'): [0.187, 0.257, 0.339, 0.243, 0.147, 0.599, 0.745, 0.135, 0.152, 0.135],
        (8, 'bot'): [0.600, 0.299, 0.336, 0.390, 0.303, 0.432, 0.062, 0.237, 0.344, 0.211],
        (9, 'top'): [0.191, 0.163, 0.034, 0.013, 0.228, 0.017, 0.066, 0.027, 0.027, 0.037],
        (9, 'bot'): [0.242, 0.187, 0.007, 0.014, 0.040, 0.013, 0.052, 0.076, 0.041, 0.074],
    }
    var = 0.15
    shrink = 0.4
    kfac = shrink / var
    for (ch, part), m in mu.items():
        rows = (0, 1) if part == 'top' else (2, 3)
        m = np.array(m)
        for d in range(10):
            for r in rows:
                for c in range(4):
                    fc_w[d, ch * 16 + r * 4 + c] += kfac * m[d]
            fc_b[d] += -kfac * m[d] ** 2 / 2.0

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
