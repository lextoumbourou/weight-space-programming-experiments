## Step 6

Critical lesson from step 5: biases of ±1.2 completely swamped everything (only 2 and 7 got predicted), which means **the template-driven logit differences are only ~order 1** — the features barely separate classes. So biases must be tiny, and the real fix is stronger *discrimination*.

Root cause across all steps: with raw templates, dense digits (5,6,8) win; with full normalisation, the center-heavy "1" wins. The center cells are non-discriminative (every centred digit fills them), so they just create a magnet. This step I **de-emphasise the center 2×2 cells** in the ink templates and then normalise, forcing discrimination to come from the *peripheral* ink structure (where digits actually differ). I keep the scalar vert/horiz preferences and set biases back to ~0.

```python
import numpy as np

def build_weights():
    w = {}

    # ---------------- conv1: ink + vertical + horizontal detectors ----------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, :, :] = 1.0 / 25.0
    vprof = np.array([-1, -1, 4, -1, -1], dtype=np.float32)
    for r in range(5):
        conv1_w[1, 0, r, :] = vprof / 25.0
    hprof = np.array([-1, -1, 4, -1, -1], dtype=np.float32)
    for c in range(5):
        conv1_w[2, 0, :, c] = hprof / 25.0
    conv1_b = np.zeros(8, dtype=np.float32)
    w['conv1.weight'] = conv1_w
    w['conv1.bias'] = conv1_b

    # ---------------- conv2: pass 3 maps through averaging ----------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_w[0, 0, :, :] = 1.0 / 25.0   # ink
    conv2_w[1, 1, :, :] = 1.0 / 25.0   # vert
    conv2_w[2, 2, :, :] = 1.0 / 25.0   # horiz
    conv2_b = np.zeros(16, dtype=np.float32)
    w['conv2.weight'] = conv2_w
    w['conv2.bias'] = conv2_b

    # ---------------- fc templates ----------------
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
    vtot = {0:0.3, 1:1.0, 2:-0.2, 3:-0.3, 4:0.7, 5:0.2, 6:0.5, 7:-0.2, 8:0.4, 9:0.5}
    htot = {0:0.3, 1:-0.8, 2:0.6, 3:0.7, 4:0.2, 5:0.6, 6:0.3, 7:0.6, 8:0.4, 9:0.3}

    # de-emphasise the non-discriminative central 2x2 cells
    cmask = np.array([[1,1,1,1],
                      [1,0.25,0.25,1],
                      [1,0.25,0.25,1],
                      [1,1,1,1]], dtype=np.float32)

    vmean = np.mean(list(vtot.values()))
    hmean = np.mean(list(htot.values()))

    Gi, Gv, Gh = 10.0, 8.0, 8.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    for d in range(10):
        t = np.array(INK[d], dtype=np.float32)
        t = (t - t.mean()) * cmask          # center-out, kill center dominance
        n = np.linalg.norm(t)
        if n > 1e-6:
            t = t / n                        # fair competition across digits
        for r in range(4):
            for c in range(4):
                pos = r * 4 + c
                fc_w[d, 0 * 16 + pos] = Gi * t[r, c]
                fc_w[d, 1 * 16 + pos] = Gv * (vtot[d] - vmean) / 16.0
                fc_w[d, 2 * 16 + pos] = Gh * (htot[d] - hmean) / 16.0
        fc_b[d] = 0.0

    w['fc.weight'] = fc_w
    w['fc.bias'] = fc_b
    return w
```
