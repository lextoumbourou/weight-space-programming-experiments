## Step 6: add loop and arc part-detectors in conv2

**What I'm trying.** Steps 4 and 5 show that tuning α only trades classes against each other:

- α = 0.6 rescued 7 (179→708 correct) and helped 2 and 3;
- but it killed 8 (never predicted) and hurt 0, 4, 6 and 9.

Plain orientation templates seem to top out around 60%. They don't capture the *shape* facts that separate the confused pairs: closed loops versus open arcs, and where each one sits.

So I'm turning the unused conv2 channels into hand-built **part detectors** on the 12×12 orientation maps. Each 5×5 kernel spans about 8 input pixels between its outer taps.

- **ch5, loop detector.** It looks for a ring of strokes of radius about 2 pooled cells (≈4 px). At every ring position it expects the orientation tangent to the circle, and it penalises ink at the centre (the hole). This should fire for the loops of 6, 8 and 9 and for small 0s.
- **ch6–9, arc detectors.** These are the same ring restricted to one closed side, with negative weight for strokes on the open side:
  - ch6 is ⊃ (closed on the right, as in 3's bumps and 5's belly);
  - ch7 is ⊂ (closed on the left);
  - ch8 is ∩ (closed on top, as in the tops of 0 and 2);
  - ch9 is ∪ (closed at the bottom, as in the bottom of 0 and the open-top 4).
- **Biases.** Each part detector has a negative bias, so it only fires when most of the ring is present.

**fc.** It has two parts:

- **Orientation templates (ch0–4).** These keep the nearest-centroid rule, with α set to 0.5, between the step 4 and step 5 values.
- **Part channels (ch5–9).** For each digit I list by hand which parts appear and where, for example "9: loop centred near (x=14, y=9.5)" and "3: two ⊃ arcs". These become location templates on the 4×4 grid, again with a nearest-centroid bias.

```python
import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')   # V = row offset (down), U = col offset (right)

    # ================= conv1: oriented line detectors + intensity =================
    W1 = np.zeros((8, 1, 5, 5)); b1 = np.zeros(8)
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)
        perp = -U * math.sin(th) + V * math.cos(th)
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = K
        b1[k] = -0.05
    G = np.exp(-(U**2 + V**2) / 2.0); G /= G.sum()
    W1[4, 0] = G                      # channel 4: local ink density
    # channels 5-7 unused

    # ================= conv2 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)
    # ch0-4: blurred pass-through of orientation / intensity maps
    G2 = np.exp(-(U**2 + V**2) / 2.0); G2 /= G2.sum()
    for c in range(5):
        W2[c, c] = G2

    # part detectors on the pooled orientation maps
    rho = np.sqrt(U**2 + V**2)
    phi = np.arctan2(V, U)            # angle of kernel position around centre (row down)
    tang = phi + math.pi / 2          # tangent direction of a circle at that position
    ring = np.exp(-(rho - 2.0)**2 / (2 * 0.6**2)); ring[2, 2] = 0.0
    hole = -0.5 * np.exp(-rho**2 / (2 * 0.7**2))   # penalise ink at the centre

    def part_kernel(gate):
        Wk = np.zeros((8, 5, 5))
        for k, th in enumerate(thetas):
            Wk[k] = ring * np.cos(tang - th)**4 * gate
        pos = Wk[:4][Wk[:4] > 0].sum()
        Wk[:4] *= 1.5 / pos
        Wk[4] = hole
        return Wk

    W2[5] = part_kernel(np.ones((5, 5))); b2[5] = -0.30          # loop
    def arc_gate(phic):
        cs = np.cos(phi - phic)
        return np.maximum(0, cs) - 0.6 * np.maximum(0, -cs)**2
    W2[6] = part_kernel(arc_gate(0.0));          b2[6] = -0.25   # closed right  (⊃)
    W2[7] = part_kernel(arc_gate(math.pi));      b2[7] = -0.25   # closed left   (⊂)
    W2[8] = part_kernel(arc_gate(-math.pi / 2)); b2[8] = -0.25   # closed top    (∩)
    W2[9] = part_kernel(arc_gate(math.pi / 2));  b2[9] = -0.25   # closed bottom (∪)
    # ch10-15 unused

    # ================= stroke descriptions (x=col, y=row) =================
    def seg(p0, p1, w=1.0):
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(L / 0.5))
        t = (np.arange(n) + 0.5) / n
        return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t,
                np.full(n, math.atan2(y1 - y0, x1 - x0)), np.full(n, w * L / n))

    def arc(cx, cy, rx, ry, t0, t1, w=1.0):
        t0r, t1r = math.radians(t0), math.radians(t1)
        n = max(8, int(abs(t1 - t0) / 3))
        t = t0r + (t1r - t0r) * (np.arange(n) + 0.5) / n
        dt = abs(t1r - t0r) / n
        dx = -rx * np.sin(t); dy = ry * np.cos(t)
        return (cx + rx * np.cos(t), cy + ry * np.sin(t),
                np.arctan2(dy, dx), w * np.hypot(dx, dy) * dt)

    digits = {
        0: [arc(14, 14, 5.5, 8.5, 0, 360)],
        1: [seg((15, 4.5), (13, 23.5), 0.6), seg((17.5, 5), (10.5, 23), 0.6)],
        2: [arc(14, 10, 5, 5, 180, 390), seg((18.3, 12.5), (9, 22.5)), seg((9, 22.5), (20, 22.5))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [seg((10, 4.5), (8, 16)), seg((8, 16), (20, 16)), seg((17, 5), (17, 23.5))],
        5: [seg((10, 5), (19, 5)), seg((10, 5), (9.5, 13)), arc(13.5, 17.5, 5.5, 5, 228, 510)],
        6: [seg((17, 4.5), (10.5, 12)), seg((10.5, 12), (8.5, 18)), arc(13.5, 18, 5, 4.5, 0, 360)],
        7: [seg((8, 5), (20, 5)), seg((20, 5), (12, 23.5))],
        8: [arc(14, 9, 4, 4.5, 0, 360), arc(14, 18.5, 5, 4.5, 0, 360)],
        9: [arc(14, 9.5, 5, 4.5, 0, 360), seg((19, 10), (16, 23.5))],
    }

    # hand-listed parts per digit: (channel, x, y, strength)
    LOOP, CR, CL, CT, CB = 5, 6, 7, 8, 9
    parts = {
        0: [(CT, 14, 8.5, 1.0), (CB, 14, 19.5, 1.0), (CL, 11, 14, 0.5), (CR, 17, 14, 0.5), (LOOP, 14, 14, 0.3)],
        1: [],
        2: [(CT, 14, 9, 1.0), (CR, 15, 10, 0.7)],
        3: [(CR, 13, 9, 1.0), (CR, 13, 18.5, 1.0)],
        4: [(CB, 13, 11, 0.8)],
        5: [(CR, 13.5, 17.5, 1.0)],
        6: [(LOOP, 13.5, 18, 1.0)],
        7: [],
        8: [(LOOP, 14, 9, 1.0), (LOOP, 14, 18.5, 1.0)],
        9: [(LOOP, 14, 9.5, 1.0)],
    }

    centers = [4 * i + 7.5 for i in range(4)]   # input-pixel centre of each final 4x4 cell

    # ---- orientation templates (channels 0-4) ----
    T = np.zeros((10, 16, 4, 4))
    sigma = 3.0
    for d, strokes in digits.items():
        x = np.concatenate([s[0] for s in strokes]); y = np.concatenate([s[1] for s in strokes])
        a = np.concatenate([s[2] for s in strokes]); ds = np.concatenate([s[3] for s in strokes])
        for r in range(4):
            for c in range(4):
                prox = np.exp(-((x - centers[c])**2 + (y - centers[r])**2) / (2 * sigma**2)) * ds
                for k, th in enumerate(thetas):
                    T[d, k, r, c] = 1 - math.exp(-np.sum(prox * np.cos(a - th)**4) / 3.0)
                T[d, 4, r, c] = 0.5 * (1 - math.exp(-np.sum(prox) / 3.0))

    # ---- part templates (channels 5-9) ----
    P = np.zeros((10, 16, 4, 4))
    sp = 2.5
    for d, plist in parts.items():
        for (ch, px, py, w) in plist:
            for r in range(4):
                for c in range(4):
                    P[d, ch, r, c] += w * math.exp(-((px - centers[c])**2 + (py - centers[r])**2) / (2 * sp**2))
    P = np.minimum(P, 1.0)

    Tf = T.reshape(10, 256); Pf = P.reshape(10, 256)

    # ---- nearest-centroid logits for both feature groups ----
    alpha, s = 0.5, 9.0          # orientation features
    alpha_p, s_p = 0.3, 8.0      # part features
    Wfc = s * alpha * Tf + s_p * Pf
    bfc = -0.5 * s * alpha**2 * np.sum(Tf**2, axis=1) - 0.5 * s_p * alpha_p * np.sum(Pf**2, axis=1)

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
