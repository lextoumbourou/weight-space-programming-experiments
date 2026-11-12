## Step 15: probe the strict loop detector

**What I'm trying.** Step 14 is the best so far: 71.4% accuracy, loss 0.912. Gains from tweaking templates are now small, about 1% per step.

I want to know whether the strict four-sided loop detector from step 11 actually works before building more on that design. It might fire selectively on 0, 6, 8 and 9, it might almost never fire, or it might still fire on everything.

**This step is a measurement, not a model**, like step 10. conv1 and conv2 are identical to step 14. fc encodes two scalars on a 3×3 grid:

- S1 = total strict-loop activity in the top half (rows 0–1);
- S2 = total strict-loop activity in the bottom half (rows 2–3);
- the bins are < 0.15, 0.15–0.7 and > 0.7.

The logits are logit_(3i+j) = M·(u_i·S1 + v_j·S2 − (u_i² + v_j²)/2), with u = v = (0, 0.3, 1.1).

- The argmax is the nearest lattice point, so predicted class 3i + j means S1 is in bin i and S2 is in bin j.
- Class 9 is disabled.

**How I'll use the result.**

- If loops show up for 9 at the top, 6 at the bottom and 8 in both, I'll increase the loop feature's weight and replace the open-arc features with corner and junction detectors built the same way. Examples are ┌ for 5, ┐ for 7 and └ for 4.
- If the detector rarely fires, I'll lower its threshold.

```python
import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')
    HOR, DIAG1, VER, DIAG2 = 0, 1, 2, 3

    # ================= conv1: identical to step 14 =================
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

    # ================= conv2: identical to step 14 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)

    def set_pair(m, Z, g, t):
        for k in range(4):
            W2[2 * m, k] = g * Z[k];      W2[2 * m, k + 4] = -g * Z[k]
            W2[2 * m + 1, k] = g * Z[k];  W2[2 * m + 1, k + 4] = -g * Z[k]
        b2[2 * m] = -g * t
        b2[2 * m + 1] = -g * t - 1.0

    nb = np.zeros((5, 5))
    nb[1:4, 1:4] = [[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]]
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k] = nb
        set_pair(k, Z, 1.0, 0.6)

    def side(Z, name, w):
        if name == 'top':    Z[HOR, 0, 2] += w
        if name == 'bottom': Z[HOR, 4, 2] += w
        if name == 'left':   Z[VER, 2, 0] += w
        if name == 'right':  Z[VER, 2, 4] += w

    def centre_pen(Z, w=0.5):
        for k in range(4):
            Z[k, 2, 2] -= w

    Z = np.zeros((4, 5, 5))
    for s_ in ['top', 'bottom', 'left', 'right']:
        side(Z, s_, 1.0)
    centre_pen(Z)
    set_pair(4, Z, 2.5, 3.0)                                   # strict loop

    def arc3(present, absent_cells):
        Z = np.zeros((4, 5, 5))
        for s_ in present:
            side(Z, s_, 1.0)
        k, cells = absent_cells
        for (a, b) in cells:
            Z[k, a, b] -= 1.2
        centre_pen(Z)
        return Z

    set_pair(5, arc3(['top', 'right', 'bottom'], (VER, [(2, 0), (2, 1)])), 2.5, 2.2)
    set_pair(6, arc3(['top', 'left', 'right'], (HOR, [(4, 2), (3, 2)])), 2.5, 2.2)
    set_pair(7, arc3(['bottom', 'left', 'right'], (HOR, [(0, 2), (1, 2)])), 2.5, 2.2)

    # ================= fc: PROBE of strict loop feature (m=4 -> channels 8, 9) =================
    A_top = np.zeros((16, 4, 4)); A_top[8, 0:2, :] = 1.0; A_top[9, 0:2, :] = -1.0
    A_bot = np.zeros((16, 4, 4)); A_bot[8, 2:4, :] = 1.0; A_bot[9, 2:4, :] = -1.0
    A_top = A_top.reshape(256); A_bot = A_bot.reshape(256)
    lev = [0.0, 0.3, 1.1]       # bin boundaries at 0.15 and 0.7
    M = 60.0
    Wfc = np.zeros((10, 256)); bfc = np.zeros(10)
    for i in range(3):          # top-half bin
        for j in range(3):      # bottom-half bin
            cls = 3 * i + j
            Wfc[cls] = M * (lev[i] * A_top + lev[j] * A_bot)
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
