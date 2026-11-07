# Step 10: switching conv1 from line detectors to signed edge detectors

**Why change the features now**

Accuracy has stalled at about 82.5%, and tuning shrinkage no longer helps, so the features themselves are the likely limit. The zero-mean ridge filters in conv1 respond well only to strokes about 2–3 px wide. A bold stroke (4 px or wider) fills the whole 5×5 window and gives almost no response, and MNIST has many bold digits.

**The new conv1: signed edge detectors**

conv1 now holds 8 signed edge detectors, which are derivatives of a Gaussian. Each responds where ink increases along its direction φ = 0°, 45°, …, 315°, in the style of HOG features.

- Every stroke, thin or bold, produces two edges with opposite signs. The response therefore depends little on stroke thickness.
- The sign shows which side of a stroke the ink is on. This tells the inside of a loop from the outside, which should help with 3/5, 7/9 and 4/9.

**Matching change to the synthetic feature model**

Each stroke point now contributes two edge points. They sit at ± the stroke's half-width along the normal, which is drawn at random from 0.7–1.8 px for each sample. Each edge point has an inward-pointing gradient direction, and the direction tuning is max(0, cos Δ − 0.15) / 0.85.

**Unchanged and reset**

conv2 pooling, the stroke models, the LDA with nuisance directions and alpha = 2.5 are unchanged. γ is 0.8. The old biases were calibrated for the old features, so I reset them to 0 and will recalibrate them in the next step.

```python
import numpy as np
import math

def build_weights():
    rng = np.random.RandomState(0)

    # ---------------- conv1: 8 signed edge detectors (derivative of Gaussian) ----------------
    # Channel c responds where ink INCREASES along direction phi_c = c*45 deg
    # (x right, y down). Antisymmetric -> zero-mean; step edge -> ~1.
    phis = np.arange(8) * np.pi / 4
    w1 = np.zeros((8, 1, 5, 5), np.float32)
    yy, xx = np.mgrid[-2:3, -2:3]
    sig = 1.2
    env = np.exp(-(xx ** 2 + yy ** 2) / (2 * sig ** 2))
    for c in range(8):
        d = xx * np.cos(phis[c]) + yy * np.sin(phis[c])
        g = d * env
        g /= g[d > 1e-9].sum()          # response to ideal step edge = 1
        w1[c, 0] = g
    b1 = np.full(8, -0.15, np.float32)

    # ---------------- conv2: spatial pooling per edge direction ----------------
    w2 = np.zeros((16, 8, 5, 5), np.float32)
    for c in range(8):
        w2[c, c, 1:4, 1:4] = 1.0     # ch 0-7: broad cells (8-px bands, stride 4)
        w2[8 + c, c, 2, 2] = 1.0     # ch 8-15: sharp cells (4-px bands)
    b2 = np.zeros(16, np.float32)

    # ---------------- stroke primitives (u right, v down, box [-1,1]^2) ----------------
    def line(a, b, n=40):
        t = np.linspace(0, 1, n)[:, None]
        return np.array(a, float)[None] * (1 - t) + np.array(b, float)[None] * t

    def arc(cx, cy, rx, ry, a0, a1, n=120):
        a = np.radians(np.linspace(a0, a1, n))
        return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)

    def fig8(k=0.65, n=240):
        t = np.linspace(0, 2 * np.pi, n)
        return np.stack([k * np.sin(2 * t), np.cos(t)], 1)

    digits = {
        0: [[arc(0, 0, 0.85, 1.0, 0, 360)],
            [arc(0, 0, 0.55, 1.0, 0, 360)]],
        1: [[line((0.0, -1), (0.0, 1))],
            [line((-0.35, -0.75), (0.0, -1)), line((0.0, -1), (0.0, 1))],
            [line((-0.35, -0.75), (0.0, -1)), line((0.0, -1), (0.0, 1)),
             line((-0.35, 1), (0.35, 1))]],
        2: [[arc(0, -0.45, 0.8, 0.55, 180, 380),
             line((0.75, -0.26), (-0.8, 0.95)),
             line((-0.8, 0.95), (0.9, 0.95))]],
        3: [[arc(0, -0.5, 0.75, 0.5, 200, 450),
             arc(0, 0.5, 0.8, 0.5, 270, 520)]],
        4: [[line((-0.25, -1), (-0.8, 0.35)),
             line((-0.8, 0.35), (0.8, 0.35)),
             line((0.45, -0.9), (0.45, 1))],
            [line((-0.7, -1), (-0.7, 0.2)),
             line((-0.7, 0.2), (0.8, 0.2)),
             line((0.4, -1), (0.4, 1))],
            [line((-0.1, -1), (-0.75, 0.2)),
             line((-0.75, 0.2), (0.6, 0.2)),
             line((0.5, -1), (0.5, 1)),
             line((-0.1, -1), (0.2, -0.95))]],
        5: [[line((0.8, -1), (-0.45, -1)),
             line((-0.45, -1), (-0.55, -0.1)),
             arc(-0.05, 0.45, 0.75, 0.55, 240, 510)]],
        6: [[line((0.45, -1), (-0.65, 0.35)),
             arc(0, 0.45, 0.68, 0.55, 0, 360)],
            [arc(0.55, 0.45, 1.2, 1.45, 245, 180),
             arc(0, 0.45, 0.68, 0.55, 0, 360)]],
        7: [[line((-0.8, -1), (0.8, -1)),
             line((0.8, -1), (-0.15, 1))],
            [line((-0.8, -1), (0.7, -1)),
             line((0.7, -1), (0.2, 1))],
            [arc(0, -0.6, 0.8, 0.4, 200, 340),
             line((0.75, -0.75), (-0.1, 1))],
            [line((-0.8, -1), (0.8, -1)),
             line((0.8, -1), (-0.15, 1)),
             line((-0.2, 0.05), (0.6, 0.05))]],
        8: [[fig8(0.65)],
            [fig8(0.5)],
            [arc(0, -0.5, 0.6, 0.5, 0, 360),
             arc(0, 0.5, 0.75, 0.5, 0, 360)]],
        9: [[arc(0, -0.45, 0.7, 0.55, 0, 360),
             line((0.7, -0.45), (0.35, 1))],
            [arc(0, -0.5, 0.7, 0.5, 0, 360),
             line((0.7, -0.5), (0.6, 1))]],
    }

    def soft_band(z, lo, hi):
        out = np.maximum(0, np.maximum(lo - z, z - hi))
        return np.clip(1 - out / 2.0, 0, 1)

    def features(polys_xy, hw):
        # Expected 16x4x4 edge-feature profile from stroke geometry.
        # Each stroke point yields two edges at +-hw along the normal, each with
        # gradient (ink-increasing) direction pointing towards the stroke centre.
        Fd = np.zeros((16, 4, 4))
        for p in polys_xy:
            mid = 0.5 * (p[1:] + p[:-1])
            dv = p[1:] - p[:-1]
            ds = np.linalg.norm(dv, axis=1)
            ang = np.arctan2(dv[:, 1], dv[:, 0])
            nrm = np.stack([-np.sin(ang), np.cos(ang)], 1)
            for sgn in (+1.0, -1.0):
                pos = mid + sgn * hw * nrm                 # edge location
                gdir = np.arctan2(-sgn * nrm[:, 1], -sgn * nrm[:, 0])  # inward
                yA = np.stack([soft_band(pos[:, 1], 4 * i + 4, 4 * i + 11) for i in range(4)])
                xA = np.stack([soft_band(pos[:, 0], 4 * i + 4, 4 * i + 11) for i in range(4)])
                yB = np.stack([soft_band(pos[:, 1], 4 * i + 6, 4 * i + 9) for i in range(4)])
                xB = np.stack([soft_band(pos[:, 0], 4 * i + 6, 4 * i + 9) for i in range(4)])
                for c in range(8):
                    tune = np.maximum(0, np.cos(gdir - phis[c]) - 0.15) / 0.85
                    tw = ds * tune
                    Fd[c] += np.einsum('n,in,jn->ij', tw, yA, xA)
                    Fd[8 + c] += np.einsum('n,in,jn->ij', tw, yB, xB)
        return Fd.reshape(256)

    def place(polys, slant, wfac, taper, sx, sy, size):
        # shear/aspect/taper, then MNIST-like normalisation (box ~size, COM at 14,14)
        P = []
        for q in polys:
            v = q[:, 1]
            u = q[:, 0] * wfac * (1 + taper * v)
            P.append(np.stack([u - slant * v / 9.0, v], 1))
        allp = np.concatenate(P)
        lo, hi = allp.min(0), allp.max(0)
        scale = size / max(hi[0] - lo[0], hi[1] - lo[1])
        num, den = np.zeros(2), 0.0
        for q in P:
            m = 0.5 * (q[1:] + q[:-1]); w = np.linalg.norm(q[1:] - q[:-1], axis=1)
            num += (m * w[:, None]).sum(0); den += w.sum()
        com = num / den
        return [(q - com) * scale + np.array([14.0 + sx, 14.0 + sy]) for q in P]

    # ---------------- synthetic feature samples per class ----------------
    NS = 400
    X = np.zeros((10, NS, 256))
    for dgt, variants in digits.items():
        for k in range(NS):
            polys = variants[rng.randint(len(variants))]
            sl = rng.uniform(-3, 7) if dgt == 1 else rng.uniform(-2, 5)
            hw = rng.uniform(0.7, 1.8)                     # stroke half-width
            X[dgt, k] = features(place(polys,
                                       slant=sl,
                                       wfac=rng.uniform(0.6, 1.1),
                                       taper=rng.uniform(-0.2, 0.2),
                                       sx=rng.uniform(-1.2, 1.2),
                                       sy=rng.uniform(-1.2, 1.2),
                                       size=rng.uniform(16.5, 18.5)), hw)

    # ---------------- shrunk LDA with ink-amount nuisance directions ----------------
    mu = X.mean(1)
    R = (X - mu[:, None]).reshape(-1, 256)
    S = R.T @ R / R.shape[0]
    p = 256
    t = np.trace(S) / p
    gam = 0.8
    Sig = (1 - gam) * S + gam * t * np.eye(p)
    nuis = [np.ones(p), np.r_[np.ones(128), np.zeros(128)], np.r_[np.zeros(128), np.ones(128)]]
    for n in nuis:
        n = n / np.linalg.norm(n)
        Sig += 1000.0 * t * np.outer(n, n)

    mbar = mu.mean(0)
    W = np.linalg.solve(Sig, (mu - mbar).T).T
    W /= np.linalg.norm(W, axis=1, keepdims=True) + 1e-8
    alpha = 2.5
    wfc = (alpha * W).astype(np.float32)
    bfc = np.zeros(10, np.float32)       # reset: recalibrate next step

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1,
        "conv2.weight": w2,
        "conv2.bias": b2,
        "fc.weight": wfc,
        "fc.bias": bfc,
    }
```
