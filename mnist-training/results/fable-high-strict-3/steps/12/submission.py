import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 hand-drawn 5x5 detectors
    # ------------------------------------------------------------------
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    # ch0: ink core detector: ReLU(2*Gaussian*I - 0.7) -> thin bands, faint ink dropped
    for a in range(5):
        for b in range(5):
            w1[0, 0, a, b] = math.exp(-((a - 2) ** 2 + (b - 2) ** 2) / 2.0)
    w1[0, 0] *= 2.0 / w1[0, 0].sum()
    b1[0] = -0.7
    prof = np.array([-1.0, 0.5, 1.0, 0.5, -1.0])
    w1[1, 0] = np.outer(prof, np.ones(5) / 5.0) / 2.0   # ch1: horizontal stroke
    w1[2, 0] = w1[1, 0].T                                 # ch2: vertical stroke
    g = {0: 1.0, 1: 0.3, 2: -0.6, 3: -0.6, 4: -0.6}
    for a in range(5):
        for b in range(5):
            da, db = a - 2, b - 2
            w1[3, 0, a, b] = g[abs(da + db)] / 6.0        # ch3: '/' diagonal
            w1[4, 0, a, b] = g[abs(da - db)] / 6.0        # ch4: '\' diagonal
    # ch5..7 unused

    # ------------------------------------------------------------------
    # conv2: wiring. channel k = f*4 + dy*2 + dx = feature f shifted (dy,dx).
    # Row taps 1+dy (input rows 4..21), column taps 2+dx (input cols 6..23).
    # After the 2x2 pool the 4 shifts interleave into an 8x8 map of feature f.
    # f: 0=ink, 1=horizontal, 2=vertical, 3=diagonal (both)
    # ------------------------------------------------------------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    src = {0: [0], 1: [1], 2: [2], 3: [3, 4]}
    for f in range(4):
        for dy in (0, 1):
            for dx in (0, 1):
                k = f * 4 + dy * 2 + dx
                for c in src[f]:
                    w2[k, c, 1 + dy, 2 + dx] = 1.0

    # ------------------------------------------------------------------
    # Hand-drawn digit strokes (unit box, x right, y down)
    # ------------------------------------------------------------------
    PI = math.pi
    def ell(cx, cy, rx, ry, t0, t1, n=80):
        return [(cx + rx * math.cos(t), cy + ry * math.sin(t))
                for t in np.linspace(t0, t1, n)]

    digits = {
        0: [ell(0.5, 0.5, 0.37, 0.5, 0, 2 * PI)],
        1: [[(0.56, 0.0), (0.44, 1.0)]],
        2: [ell(0.5, 0.3, 0.3, 0.3, PI, 2.3 * PI) + [(0.15, 1.0), (0.85, 1.0)]],
        3: [ell(0.5, 0.26, 0.28, 0.26, 1.15 * PI, 2.5 * PI),
            ell(0.5, 0.74, 0.30, 0.27, 1.5 * PI, 2.85 * PI)],
        4: [[(0.28, 0.0), (0.15, 0.55)], [(0.15, 0.55), (0.95, 0.55)],
            [(0.68, 0.0), (0.62, 1.0)]],
        5: [[(0.85, 0.02), (0.25, 0.02), (0.20, 0.45)] +
            ell(0.5, 0.72, 0.33, 0.28, 1.25 * PI, 2.85 * PI)],
        6: [[(0.72, 0.0), (0.38, 0.30), (0.22, 0.60)],
            ell(0.5, 0.73, 0.29, 0.27, 0, 2 * PI)],
        7: [[(0.10, 0.03), (0.90, 0.03), (0.38, 1.0)]],
        # 8: slimmer than before (real 8s are narrow)
        8: [ell(0.5, 0.26, 0.21, 0.26, 0, 2 * PI),
            ell(0.5, 0.72, 0.25, 0.28, 0, 2 * PI)],
        9: [ell(0.5, 0.30, 0.30, 0.30, 0, 2 * PI),
            [(0.80, 0.33), (0.68, 0.75), (0.50, 1.0)]],
    }

    # must-be-empty regions (x0, x1, y0, y1, weight) in the stroke frame
    forbid = {
        0: [(0.35, 0.65, 0.35, 0.65, 1.0)],                               # centre hole
        1: [(-0.5, 0.20, 0.1, 0.9, 1.0), (0.80, 1.50, 0.1, 0.9, 1.0)],    # far sides
        2: [(0.00, 0.30, 0.35, 0.65, 1.0), (0.00, 0.20, 0.55, 0.80, 1.0)],# left middle, far lower-left
        3: [(0.00, 0.34, 0.10, 0.80, 1.0)],                               # whole left side
        4: [(0.36, 0.60, 0.00, 0.25, 1.0), (0.00, 0.40, 0.75, 1.0, 1.0)], # top gap, bottom-left
        5: [(0.70, 1.00, 0.18, 0.40, 1.5)],                               # upper right
        6: [(0.65, 1.00, 0.20, 0.50, 1.3)],                               # upper right
        7: [(0.00, 0.30, 0.45, 1.0, 1.0), (0.80, 1.00, 0.35, 1.0, 1.0)],  # lower-left, lower-right
        8: [(0.00, 0.17, 0.30, 0.70, 1.0), (0.83, 1.00, 0.30, 0.70, 1.0), # waist sides
            (0.78, 1.00, 0.00, 0.15, 1.0)],                               # top-right corner
        9: [(0.00, 0.45, 0.62, 1.0, 1.0)],                                # bottom left
    }

    # ------------------------------------------------------------------
    # Rasterise strokes into 8x8 maps of ink / H / V / D (+ forbidden masks).
    # Cell (R,S) <-> input rows 2R+4..2R+7, cols 2S+6..2S+9.
    # Image centre (13.5,13.5) -> template (row 4.5, col 3.5).
    # Mimic MNIST preprocessing: max extent 20px = 10 cells, centre of mass at centre.
    # ------------------------------------------------------------------
    sigma = 0.9
    CY, CX = 4.5, 3.5
    T = np.zeros((4, 10, 8, 8), np.float32)
    N = np.zeros((10, 8, 8), np.float32)
    for d, polys in digits.items():
        pts = []
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
        shx = CX - (xs * s).mean(); shy = CY - (ys * s).mean()
        xs = xs * s + shx; ys = ys * s + shy
        wts = np.stack([np.ones_like(ths), np.cos(ths) ** 4,
                        np.sin(ths) ** 4, np.sin(2 * ths) ** 2])
        for R in range(8):
            for S in range(8):
                gw = np.exp(-((ys - (R + 0.5)) ** 2 + (xs - (S + 0.5)) ** 2) / (2 * sigma ** 2))
                T[:, d, R, S] = (wts * gw).sum(axis=1)
        m = T[0, d].max()
        T[:, d] = np.clip(T[:, d] / (0.75 * m), 0.0, 1.0)
        for (x0, x1, y0, y1, wgt) in forbid[d]:
            X0, X1 = x0 * s + shx, x1 * s + shx
            Y0, Y1 = y0 * s + shy, y1 * s + shy
            for R in range(8):
                for S in range(8):
                    ov = max(0.0, min(X1, S + 1) - max(X0, S)) * max(0.0, min(Y1, R + 1) - max(Y0, R))
                    N[d, R, S] = max(N[d, R, S], wgt * ov)
        N[d] *= np.clip(1.0 - 2.0 * T[0, d], 0.0, 1.0)   # never penalise own ink

    fscale = [0.30, 0.15, 0.15, 0.15]   # ink, H, V, D
    kappa = 0.15                         # negative weight on forbidden ink

    # per-class bias calibration (accumulated, gentle)
    bcal = np.array([0.99, 0.40, 0.27, 0.02, 0.96, 1.00, -0.37, 0.14, -0.28, -0.09], np.float32)

    # ------------------------------------------------------------------
    # fc: logit_d = s*(mu_d . x) - kappa*(N_d . ink) - s*0.5*||mu_d||^2 + bias
    # ------------------------------------------------------------------
    M = T.copy()
    M[0] -= (kappa / fscale[0]) * N
    wf = np.zeros((10, 256), np.float32)
    bf = bcal.copy()
    for d in range(10):
        bf[d] += 0.12 * kappa * float(N[d].sum())   # small compensation for own-class spill
        for f in range(4):
            bf[d] -= 0.5 * fscale[f] * float((T[f, d] ** 2).sum())
            for dy in (0, 1):
                for dx in (0, 1):
                    k = f * 4 + dy * 2 + dx
                    for r in range(4):
                        for s_ in range(4):
                            idx = k * 16 + r * 4 + s_
                            wf[d, idx] = fscale[f] * M[f, d, 2 * r + dy, 2 * s_ + dx]

    return {
        "conv1.weight": w1, "conv1.bias": b1,
        "conv2.weight": w2, "conv2.bias": b2,
        "fc.weight": wf, "fc.bias": bf,
    }
