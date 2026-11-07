## Step 4

Step 3 made it worse (21%) and swung back to **everything → "1"**. Diagnosis: all three feature maps are center-heavy and smooth for every (centred) digit, so the unit-norm template that concentrates its weight in the center — "1" — wins generically. Normalisation alone didn't remove the *common* center-heavy component shared by all digits.

Fix this step: build **discriminative** templates by subtracting the across-digit mean template, so each digit's template captures only how it *differs* from a typical digit (this automatically kills the center-dominance and the "1" magnet, since "1" becomes strongly negative in the periphery). I also go back to the step-2 idea that actually worked best (29%): keep ink as a **spatial** template but make vertical/horizontal just **scalar** preferences (uniform over position), which were more stable than spatial orientation maps.

```python
import numpy as np

def build_weights():
    w = {}

    # ---------------- conv1: ink + vertical + horizontal detectors ----------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, :, :] = 1.0 / 25.0                          # ch0 ink
    vprof = np.array([-1, -1, 4, -1, -1], dtype=np.float32)
    for r in range(5):
        conv1_w[1, 0, r, :] = vprof / 25.0                    # ch1 vertical stroke
    hprof = np.array([-1, -1, 4, -1, -1], dtype=np.float32)
    for c in range(5):
        conv1_w[2, 0, :, c] = hprof / 25.0                    # ch2 horizontal stroke
    conv1_b = np.zeros(8, dtype=np.float32)
    w['conv1.weight'] = conv1_w
    w['conv1.bias'] = conv1_b

    # ---------------- conv2: pass the 3 feature maps through averaging ----------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_w[0, 0, :, :] = 1.0 / 25.0   # ink   -> conv2 ch0
    conv2_w[1, 1, :, :] = 1.0 / 25.0   # vert  -> conv2 ch1
    conv2_w[2, 2, :, :] = 1.0 / 25.0   # horiz -> conv2 ch2
    conv2_b = np.zeros(16, dtype=np.float32)
    w['conv2.weight'] = conv2_w
    w['conv2.bias'] = conv2_b

    # ---------------- spatial ink templates (where ink is expected) ----------------
    INK = {
        0: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
        1: [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]],
        2: [[1,1,1,1],[0,0,1,1],[0,1,1,0],[1,1,1,1]],
        3: [[1,1,1,1],[0,0,1,1],[0,0,1,1],[1,1,1,1]],
        4: [[1,0,0,1],[1,0,0,1],[1,1,1,1],[0,0,0,1]],
        5: [[1,1,1,1],[1,1,0,0],[0,0,1,1],[1,1,1,0]],
        6: [[0,1,1,1],[1,0,0,0],[1,1,1,1],[1,1,1,1]],
        7: [[1,1,1,1],[0,0,1,1],[0,1,1,0],[0,1,0,0]],
        8: [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,0,1]],
        9: [[1,1,1,1],[1,0,0,1],[1,1,1,1],[0,0,0,1]],
    }
    # scalar orientation preference per digit (relative vert / horiz content)
    vtot = {0:0.4, 1:1.0, 2:0.1, 3:0.3, 4:0.8, 5:0.3, 6:0.5, 7:0.1, 8:0.6, 9:0.6}
    htot = {0:0.5, 1:0.0, 2:0.8, 3:0.8, 4:0.4, 5:0.8, 6:0.5, 7:0.7, 8:0.8, 9:0.6}

    # ---- make ink templates discriminative: subtract across-digit mean, then L2 norm ----
    ink_arr = np.stack([np.array(INK[d], dtype=np.float32) for d in range(10)])
    ink_mean = ink_arr.mean(axis=0)                 # the "typical digit" ink pattern
    ink_disc = ink_arr - ink_mean[None]             # deviation from typical
    for d in range(10):
        n = np.linalg.norm(ink_disc[d])
        if n > 1e-6:
            ink_disc[d] /= n

    # center the scalar orientation preferences across digits
    vmean = np.mean(list(vtot.values()))
    hmean = np.mean(list(htot.values()))

    Gi, Gv, Gh = 12.0, 6.0, 6.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    for d in range(10):
        t = ink_disc[d]
        for r in range(4):
            for c in range(4):
                pos = r * 4 + c
                fc_w[d, 0 * 16 + pos] = Gi * t[r, c]                 # discriminative ink
                fc_w[d, 1 * 16 + pos] = Gv * (vtot[d] - vmean) / 16  # vertical pref
                fc_w[d, 2 * 16 + pos] = Gh * (htot[d] - hmean) / 16  # horizontal pref

    w['fc.weight'] = fc_w
    w['fc.bias'] = fc_b
    return w
```
