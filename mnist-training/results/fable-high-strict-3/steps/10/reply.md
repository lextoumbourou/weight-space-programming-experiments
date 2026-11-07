**Step 10.** 57% — the thin-ink + forbidden-region combination works, so I extend it. Three changes: (1) The bottom 3 px of every digit were invisible (the 2's base, bottoms of 0/6/8, stem ends), which drives 2→9, 2→8, 9→8. I repurpose the four diagonal channels (least useful) as a second ink map with lower row taps (rows 8–25); only its two bottom rows are used, giving the ink map **10 rows × 8 cols covering rows 4–25**, i.e. the whole digit. (2) Forbidden regions are extended (2: whole left side + right-lower; 3: whole left; 8: waist sides, top corners, bottom-left corner) with weight 0.2. (3) Gentle bias calibration.

```python
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
    # ch3..7 unused

    # ------------------------------------------------------------------
    # conv2: wiring. channel k = f*4 + dy*2 + dx.
    #  f=0 ink   : row taps 1+dy (rows 4..21), col taps 2+dx (cols 6..23)
    #  f=1 H     : same window
    #  f=2 V     : same window
    #  f=3 ink-low: row taps 3+dy (rows 8..25); only its 2 bottom pooled rows are
    #              used, extending the ink map to rows 4..25 (10 x 8 grid).
    # ------------------------------------------------------------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    src = {0: 0, 1: 1, 2: 2, 3: 0}
    for f in range(4):
        for dy in (0, 1):
            for dx in (0, 1):
                k = f * 4 + dy * 2 + dx
                ky = (3 if f == 3 else 1) + dy
                w2[k, src[f], ky, 2 + dx] = 1.0

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
        8: [ell(0.5, 0.26, 0.24, 0.26, 0, 2 * PI),
            ell(0.5, 0.72, 0.29, 0.28, 0, 2 * PI)],
        9: [ell(0.5, 0.30, 0.30, 0.30, 0, 2 * PI),
            [(0.80, 0.33), (0.68, 0.75), (0.50, 1.0)]],
    }

    # must-be-empty regions (x0, x1, y0, y1) in the stroke frame
    forbid = {
        0: [(0.35, 0.65, 0.35, 0.65)],                          # centre hole
        1: [(-0.5, 0.20, 0.1, 0.9), (0.80, 1.50, 0.1, 0.9)],    # far sides
        2: [(0.00, 0.25, 0.30, 0.80), (0.80, 1.00, 0.55, 0.85)],# left side, right-lower
        3: [(0.00, 0.30, 0.20, 0.80)],                          # whole left side
        4: [(0.36, 0.60, 0.00, 0.25), (0.00, 0.40, 0.72, 1.0)], # top gap, bottom-left
        5: [(0.70, 1.00, 0.18, 0.40)],                          # upper right
        6: [(0.65, 1.00, 0.20, 0.50)],                          # upper right
        7: [(0.00, 0.30, 0.45, 1.0), (0.80, 1.00, 0.35, 1.0)],  # lower-left, lower-right
        8: [(0.00, 0.15, 0.30, 0.70), (0.85, 1.00, 0.30, 0.70), # waist sides
            (0.00, 0.22, 0.00, 0.15), (0.78, 1.00, 0.00, 0.15), # top corners
            (0.00, 0.20, 0.85, 1.00)],                          # bottom-left corner
        9: [(0.00, 0.40, 0.62, 1.0)],                           # bottom left
    }

    # ------------------------------------------------------------------
    # Rasterise. Ink grid: 10 rows x 8 cols, cell (R,S) <-> input rows 2R+4..2R+7,
    # cols 2S+6..2S+9. H/V grids: rows 0..7 of the same frame.
    # Image centre (13.5,13.5) -> template (row 4.5, col 3.5).
    # Mimic MNIST preprocessing: max extent 20px = 10 cells, centre of mass at centre.
    # ------------------------------------------------------------------
    sigma = 0.9
    CY, CX = 4.5, 3.5
    T = np.zeros((3, 10, 10, 8), np.float32)   # feature (ink,H,V), digit, row, col
    N = np.zeros((10, 10, 8), np.float32)
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
        wts = np.stack([np.ones_like(ths), np.cos(ths) ** 4, np.sin(ths) ** 4])
        for R in range(10):
            for S in range(8):
                gw = np.exp(-((ys - (R + 0.5)) ** 2 + (xs - (S + 0.5)) ** 2) / (2 * sigma ** 2))
                T[:, d, R, S] = (wts * gw).sum(axis=1)
        m = T[0, d].max()
        T[:, d] = np.clip(T[:, d] / (0.75 * m), 0.0, 1.0)
        for (x0, x1, y0, y1) in forbid[d]:
            X0, X1 = x0 * s + shx, x1 * s + shx
            Y0, Y1 = y0 * s + shy, y1 * s + shy
            for R in range(10):
                for S in range(8):
                    ov = max(0.0, min(X1, S + 1) - max(X0, S)) * max(0.0, min(Y1, R + 1) - max(Y0, R))
                    N[d, R, S] = max(N[d, R, S], ov)
        N[d] *= np.clip(1.0 - 2.0 * T[0, d], 0.0, 1.0)   # never penalise own ink

    s_ink, s_or = 0.30, 0.15
    kappa = 0.20

    # per-class bias calibration (accumulated, gentle)
    bcal = np.array([0.92, 0.37, 0.25, 0.02, 0.94, 1.07, -0.46, 0.14, -0.24, -0.05], np.float32)

    # effective ink template (positive part + forbidden negative part)
    Mink = s_ink * T[0] - kappa * N          # (10 digits, 10 rows, 8 cols)

    # ------------------------------------------------------------------
    # fc: logit_d = Mink_d . ink10x8 + s_or*(H_d.H + V_d.V) - 0.5*||mu_d||^2 + bias
    # ------------------------------------------------------------------
    wf = np.zeros((10, 256), np.float32)
    bf = bcal.copy()
    for d in range(10):
        bf[d] += 0.15 * kappa * float(N[d].sum())
        bf[d] -= 0.5 * s_ink * float((T[0, d] ** 2).sum())
        bf[d] -= 0.5 * s_or * float((T[1, d, :8] ** 2).sum() + (T[2, d, :8] ** 2).sum())
        for dy in (0, 1):
            for dx in (0, 1):
                for r in range(4):
                    for s_ in range(4):
                        R, S = 2 * r + dy, 2 * s_ + dx
                        # f=0: ink rows 0..7
                        wf[d, (0 * 4 + dy * 2 + dx) * 16 + r * 4 + s_] = Mink[d, R, S]
                        # f=1,2: H and V maps
                        wf[d, (1 * 4 + dy * 2 + dx) * 16 + r * 4 + s_] = s_or * T[1, d, R, S]
                        wf[d, (2 * 4 + dy * 2 + dx) * 16 + r * 4 + s_] = s_or * T[2, d, R, S]
                        # f=3: lower ink window; pooled row r=3 <-> ink rows 8,9
                        if r == 3:
                            wf[d, (3 * 4 + dy * 2 + dx) * 16 + r * 4 + s_] = Mink[d, 8 + dy, S]

    return {
        "conv1.weight": w1, "conv1.bias": b1,
        "conv2.weight": w2, "conv2.bias": b2,
        "fc.weight": wf, "fc.bias": bf,
    }
```
