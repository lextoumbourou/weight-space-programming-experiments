## Step 6: HOG-style summed features instead of max-pooled presence

**Why accuracy is stuck.** Accuracy has plateaued at about 62%. In the current design, conv2 passes each conv1 feature through a single tap, so the max-pools only report whether a stroke is present anywhere in a cell. Those values saturate near 1 and look similar for most digits. That is why the cosine scores of the classes sit so close together.

**New feature extractor.**
- conv1 is unchanged: channel 0 detects ink, channels 1–4 detect strokes in four orientations.
- conv2 channel k (k = 0–4) now sums a 3×3 block of conv1 channel k on the 12×12 pooled map, instead of copying one tap.
- After the final 2×2 max-pool, each of the 4×4 cells reports how much stroke of each orientation lies in an image window about 8 px wide. The cells are still centred at 7.5, 11.5, 15.5 and 19.5.
- These amounts behave much like a histogram of oriented gradients (HOG), which is far more informative than presence alone.

**Matching templates.** The templates are computed from the same stroke descriptions, now on the 12×12 pooled grid. That grid is then summed over 3×3 blocks and max-reduced exactly as conv2 and the second pool combine it.

**Classifier.** The fc is again a normalised correlation with each digit's template. The ink channel is down-weighted to 0.3. α drops to 6 because the summed features are several times larger than before.

```python
import numpy as np
import math

def build_weights():
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)

    # ---------------- conv1 ----------------
    # channel 0: ink detector (Gaussian blur, sums to 1)
    g = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            g[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / 2.0)
    g /= g.sum()
    W1[0, 0] = g
    b1[0] = -0.05

    # channels 1..4: oriented line detectors (0=horiz, pi/2=vert, pi/4="\", 3pi/4="/")
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                r, c = i - 2, j - 2
                d = r * math.cos(th) - c * math.sin(th)   # across stroke
                l = r * math.sin(th) + c * math.cos(th)   # along stroke
                K[i, j] = (1 - d * d / 2.0) * math.exp(-d * d / 4.0) * math.exp(-l * l / 12.0)
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[1 + k, 0] = K
        b1[1 + k] = -0.1

    # ---------------- conv2: 3x3 local SUM of each conv1 channel ----------------
    # conv2 channel k (k=0..4) = sum over pool1 rows/cols r+1..r+3 of conv1 channel k
    for k in range(5):
        W2[k, k, 1:4, 1:4] = 1.0

    # ---------------- digit stroke descriptions (row, col) ----------------
    def poly(pts):
        out = []
        for (r0, c0), (r1, c1) in zip(pts[:-1], pts[1:]):
            L = math.hypot(r1 - r0, c1 - c0)
            n = max(2, int(L / 0.25))
            phi = math.atan2(r1 - r0, c1 - c0) % math.pi
            for t in np.linspace(0, 1, n):
                out.append((r0 + t * (r1 - r0), c0 + t * (c1 - c0), phi))
        return out

    def ellipse(cr, cc, rr, rc, t0=0.0, t1=2 * math.pi):
        out = []
        for t in np.linspace(t0, t1, 200):
            r = cr + rr * math.sin(t)
            c = cc + rc * math.cos(t)
            dr = rr * math.cos(t)
            dc = -rc * math.sin(t)
            out.append((r, c, math.atan2(dr, dc) % math.pi))
        return out

    digits = {
        0: ellipse(14, 14, 9.5, 6.5),
        1: poly([(4, 15.5), (24, 12.5)]),
        2: poly([(8, 8.5), (5, 11), (4.5, 14), (5.5, 17.5), (8.5, 19), (12, 17),
                 (16, 13), (20, 9.5), (23, 8), (23, 14), (23, 21)]),
        3: poly([(6, 9), (4.5, 13), (5.5, 17.5), (8.5, 18.5), (12, 16), (13.5, 12)]) +
           poly([(13.5, 12), (14.5, 17), (18, 19.5), (21.5, 18), (23.5, 13), (22, 8.5)]),
        4: poly([(4, 10), (15, 8)]) + poly([(15, 8), (15, 21)]) + poly([(5, 17), (24, 17)]),
        5: poly([(4.5, 20), (4.5, 10)]) + poly([(4.5, 10), (12, 9)]) +
           poly([(12, 9), (11, 14), (12.5, 18), (16.5, 19.5), (20.5, 18), (23, 14), (22.5, 8.5)]),
        6: poly([(4, 17), (7.5, 12.5), (12, 9.5), (17, 8.5), (21, 9.5), (23.5, 13),
                 (22, 17.5), (18, 19), (15, 16.5), (14.5, 12), (16, 9)]),
        7: poly([(5, 8), (5, 20)]) + poly([(5, 20), (24, 12)]),
        8: ellipse(9, 14, 4.5, 4.5) + ellipse(18.5, 14, 5, 5.5),
        9: ellipse(9, 14.5, 4.5, 4.5) + poly([(9, 19), (24, 16)]),
    }

    # ---------------- analytic templates ----------------
    # pool1 cell q is centred at image coord 2q+2.5 and responds to strokes within ~2px
    def m(x):
        return 1.0 / (1.0 + math.exp((abs(x) - 2.0) * 2.0))
    def omatch(phi, th):
        return ((1 + math.cos(2 * (phi - th))) / 2.0) ** 2

    T = np.zeros((10, 5, 4, 4))
    for d, pts in digits.items():
        # P: expected pool1-level map, channel 0 = ink, 1..4 = orientations
        P = np.zeros((5, 12, 12))
        for (r, c, phi) in pts:
            for qr in range(12):
                mr = m(r - (2 * qr + 2.5))
                if mr < 1e-3:
                    continue
                for qc in range(12):
                    sp = mr * m(c - (2 * qc + 2.5))
                    if sp < 1e-3:
                        continue
                    P[0, qr, qc] = max(P[0, qr, qc], sp)
                    for k, th in enumerate(thetas):
                        P[1 + k, qr, qc] = max(P[1 + k, qr, qc], sp * omatch(phi, th))
        # conv2 3x3 sum (rows r+1..r+3) then 2x2 max-pool, done on the template map
        for ch in range(5):
            for sr in range(4):
                for sc in range(4):
                    best = 0.0
                    for r in (2 * sr, 2 * sr + 1):
                        for c in (2 * sc, 2 * sc + 1):
                            best = max(best, P[ch, r + 1:r + 4, c + 1:c + 4].sum())
                    T[d, ch, sr, sc] = best

    # ---------------- fc: normalised correlation ----------------
    chw = np.array([0.3, 1.0, 1.0, 1.0, 1.0])   # ink channel down-weighted
    alpha = 6.0
    for d in range(10):
        v = np.zeros(256)
        for ch in range(5):
            v[ch * 16:(ch + 1) * 16] = chw[ch] * T[d, ch].reshape(-1)
        v /= np.linalg.norm(v)
        Wf[d] = alpha * v
    bf[:] = 0.0

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
