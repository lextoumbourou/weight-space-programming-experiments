## Approach for step 24

Step 23 reached 72.8% accuracy with the best loss so far (0.872). Further bias and loop tweaks now give only small gains. The largest remaining confusions are pairs that differ mainly in where the strokes end:

- 4→9 (162): a 4 has open top ends, while a 9 has a closed loop.
- 3→5 (142): a 3 has a top-left end; a 5 has a top-right end.
- 2→3 (121): a 2 ends bottom-right; a 3 ends bottom-left.
- 3→8 (113): an 8 has no stroke ends at all.
- 7→9 (103): a 7 has a top-left end.
- 5→6 (100): a 5 ends bottom-left; a 6 ends at the top.

**New feature: a stroke-endpoint detector** (conv2 channel 5).

- It works on the pooled raw-ink map. The kernel is +2.5 at the centre and −1 on each of the 16 cells of the ring 2 cells (4 px) out, with bias −1.
- A stroke passing through the centre crosses that ring twice, so the response is ≤ 0. A stroke ending within about 4 px of the centre crosses it once, giving about +0.5. Corners and junctions cross two or more times, so they stay silent.
- To free the channel, the diagonal map keeps only 2 of its 4 offsets. The ink map gets its third offset back.

**Endpoint templates.** These are hand-specified as (x, y, probability):

| Digit | Endpoints |
|---|---|
| 0, 8 | none |
| 1 | top, bottom |
| 2 | top-left, bottom-right |
| 3 | top-left, bottom-left |
| 4 | top-left, top-right, stem bottom, crossbar right |
| 5 | top-right, bottom-left |
| 6 | top |
| 7 | top-left, bottom |
| 9 | stem bottom |

As with the loops, these are decoupled positive evidence: weight = g_end · map, with g_end = 1.5, and no distance penalty. Classes with many endpoints would gain on average from this, so I pre-subtract 0.15·g_end·Σprob from each class's bias.

```python
import numpy as np
import math

def build_weights():
    # ================= conv1 =================
    # ch0..3: oriented line detectors (0, 45, 90, 135 deg); ch4: ink blur;
    # ch5: raw ink (keeps holes / ends sharp); ch6-7 unused
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros(8, dtype=np.float64)
    thetas = [0.0, 45.0, 90.0, 135.0]   # stroke direction (x=col right, y=row down)
    for k, th in enumerate(thetas):
        t_rad = math.radians(th)
        ker = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                y, x = r - 2, c - 2
                n = -x * math.sin(t_rad) + y * math.cos(t_rad)   # across line
                t = x * math.cos(t_rad) + y * math.sin(t_rad)    # along line
                ker[r, c] = math.exp(-n * n / 2.0) * math.exp(-t * t / (2 * 2.5 ** 2))
        ker -= ker.mean()
        ker /= ker[ker > 0].sum()
        conv1_w[k, 0] = ker
        conv1_b[k] = -0.2
    g = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            g[r, c] = math.exp(-((r - 2) ** 2 + (c - 2) ** 2) / 2.0)
    conv1_w[4, 0] = g / g.sum()          # ink blur
    conv1_w[5, 0, 2, 2] = 1.0            # raw ink copy

    # ================= conv2 =================
    # specs: ('tap', type, dy, dx) | ('loop',) | ('sloop',) | ('end',)
    type_inputs = [[4], [0], [2], [1, 3]]   # ink, horizontal, vertical, diagonal
    offs4 = [(2, 2), (2, 3), (3, 2), (3, 3)]
    specs = [('tap', 0, 2, 2), ('tap', 0, 3, 3), ('tap', 0, 2, 3),
             ('sloop',), ('loop',), ('end',)]
    for ty in (1, 2):
        for (dy, dx) in offs4:
            specs.append(('tap', ty, dy, dx))
    for (dy, dx) in [(2, 2), (3, 3)]:
        specs.append(('tap', 3, dy, dx))
    assert len(specs) == 16

    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros(16, dtype=np.float64)
    for c, sp in enumerate(specs):
        if sp[0] == 'tap':
            _, ty, dy, dx = sp
            for ic in type_inputs[ty]:
                conv2_w[c, ic, dy, dx] = 1.0
        elif sp[0] == 'loop':
            # ~8px loop: ink ring 2 cells out, empty centre (blurred ink)
            K = np.zeros((5, 5))
            for j in (1, 2, 3):
                K[0, j] = K[4, j] = K[j, 0] = K[j, 4] = 1.0
            K[2, 2] = -2.0
            for (r, cc) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
                K[r, cc] = -0.5
            conv2_w[c, 4] = K / 1.5
            conv2_b[c] = -7.0 / 1.5
        elif sp[0] == 'sloop':
            # small loop: ink on 3x3 ring, empty centre (raw ink)
            K = np.zeros((5, 5))
            for r in (1, 2, 3):
                for cc in (1, 2, 3):
                    K[r, cc] = 1.0
            K[2, 2] = -3.0
            conv2_w[c, 5] = K / 1.5
            conv2_b[c] = -5.5 / 1.5
        else:
            # stroke endpoint: ink at centre, ink crossing the outer ring only once
            K = -np.ones((5, 5))
            K[1:4, 1:4] = 0.0
            K[2, 2] = 2.5
            conv2_w[c, 5] = K
            conv2_b[c] = -1.0

    # ================= digit prototypes (x=col, y=row) =================
    def ell(cx, cy, rx, ry, n=48, tilt=0.0):
        pts = []
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            x, y = rx * math.cos(a), ry * math.sin(a)
            pts.append((cx + x - tilt * y, cy + y))
        return pts

    variants = {
        0: [[ell(14, 14, 6, 9)],
            [ell(14, 14, 5, 9, tilt=0.3)],
            [ell(14, 14, 7, 8.5)]],
        1: [[[(16, 4), (12, 23)]],
            [[(14, 4), (14, 23)]],
            [[(18, 4), (10, 23)]]],
        2: [[[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17), (8, 22)],
             [(8, 22), (21, 22)]],
            [[(8, 7), (12, 4), (17, 4), (19, 8), (16, 14), (10, 20), (8, 22), (10, 19),
              (13, 20), (17, 22), (21, 22)]]],
        3: [[[(8, 6), (12, 4), (17, 4), (19, 7), (18, 10), (13, 13)],
             [(13, 13), (18, 15), (20, 18), (18, 22), (13, 23), (8, 21)]],
            [[(9, 5), (14, 4), (18, 6), (17, 10), (12, 13)],
             [(12, 13), (17, 14), (19, 18), (16, 22), (10, 23), (7, 20)]]],
        4: [[[(11, 4), (7, 16), (21, 16)], [(17, 5), (17, 24)]],
            [[(8, 5), (8, 15), (21, 15)], [(18, 5), (18, 24)]],
            [[(12, 4), (6, 16), (21, 15)], [(19, 6), (16, 24)]]],
        5: [[[(20, 4), (10, 4)], [(10, 4), (9, 13)],
             [(9, 13), (14, 11), (19, 13), (20, 18), (17, 22), (12, 23), (7, 21)]],
            [[(21, 5), (12, 5)], [(12, 5), (10, 13)],
             [(10, 13), (15, 12), (18, 15), (18, 19), (14, 23), (8, 22)]]],
        6: [[[(17, 4), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23), (18, 21),
              (19, 17), (16, 14), (12, 14), (9, 17)]],
            [[(18, 4), (14, 7), (11, 12), (10, 17), (12, 22), (16, 23), (19, 20),
              (18, 16), (14, 15), (11, 18)]]],
        7: [[[(7, 5), (21, 5)], [(21, 5), (12, 24)]],
            [[(7, 5), (20, 5)], [(20, 5), (16, 14), (15, 24)]],
            [[(8, 6), (21, 4)], [(21, 4), (10, 24)]],
            [[(7, 5), (21, 5)], [(21, 5), (13, 24)], [(11, 14), (21, 14)]]],
        8: [[ell(14, 9, 5, 4.5), ell(14, 18.5, 6, 5)],
            [ell(15, 9, 4.5, 4.5, tilt=0.2), ell(13, 18.5, 5, 5, tilt=0.2)],
            [ell(14, 9, 3.5, 4.5), ell(14, 18.5, 4, 5)],
            [ell(16, 9, 4, 4.5, tilt=0.35), ell(12.5, 18.5, 4.5, 5, tilt=0.35)]],
        9: [[ell(14, 10, 6, 5.5), [(20, 10), (18, 24)]],
            [ell(13.5, 9.5, 5.5, 5), [(19, 10), (19, 24)]],
            [ell(15, 9.5, 5.5, 5, tilt=0.2), [(20, 10), (15, 24)]],
            [ell(15, 8.5, 4.5, 4, tilt=0.3), [(19, 9), (14, 24)]]],
    }

    # loop locations (x, y, prob)
    loops_big = {
        0: [(14, 14, 0.3)], 1: [], 2: [(10, 20, 0.1)], 3: [], 4: [(12, 10, 0.15)],
        5: [], 6: [(14, 18, 0.7)], 7: [], 8: [(14, 9, 0.6), (14, 18.5, 0.6)],
        9: [(14.5, 9.5, 0.7)],
    }
    loops_small = {
        0: [(14, 14, 0.15)], 1: [], 2: [(10, 20, 0.15)], 3: [], 4: [(12, 10, 0.2)],
        5: [], 6: [(14, 18, 0.5)], 7: [], 8: [(14, 9, 0.6), (14, 18.5, 0.6)],
        9: [(14.5, 9.5, 0.5)],
    }
    generic_loops = [(14, 9, 1.0), (14, 18.5, 1.0)]
    no_loop_digits = [1, 3, 5, 7]

    # stroke endpoint locations (x, y, prob), placed ~2 px inside the stroke end
    ends = {
        0: [],
        1: [(15, 6, 0.8), (13, 21, 0.8)],
        2: [(9, 8, 0.7), (20, 21, 0.8)],
        3: [(9, 6, 0.8), (9, 20, 0.8)],
        4: [(10, 7, 0.7), (17, 7, 0.7), (17, 21, 0.8), (20, 15, 0.4)],
        5: [(19, 5, 0.8), (8, 20, 0.8)],
        6: [(16, 6, 0.8)],
        7: [(8, 6, 0.8), (13, 21, 0.8)],
        8: [],
        9: [(17, 21, 0.8)],
    }

    def sample(polys):
        pts, ths = [], []
        for poly in polys:
            for p, q in zip(poly[:-1], poly[1:]):
                dx, dy = q[0] - p[0], q[1] - p[1]
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                m = max(1, int(L / 0.5))
                th = math.atan2(dy, dx)
                for i in range(m):
                    f = (i + 0.5) / m
                    pts.append((p[0] + dx * f, p[1] + dy * f))
                    ths.append(th)
        return np.array(pts), np.array(ths)

    th_o = np.radians(np.array(thetas))
    A = [0.8, 0.65, 0.65, 0.65]
    plateau = 2.5
    sig_var = 2.0

    def feature_template(polys):
        pts, ths = sample(polys)
        dth = ths[:, None] - th_o[None, :]
        tune4 = np.clip((np.cos(dth) ** 2 - 0.25) / 0.75, 0, None)
        tunes = [np.ones(len(pts)),
                 tune4[:, 0],
                 tune4[:, 2],
                 np.minimum(1.0, tune4[:, 1] + tune4[:, 3])]
        T = np.zeros((16, 4, 4))
        for c, sp in enumerate(specs):
            if sp[0] != 'tap':
                continue
            _, ty, dy, dx = sp
            for a in range(4):
                for b in range(4):
                    cy = 4 * a + 2 * dy + 3.5
                    cx = 4 * b + 2 * dx + 3.5
                    d = np.sqrt((pts[:, 0] - cx) ** 2 + (pts[:, 1] - cy) ** 2)
                    e = np.maximum(0.0, d - plateau)
                    v = tunes[ty] * np.exp(-e * e / (2 * sig_var ** 2))
                    T[c, a, b] = A[ty] * v.max()
        return T

    def point_map(lst):
        # map of hand-specified point features on the 4x4 grid (centres 4a+7.5)
        M = np.zeros((4, 4))
        for a in range(4):
            for b in range(4):
                cy, cx = 4 * a + 7.5, 4 * b + 7.5
                val = 0.0
                for (lx, ly, p) in lst:
                    dd = math.hypot(lx - cx, ly - cy)
                    e = max(0.0, dd - 1.0)
                    val = max(val, p * math.exp(-e * e / (2 * 2.5 ** 2)))
                M[a, b] = val
        return M

    loop_c = [i for i, sp in enumerate(specs) if sp[0] == 'loop'][0]
    sloop_c = [i for i, sp in enumerate(specs) if sp[0] == 'sloop'][0]
    end_c = [i for i, sp in enumerate(specs) if sp[0] == 'end'][0]
    special = [loop_c, sloop_c, end_c]

    # stroke templates (special channels excluded from the distance model)
    mu = np.zeros((10, 16, 4, 4))
    for d in range(10):
        acc = np.zeros((16, 4, 4))
        for var in variants[d]:
            acc += feature_template(var)
        mu[d] = acc / len(variants[d])
        for c in special:
            mu[d, c] = 0.0

    # ================= fc =================
    beta = 0.55
    s = 1.6
    W = 2.0 * s * beta * mu
    fc_b = -s * beta ** 2 * np.sum(mu.reshape(10, -1) ** 2, axis=1)

    # loop evidence (decoupled): positive for loop digits, negative for loop-free digits
    g_big, g_small = 1.9, 1.5
    neg = 0.5
    gen = point_map(generic_loops)
    for d in range(10):
        W[d, loop_c] = g_big * point_map(loops_big[d])
        W[d, sloop_c] = g_small * point_map(loops_small[d])
        if d in no_loop_digits:
            W[d, loop_c] -= neg * g_big * gen
            W[d, sloop_c] -= neg * g_small * gen

    # endpoint evidence (decoupled)
    g_end = 1.5
    for d in range(10):
        W[d, end_c] = g_end * point_map(ends[d])
    fc_w = W.reshape(10, 256)

    # class-balance correction (from step 22/23) + pre-compensation for endpoint boost
    #                  0      1      2     3     4     5     6      7      8     9
    corr = np.array([-0.22, -2.26, -0.27, 0.59, 2.80, 1.58, -0.08, -0.16, 0.25, -0.01])
    end_mass = np.array([sum(p for (_, _, p) in ends[d]) for d in range(10)])
    fc_b = fc_b + corr - 0.15 * g_end * end_mass

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
