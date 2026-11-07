## Step 12: add loop and "tube" detectors to the step-9 features

**What steps 10 and 11 showed.** Both made things worse.
- The ink penalty in step 10 turned "8" into the attractor, because an 8 has ink almost everywhere.
- The signed edge detectors in step 11 produced diffuse responses, and again everything drifted to "8".

So I go back to step 9's features, the best so far at 64.6%.

**The main remaining errors are topological.** The biggest confusions are 0→2, 8→2, 5→6, 7→9, 4→9 and 9→8. All of them come down to whether, and where, the digit has a closed loop. Orientation energy cannot express that.

**New conv1 channel 5: thresholded ink.** It is a blur with gain 1.3 and bias −0.3, so after the first pool it reads roughly 0 for background and 1 for a stroke.

**New conv2 channels, each a 5×5 kernel on that ink map, with ReLU.**

| conv2 channel | Fires when | Main targets |
|---|---|---|
| 5: small loop | ink on all four sides about 4 px from the centre, and an empty centre | loops of 8, 9, 6 |
| 6: vertical tube | ink on the left and right sides, and an empty central column | the interior of 0, the open top of 4 |
| 7: horizontal tube | ink above and below, and an empty central row | half-loops such as those of 3 |

**Templates.** I compute the expected 4×4 map for each new channel from the same hand-drawn strokes. To do so I apply the kernel formula to the analytic ink-presence map of each prototype.

**fc.** Still one cosine-normalised template per class. Channels 0–4 are as in step 9. The loop and tube channels get weight 3, because their values are only 0–1 while the summed orientation features are larger. α = 4 and the biases are 0.

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
    # ch0: ink (Gaussian blur, sum 1)
    def gauss(sig):
        G = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                G[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / (2 * sig * sig))
        return G / G.sum()
    W1[0, 0] = gauss(1.0)
    b1[0] = -0.05

    # ch1..4: oriented line detectors (0=horiz, pi/2=vert, pi/4="\", 3pi/4="/")
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                r, c = i - 2, j - 2
                d = r * math.cos(th) - c * math.sin(th)
                l = r * math.sin(th) + c * math.cos(th)
                K[i, j] = (1 - d * d / 2.0) * math.exp(-d * d / 4.0) * math.exp(-l * l / 12.0)
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[1 + k, 0] = K
        b1[1 + k] = -0.1

    # ch5: thresholded ink presence, ~0 background, ~1 on stroke (used by loop detectors)
    W1[5, 0] = 1.3 * gauss(0.8)
    b1[5] = -0.3

    # ---------------- conv2 ----------------
    # ch0..4: 3x3 local sums of conv1 ch0..4 (ink + orientation energy)
    for k in range(5):
        W2[k, k, 1:4, 1:4] = 1.0

    # ch5: small loop: ink on 4 sides (offset 2 pool1 = ~4px), empty centre
    KL = np.zeros((5, 5))
    for t in (1, 2, 3):
        KL[0, t] += 1 / 3.0; KL[4, t] += 1 / 3.0
        KL[t, 0] += 1 / 3.0; KL[t, 4] += 1 / 3.0
    KL[2, 2] = -3.0
    bL = -2.4
    # ch6: vertical tube: ink left and right, empty central column
    KV = np.zeros((5, 5))
    for t in (1, 2, 3):
        KV[t, 0] = 1 / 3.0; KV[t, 4] = 1 / 3.0; KV[t, 2] = -1.0
    bV = -1.2
    # ch7: horizontal tube: ink above and below, empty central row
    KH = KV.T.copy()
    bH = -1.2
    for ch, (Kk, bk) in zip((5, 6, 7), ((KL, bL), (KV, bV), (KH, bH))):
        W2[ch, 5] = Kk
        b2[ch] = bk

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
    def m(x):
        return 1.0 / (1.0 + math.exp((abs(x) - 2.0) * 2.0))
    def omatch(phi, th):
        return ((1 + math.cos(2 * (phi - th))) / 2.0) ** 2

    blur = np.array([0.25, 0.5, 0.25])
    def blur2(A):
        n = A.shape[0]
        B = np.zeros_like(A)
        for i in range(n):
            for o, w in zip((-1, 0, 1), blur):
                if 0 <= i + o < n:
                    B[i] += w * A[i + o]
        C = np.zeros_like(B)
        for j in range(n):
            for o, w in zip((-1, 0, 1), blur):
                if 0 <= j + o < n:
                    C[:, j] += w * B[:, j + o]
        return C

    NCH = 8
    T = np.zeros((10, NCH, 4, 4))
    for d, pts in digits.items():
        P = np.zeros((5, 12, 12))      # pool1-level expected maps: ink, 4 orientations
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
        # channels 0..4: blurred 3x3 sums, 2x2 max
        for ch in range(5):
            Pb = blur2(blur2(P[ch]))
            for sr in range(4):
                for sc in range(4):
                    best = 0.0
                    for r in (2 * sr, 2 * sr + 1):
                        for c in (2 * sc, 2 * sc + 1):
                            best = max(best, Pb[r + 1:r + 4, c + 1:c + 4].sum())
                    T[d, ch, sr, sc] = best
        # channels 5..7: loop / tube formulas on the ink-presence map, relu, 2x2 max
        for ch, (Kk, bk) in zip((5, 6, 7), ((KL, bL), (KV, bV), (KH, bH))):
            O = np.zeros((8, 8))
            for r in range(8):
                for c in range(8):
                    O[r, c] = max(0.0, float((Kk * P[0, r:r + 5, c:c + 5]).sum()) + bk)
            Q = np.zeros((4, 4))
            for sr in range(4):
                for sc in range(4):
                    Q[sr, sc] = O[2 * sr:2 * sr + 2, 2 * sc:2 * sc + 2].max()
            T[d, ch] = blur2(Q)        # mild positional tolerance

    # ---------------- fc: normalised correlation ----------------
    chw = np.array([0.3, 1.0, 1.0, 1.0, 1.0, 3.0, 3.0, 3.0])
    alpha = 4.0
    for d in range(10):
        v = np.zeros(256)
        for ch in range(NCH):
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
