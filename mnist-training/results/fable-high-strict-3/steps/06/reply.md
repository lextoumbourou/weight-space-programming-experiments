**Step 6.** The nearest-centroid rule only rewards ink where a template has ink; it never penalises ink where a digit *must be empty* — which is why the "average-looking" 8 keeps flipping between sink and never-predicted, and 6/5/3 bleed into each other. Trained linear classifiers get most of their power from such negative regions. So I now add hand-drawn **forbidden regions** per class (e.g. 0: centre hole; 1: both sides; 4: top-centre gap and bottom-left; 7: whole lower-left and lower-right; 9: bottom-left; 8: both sides of the waist; 6: upper-right; 3: left-middle; 5: upper-right and open left of the bowl; 2: left-middle and right-lower). They get negative ink weights, automatically masked out wherever the class's own (dilated) template has ink. Templates are those of step 5, plus a gentle bias calibration.

```python
import numpy as np
import math

def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 hand-drawn 5x5 detectors
    # ------------------------------------------------------------------
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    for a in range(5):                      # ch0: ink blob (Gaussian, sums to 1)
        for b in range(5):
            w1[0, 0, a, b] = math.exp(-((a - 2) ** 2 + (b - 2) ** 2) / 2.0)
    w1[0, 0] /= w1[0, 0].sum()
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
    # conv2: wiring. channel k = f*4 + dy*2 + dx = feature f shifted (dy,dx);
    # after the 2x2 pool the 4 shifts interleave into an 8x8 map of feature f.
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
                    w2[k, c, 2 + dy, 2 + dx] = 1.0

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
        6: [[(0.70, 0.0), (0.30, 0.22), (0.17, 0.60)],
            ell(0.5, 0.73, 0.31, 0.27, 0, 2 * PI)],
        7: [[(0.10, 0.03), (0.90, 0.03), (0.38, 1.0)]],
        8: [ell(0.5, 0.26, 0.24, 0.26, 0, 2 * PI),
            ell(0.5, 0.72, 0.29, 0.28, 0, 2 * PI)],
        9: [ell(0.5, 0.30, 0.30, 0.30, 0, 2 * PI),
            [(0.80, 0.33), (0.68, 0.75), (0.50, 1.0)]],
    }

    # forbidden (must-be-empty) regions per digit: rectangles (x0, x1, y0, y1)
    # in the same unit frame as the strokes
    forbid = {
        0: [(0.30, 0.70, 0.30, 0.70)],                      # centre hole
        1: [(-0.4, 0.30, 0.0, 1.0), (0.70, 1.40, 0.0, 1.0)],# both sides
        2: [(0.00, 0.35, 0.30, 0.65), (0.78, 1.00, 0.60, 0.85)],
        3: [(0.00, 0.30, 0.25, 0.75)],                      # left middle
        4: [(0.33, 0.62, 0.00, 0.30), (0.00, 0.45, 0.70, 1.00)],
        5: [(0.65, 1.00, 0.15, 0.45), (0.00, 0.25, 0.55, 0.80)],
        6: [(0.60, 1.00, 0.20, 0.50)],                      # upper right
        7: [(0.00, 0.35, 0.40, 1.00), (0.75, 1.00, 0.30, 1.00)],
        8: [(0.00, 0.18, 0.30, 0.70), (0.82, 1.00, 0.30, 0.70)],
        9: [(0.00, 0.45, 0.62, 1.00)],                      # bottom left
    }

    # ------------------------------------------------------------------
    # Rasterise strokes into 8x8 maps of ink / H / V / D and forbidden masks.
    # Cell (R,S) <-> input rows 2R+6..2R+9, cols 2S+6..2S+9 ; centre 13.5 -> 3.5.
    # Mimic MNIST preprocessing: max extent 20px = 10 cells, centre of mass at centre.
    # ------------------------------------------------------------------
    sigma = 0.8
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
        shx = 3.5 - (xs * s).mean(); shy = 3.5 - (ys * s).mean()
        xs = xs * s + shx; ys = ys * s + shy
        wts = np.stack([np.ones_like(ths), np.cos(ths) ** 4,
                        np.sin(ths) ** 4, np.sin(2 * ths) ** 2])
        for R in range(8):
            for S in range(8):
                gw = np.exp(-((ys - (R + 0.5)) ** 2 + (xs - (S + 0.5)) ** 2) / (2 * sigma ** 2))
                T[:, d, R, S] = (wts * gw).sum(axis=1)
        m = T[0, d].max()
        T[:, d] = np.clip(T[:, d] / (0.55 * m), 0.0, 1.0)
        # forbidden mask: overlap fraction of each cell with the transformed rects,
        # masked out wherever the (dilated) own template has ink
        for (x0, x1, y0, y1) in forbid[d]:
            X0, X1 = x0 * s + shx, x1 * s + shx
            Y0, Y1 = y0 * s + shy, y1 * s + shy
            for R in range(8):
                for S in range(8):
                    ov = max(0.0, min(X1, S + 1) - max(X0, S)) * max(0.0, min(Y1, R + 1) - max(Y0, R))
                    N[d, R, S] = max(N[d, R, S], ov)
        N[d] *= np.clip(1.0 - 1.3 * T[0, d], 0.0, 1.0)

    fscale = [0.30, 0.20, 0.20, 0.20]   # ink, H, V, D
    kappa = 0.24                         # negative weight on forbidden ink

    # per-class bias calibration (accumulated, gentle)
    bcal = np.array([0.99, 0.41, 0.24, 0.08, 1.40, 1.12, -0.14, 0.20, -0.27, -0.04], np.float32)

    # ------------------------------------------------------------------
    # fc: logit_d = s*(mu_d . x) - kappa*(N_d . ink) - s*0.5*||mu_d||^2 + bcal_d
    # ------------------------------------------------------------------
    M = T.copy()
    M[0] -= (kappa / fscale[0]) * N        # anti-template on the ink map
    wf = np.zeros((10, 256), np.float32)
    bf = bcal.copy()
    for d in range(10):
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
```
