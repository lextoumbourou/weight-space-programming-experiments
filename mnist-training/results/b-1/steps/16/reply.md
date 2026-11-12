## Step 16: add orientation features back, and nudge per-class offsets

**Where things stand.** Cosine matching on the corrected templates gave the best result so far: 60.7% accuracy, loss 1.33. Two problems remain:
- **Over-predicted:** "8" (about 1,450 predictions for about 1,000 images) and "9" (about 1,350).
- **Under-predicted:** "4" (334) and "5" (525). The worst confusions are 4→9 (419), 5→8 (374), 0→8 (297), 3→8 (247) and 4→6 (141).

**Changes in this step:**

1. **Offsets that keep the score scale-invariant.** A plain bias would break the scale invariance, so instead I add a multiple of the normalised mean template μ̂ to each class weight:

   `logit_d = s · f · (T̂_d + β_d · μ̂)`

   Since f·μ̂ is roughly 0.85·‖f‖ for any digit, β_d acts like a fixed shift in cosine similarity. The shifts are:
   - 8: −0.03
   - 9: −0.02
   - 6: −0.01
   - 4: +0.03
   - 5: +0.02
   - 0: +0.01
   - 7: +0.01

2. **Orientation features return as a second cosine term with half weight.** The four oriented-stroke density channels (0–3) get their own normalised templates. Each template value is the stroke density weighted by how well the stroke angle matches the channel, using `max(0, cos 2Δ)`. They should help separate:
   - 4 from 9: the 4's left stroke is a diagonal "/" and it has a mid-height horizontal bar.
   - 5 from 3 and 8: 5 has a top horizontal bar and a vertical stroke at upper left.

   Ink and orientation parts are scored separately: `logit = s·(f_ink·T̂_ink + 0.5·f_ori·T̂_ori)`. This way the uncertain orientation magnitude cannot swamp the ink match.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: oriented line detectors + ink ----------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    off = np.arange(-2, 3)
    Y, X = np.meshgrid(off, off, indexing='ij')
    # 0: horizontal, 1: vertical, 2: "\" (down-right), 3: "/" (up-right)
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        d = np.abs(-math.sin(th) * X + math.cos(th) * Y)
        g = np.exp(-d ** 2 / (2 * 0.8 ** 2))
        w = g - g.mean()
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.05
    # channel 4: ink (plus-shaped average)
    W1[4, 0, 2, 2] = 0.5
    W1[4, 0, 1, 2] = W1[4, 0, 3, 2] = W1[4, 0, 2, 1] = W1[4, 0, 2, 3] = 0.125

    # ---------------- conv2 ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    avg = np.outer([1, 2, 1], [1, 2, 1]) / 16.0
    chan_src = {}
    for k in range(4):                                   # 0-3 orientation density
        chan_src[k] = (k, 2, 2)
    ink_taps = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3), (2, 1), (2, 3), (1, 2), (3, 2)]
    for i, (ky, kx) in enumerate(ink_taps):              # 4-12 ink density at 9 shifts
        chan_src[4 + i] = (4, ky, kx)
    for ch, (src, ky, kx) in chan_src.items():
        W2[ch, src, ky - 1:ky + 2, kx - 1:kx + 2] = avg

    # ---------------- digit strokes (x=col, y=row) ----------------
    def ellipse(cx, cy, rx, ry, n=48):
        t = np.linspace(0, 2 * math.pi, n + 1)
        return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in t]

    digits = {
        0: [ellipse(14, 14, 6.0, 9.5)],
        1: [[(16, 4.5), (12, 23.5)]],
        2: [[(8, 9), (10, 6), (14, 4.5), (18, 5.5), (20, 9), (18, 13), (13, 18), (8, 23), (14, 23), (21, 23)]],
        3: [[(8, 6), (12, 4.5), (17, 5), (19, 8), (17, 12), (12, 13.5), (17, 15), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        4: [[(10, 4.5), (8, 15), (20, 15)], [(17, 6), (17, 23.5)]],
        5: [[(20, 4.5), (10, 4.5), (9, 13), (14, 12), (19, 14), (20, 18), (18, 22), (13, 23.5), (8, 22)]],
        6: [[(17, 4.5), (12, 8), (9, 13), (8, 18), (10, 22), (14, 23.5), (18, 21), (19, 17), (16, 14), (12, 14), (9, 17)]],
        7: [[(8, 5), (20, 5), (14, 23.5)]],
        8: [ellipse(14.5, 8.5, 4.0, 4.0), ellipse(13.5, 18.5, 5.0, 5.0)],
        9: [ellipse(14, 9, 4.5, 4.5), [(18.5, 10), (15, 23.5)]],
    }
    xscale = {0: 1.25, 1: 1.0, 2: 1.15, 3: 1.15, 4: 1.2, 5: 1.15, 6: 1.15, 7: 1.15, 8: 1.3, 9: 1.3}

    def sample(strokes):
        pts, angs, steps = [], [], []
        for poly in strokes:
            for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                n = max(1, int(L / 0.25))
                phi = math.atan2(y1 - y0, x1 - x0)
                for j in range(n):
                    t = (j + 0.5) / n
                    pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
                    angs.append(phi)
                    steps.append(L / n)
        return np.array(pts), np.array(angs), np.array(steps)

    def box(t, h, soft):
        return 1.0 / (1.0 + np.exp((np.abs(t) - h) / soft))

    # ---------------- templates (orientation 0-3, ink 4-12) ----------------
    COM = 13.8
    T = np.zeros((10, 16, 4, 4))
    for dgt, strokes in digits.items():
        sx = xscale[dgt]
        strokes = [[(14 + (x - 14) * sx, y) for (x, y) in poly] for poly in strokes]
        P, A, S = sample(strokes)
        com = (P * S[:, None]).sum(0) / S.sum()
        P = P - com + COM                       # centre-of-mass alignment
        for ch in range(13):
            src, ky, kx = chan_src[ch]
            if src < 4:
                o = np.maximum(0.0, np.cos(2 * (A - thetas[src])))
            else:
                o = np.ones_like(A)
            for r in range(4):
                cy = 4 * r + 2 * ky + 3.5
                for c in range(4):
                    cx = 4 * c + 2 * kx + 3.5
                    K = box(P[:, 0] - cx, 3.0, 1.5) * box(P[:, 1] - cy, 3.0, 1.5)
                    T[dgt, ch, r, c] = np.sum(S * o * K) / 36.0 * 2.5

    # ---------------- fc: two-part cosine matching + scale-invariant offsets ----------------
    s = 10.0
    lam_ori = 0.5
    beta = {8: -0.03, 9: -0.02, 6: -0.01, 4: 0.03, 5: 0.02, 0: 0.01, 7: 0.01}
    ink = np.zeros((16, 4, 4), dtype=bool); ink[4:13] = True
    ori = np.zeros((16, 4, 4), dtype=bool); ori[0:4] = True

    def unit(v):
        return v / (np.linalg.norm(v) + 1e-8)

    mu = T.mean(axis=0)
    mu_ink = np.where(ink, mu, 0.0); mu_ink = unit(mu_ink)
    mu_ori = np.where(ori, mu, 0.0); mu_ori = unit(mu_ori)

    Wfc = np.zeros((10, 16, 4, 4))
    bfc = np.zeros(10)
    for dgt in range(10):
        ti = unit(np.where(ink, T[dgt], 0.0))
        to = unit(np.where(ori, T[dgt], 0.0))
        b = beta.get(dgt, 0.0)
        Wfc[dgt] = s * ((ti + b * mu_ink) + lam_ori * (to + b * mu_ori))

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.reshape(10, 256).astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
