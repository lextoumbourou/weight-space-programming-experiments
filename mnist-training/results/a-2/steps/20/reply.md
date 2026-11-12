## Step 20: probe the endpoint detectors before relying on them

**What I'm trying.** Adding endpoint detectors in step 19 hurt: accuracy fell to 62.6%. The damage pattern is telling:

- 9→4 jumped to 480 and 6→4 to 300;
- 3 is now over-predicted, absorbing 5s (217) and 8s (255).

4's template lists many endpoints: two top ends, a bottom end and a right end. So whenever the endpoint detectors fire somewhere near those places, 4 gains evidence. Most likely the detectors fire far more often than I assumed, on curves, junctions and stroke edges, and not only on real stroke ends. The unclipped single-channel values may also exceed 1.

Rather than guess again, I'll measure them, as I did for the loop detector in step 15. conv1 and conv2 are exactly as in step 19. fc encodes two scalars on a 3×3 grid:

- S1 = total E_down activity (top endpoints) in the top half, rows 0–1. I expect it to be high for 1, 4 and 6.
- S2 = total E_up activity (bottom endpoints) in the bottom half, rows 2–3. I expect it to be high for 1, 4, 7 and 9.
- The bins are < 0.3, 0.3–1.5 and > 1.5.

The logits are logit_(3i+j) = M·(u_i·S1 + v_j·S2 − (u_i² + v_j²)/2), with u = v = (0, 0.6, 2.4).

- Predicted class 3i + j means S1 is in bin i and S2 is in bin j.
- Class 9 is disabled.

From the rows I can tell whether the endpoint detectors are selective, and recalibrate their thresholds and templates, or drop them.

```python
import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')
    HOR, D1, VER, D2 = 0, 1, 2, 3

    # ================= conv1: identical to step 19 =================
    W1 = np.zeros((8, 1, 5, 5)); b1 = np.zeros(8)
    g1 = 3.0
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)
        perp = -U * math.sin(th) + V * math.cos(th)
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = g1 * K;     b1[k] = -0.6
        W1[k + 4, 0] = g1 * K; b1[k + 4] = -1.6

    # ================= conv2: identical to step 19 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)

    def put(ch, Z, g):
        for k in range(4):
            W2[ch, k] += g * Z[k]
            W2[ch, k + 4] -= g * Z[k]

    def set_pair(m, Z, g, t):
        put(2 * m, Z, g);     b2[2 * m] = -g * t
        put(2 * m + 1, Z, g); b2[2 * m + 1] = -g * t - 1.0

    def set_single(ch, Z, g, t):
        put(ch, Z, g); b2[ch] = -g * t

    nb = np.zeros((5, 5))
    nb[1:4, 1:4] = [[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]]
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k] = nb
        set_pair(k, Z, 1.0, 0.6)

    Z = np.zeros((4, 5, 5))
    Z[HOR, 0, 2] = 1; Z[HOR, 4, 2] = 1; Z[VER, 2, 0] = 1; Z[VER, 2, 4] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_single(8, Z, 2.0, 3.0)

    Z = np.zeros((4, 5, 5))
    Z[D2, 1, 1] = 1; Z[D1, 1, 3] = 1; Z[D1, 3, 1] = 1; Z[D2, 3, 3] = 1
    for k in range(4):
        Z[k, 2, 2] -= 0.5
    set_single(9, Z, 2.0, 3.0)

    Edown = np.zeros((5, 5))
    Edown[2, 2] = 0.4; Edown[3, 2] = 0.4; Edown[3, 1] = 0.2; Edown[3, 3] = 0.2; Edown[4, 2] = 0.2
    Edown[1, 1] = -0.6; Edown[1, 2] = -0.6; Edown[1, 3] = -0.6; Edown[0, 2] = -0.2
    Edown[2, 1] = -0.3; Edown[2, 3] = -0.3
    Eup = np.flipud(Edown)
    Eright = Edown.T.copy()
    Eleft = np.fliplr(Eright)
    for ch, Emap in zip([10, 11, 12, 13], [Edown, Eup, Eright, Eleft]):
        Z = np.stack([Emap] * 4)
        set_single(ch, Z, 1.5, 1.1)

    # ================= fc: PROBE  S1 = E_down (ch10) in top half, S2 = E_up (ch11) in bottom half
    A1 = np.zeros((16, 4, 4)); A1[10, 0:2, :] = 1.0
    A2 = np.zeros((16, 4, 4)); A2[11, 2:4, :] = 1.0
    A1 = A1.reshape(256); A2 = A2.reshape(256)
    lev = [0.0, 0.6, 2.4]       # bin boundaries at 0.3 and 1.5
    M = 30.0
    Wfc = np.zeros((10, 256)); bfc = np.zeros(10)
    for i in range(3):
        for j in range(3):
            cls = 3 * i + j
            Wfc[cls] = M * (lev[i] * A1 + lev[j] * A2)
            bfc[cls] = -M * 0.5 * (lev[i]**2 + lev[j]**2)
    bfc[9] = -1e4

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
