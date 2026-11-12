# Step 3: redraw the weak digit prototypes and make templates tolerant of slant

Making templates zero-sum fixed the "everything is 8" failure, and accuracy rose from 38% to 57%. The confusion matrix and the mistakes now point to specific bad prototypes.

**Problems seen at step 2:**
- **8** was predicted as 7 or 1. I drew 8 as two touching ellipses, which gives horizontal strokes in the middle. Real 8s have an X-shaped crossing of "/" and "\" there.
- **4** was predicted as 1, 9 or 7. Many 4s are open-topped with a vertical left arm; others are the closed, slanted kind.
- **Slant:** slanted 1s become 7s, and slanted 9s become 7s. All my prototypes were upright, while MNIST digits often lean right.

**Changes this step (conv1 and conv2 unchanged):**
- **8:** drawn as one S-shaped path with a diagonal X crossing in the middle.
- **4:** two hand-drawn variants (closed/slanted and open) are added into one template.
- **1, 2, 3, 5, 9:** redrawn a little more carefully.
- **Slant:** every template is the sum of the upright drawing and a right-leaning sheared copy, using the formula x' = x + s·(14 − y) with s = 0.3. Templates now tolerate the usual slant.
- The normalisation from step 2 stays: zero-sum, equal-norm templates.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 4 orientations x 2 polarities of edge detectors ----------------
    # Orientation angles (y pointing UP): 0 = horizontal, 45 = "/", 90 = vertical, 135 = "\".
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
                n = -u * st + v * ct       # across stroke
                K[r, c] = n * math.exp(-a * a / (2 * 1.5 ** 2) - n * n / (2 * 1.0 ** 2))
        K /= K[K > 0].sum()
        return K

    for k, th in enumerate(thetas):
        K = edge_kernel(th)
        conv1_w[2 * k, 0] = K
        conv1_w[2 * k + 1, 0] = -K
        conv1_b[2 * k] = -0.25
        conv1_b[2 * k + 1] = -0.25

    # ---------------- conv2: orientation energy maps (sum of polarities, 3x3 blur) -------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15

    # ---------------- fc: hand-drawn stroke templates ----------------
    cell_c = np.array([7.5 + 4 * m for m in range(4)])

    def ellipse(cx, cy, rx, ry, n=40):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    # Each digit: list of (weight, list of polylines). Points (x=column, y=row).
    protos = {
        0: [(1.0, [ellipse(14, 14, 6.0, 9.0)])],
        1: [(1.0, [[(14, 4), (14, 24)]])],
        2: [(1.0, [[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17),
                    (9, 21), (8, 23), (13, 22.5), (21, 23)]])],
        3: [(1.0, [[(8, 6), (12, 4), (17, 4), (19, 7), (18, 11), (13, 13)],
                   [(13, 13), (18, 14), (20, 18), (18, 22), (13, 24), (8, 22)]])],
        4: [(0.5, [[(14, 4), (8, 15), (20, 15)], [(17, 7), (17, 24)]]),      # closed / slanted 4
            (0.5, [[(8, 5), (8, 15), (20, 15)], [(18, 4), (18, 24)]])],      # open 4
        5: [(1.0, [[(19, 4), (10, 4), (9, 12)],
                   [(9, 12), (14, 11), (18, 13), (20, 17), (18, 22), (13, 23), (8, 21)]])],
        6: [(1.0, [[(17, 4), (12, 8), (9, 14), (9, 19), (12, 23), (16, 23), (19, 20),
                    (18, 15), (14, 13), (10, 16)]])],
        7: [(1.0, [[(7, 5), (20, 5), (17, 11), (14, 17), (13, 24)]])],
        # 8 as one S-shaped path: top loop, "\" diagonal down to bottom-right, bottom loop,
        # "/" diagonal back up across the middle -> X crossing in the centre
        8: [(1.0, [[(17, 5), (14, 4), (11, 5), (10, 8), (12, 11), (16, 14), (19, 17),
                    (19, 21), (15, 24), (11, 23), (9, 20), (10, 16), (13, 13), (17, 10),
                    (18, 7), (17, 5)]])],
        9: [(1.0, [ellipse(13.5, 9, 5.0, 4.5), [(18.5, 9), (17, 24)]])],
    }

    sig = 2.5
    shears = [0.0, 0.3]   # upright and right-leaning copy: x' = x + s*(14 - y)

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
    temps -= temps.mean(axis=0, keepdims=True)     # remove shared part
    for d in range(10):
        temps[d] -= temps[d].mean()                # zero-sum: uniform activity scores 0
        temps[d] /= np.linalg.norm(temps[d])       # equal norms

    alpha = 8.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        fc_w[d, :64] = alpha * temps[d].reshape(-1)
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
