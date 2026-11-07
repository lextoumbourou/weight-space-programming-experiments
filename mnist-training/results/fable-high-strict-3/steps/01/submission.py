import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 hand-drawn 5x5 detectors
    # ------------------------------------------------------------------
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    # ch0: ink blob (Gaussian, sums to 1 -> output roughly in [0,1])
    for a in range(5):
        for b in range(5):
            w1[0, 0, a, b] = math.exp(-((a - 2) ** 2 + (b - 2) ** 2) / 2.0)
    w1[0, 0] /= w1[0, 0].sum()
    # ch1: horizontal stroke (bar through the middle, negative 2px above/below)
    prof = np.array([-1.0, 0.5, 1.0, 0.5, -1.0])
    w1[1, 0] = np.outer(prof, np.ones(5) / 5.0) / 2.0
    # ch2: vertical stroke
    w1[2, 0] = w1[1, 0].T
    # ch3: '/' diagonal stroke, ch4: '\' diagonal stroke (negative off-diagonal lobes)
    g = {0: 1.0, 1: 0.3, 2: -0.6, 3: -0.6, 4: -0.6}
    for a in range(5):
        for b in range(5):
            da, db = a - 2, b - 2
            w1[3, 0, a, b] = g[abs(da + db)] / 6.0   # anti-diagonal '/'
            w1[4, 0, a, b] = g[abs(da - db)] / 6.0   # main diagonal '\'
    # ch5..7 unused (zero)

    # ------------------------------------------------------------------
    # conv2: wiring only. Channel k = f*4 + dy*2 + dx copies conv1 feature f
    # shifted by (dy,dx); after the 2x2 pool the 4 copies interleave into an
    # effective 8x8 map of feature f.  f: 0=ink, 1=H, 2=V, 3=diag (both).
    # ------------------------------------------------------------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    src = {0: [0], 1: [1], 2: [2], 3: [3, 4]}
    for f in range(4):
        for dy in (0, 1):
            for dx in (0, 1):
                k = f * 4 + dy * 2 + dx
                for c in src[f]:
                    w2[k, c, 2 + dy, 2 + dx] = 1.0

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (unit box, x right, y down)
    # ------------------------------------------------------------------
    PI = math.pi
    def ell(cx, cy, rx, ry, t0, t1, n=80):
        # arc of an ellipse; t=0 right, pi/2 bottom, pi left, 3pi/2 top
        return [(cx + rx * math.cos(t), cy + ry * math.sin(t))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [ell(0.5, 0.5, 0.36, 0.5, 0, 2 * PI)],
        1: [[(0.56, 0.0), (0.44, 1.0)]],
        2: [ell(0.5, 0.3, 0.3, 0.3, PI, 2.3 * PI) + [(0.15, 1.0), (0.85, 1.0)]],
        3: [ell(0.5, 0.26, 0.28, 0.26, 1.15 * PI, 2.5 * PI),
            ell(0.5, 0.74, 0.30, 0.27, 1.5 * PI, 2.85 * PI)],
        4: [[(0.32, 0.02), (0.10, 0.60)], [(0.10, 0.60), (0.92, 0.60)],
            [(0.70, 0.0), (0.70, 1.0)]],
        5: [[(0.85, 0.03), (0.28, 0.03), (0.22, 0.47)] +
            ell(0.5, 0.72, 0.32, 0.28, 1.3 * PI, 2.8 * PI)],
        6: [[(0.72, 0.0), (0.38, 0.30), (0.22, 0.60)],
            ell(0.5, 0.73, 0.29, 0.27, 0, 2 * PI)],
        7: [[(0.10, 0.03), (0.90, 0.03), (0.38, 1.0)]],
        8: [ell(0.5, 0.26, 0.24, 0.26, 0, 2 * PI),
            ell(0.5, 0.72, 0.29, 0.28, 0, 2 * PI)],
        9: [ell(0.5, 0.27, 0.27, 0.27, 0, 2 * PI), [(0.77, 0.30), (0.58, 1.0)]],
    }

    # ------------------------------------------------------------------
    # Rasterise strokes into 8x8 maps of ink / H / V / D.
    # Template cell (R,S) <-> input pixels rows 2R+6..2R+9, cols 2S+6..2S+9,
    # i.e. template coord t = (pixel - 6.5)/2 ; image centre (13.5) -> 3.5.
    # MNIST preprocessing is mimicked: scale so max extent = 20px = 10 cells,
    # then put the centre of mass at the image centre.
    # ------------------------------------------------------------------
    sigma = 0.6
    T = np.zeros((4, 10, 8, 8), np.float32)
    for d, polys in digits.items():
        pts = []  # (x, y, theta)
        for poly in polys:
            for i in range(len(poly) - 1):
                (x0, y0), (x1, y1) = poly[i], poly[i + 1]
                L = math.hypot(x1 - x0, y1 - y0)
                n = max(2, int(L / 0.01))
                th = math.atan2(y1 - y0, x1 - x0)
                for j in range(n):
                    u = j / (n - 1)
                    pts.append((x0 + u * (x1 - x0), y0 + u * (y1 - y0), th))
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        ths = np.array([p[2] for p in pts])
        s = 10.0 / max(xs.max() - xs.min(), ys.max() - ys.min())
        xs = xs * s; ys = ys * s
        xs += 3.5 - xs.mean(); ys += 3.5 - ys.mean()   # centre of mass -> centre
        wts = np.stack([np.ones_like(ths),
                        np.cos(ths) ** 4,          # horizontal-ness
                        np.sin(ths) ** 4,          # vertical-ness
                        np.sin(2 * ths) ** 2])     # diagonal-ness
        for R in range(8):
            for S in range(8):
                gw = np.exp(-((ys - (R + 0.5)) ** 2 + (xs - (S + 0.5)) ** 2) / (2 * sigma ** 2))
                T[:, d, R, S] = (wts * gw).sum(axis=1)
        m = T[0, d].max()
        T[:, d] = np.clip(T[:, d] / (0.8 * m), 0.0, 1.0)

    # discriminative templates: subtract the class mean per feature map
    Tc = T - T.mean(axis=1, keepdims=True)
    fscale = [0.35, 0.25, 0.25, 0.25]   # ink, H, V, D

    # ------------------------------------------------------------------
    # fc: place the 8x8 templates into the (channel,row,col) flatten order
    # ------------------------------------------------------------------
    wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    for d in range(10):
        for f in range(4):
            for dy in (0, 1):
                for dx in (0, 1):
                    k = f * 4 + dy * 2 + dx
                    for r in range(4):
                        for s_ in range(4):
                            idx = k * 16 + r * 4 + s_
                            wf[d, idx] = fscale[f] * Tc[f, d, 2 * r + dy, 2 * s_ + dx]

    return {
        "conv1.weight": w1, "conv1.bias": b1,
        "conv2.weight": w2, "conv2.bias": b2,
        "fc.weight": wf, "fc.bias": bf,
    }
