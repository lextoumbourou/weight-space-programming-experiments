## Step 8

Every "principled" normalisation keeps producing a magnet (1 again this time, driven partly by my large `vtot[1]=1.0`, since the vertical detector fires on the central ink of *every* digit). I've now spent several steps confirming that **step 2 (29%) is a stable local optimum** and the signal spread between classes is only ~1 logit (from step 5).

So: revert exactly to step 2, and apply the **gentle bias rebalance** I couldn't do safely before (now sized ~±0.3, not ±1.2). Step 2's errors were dominated by two magnets — **5** (absorbs true 3,7,8,9) and **6** (absorbs true 0,2) — while 0,2,7 were never predicted. I lower 5 and 6, raise 0,2,3,7,8,9.

```python
import numpy as np

def build_weights():
    w = {}

    # ---------------- conv1: ink + vertical + horizontal detectors (step 2) ----------------
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

    # ---------------- fc: exact step-2 templates + gentle bias rebalance ----------------
    Tink = {
        0: [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
        1: [[0,0,1,0],[0,1,1,0],[0,1,1,0],[0,0,1,0]],
        2: [[1,1,1,1],[0,0,0,1],[0,1,1,0],[1,1,1,1]],
        3: [[1,1,1,1],[0,0,1,1],[0,0,1,1],[1,1,1,1]],
        4: [[1,0,0,1],[1,0,0,1],[1,1,1,1],[0,0,0,1]],
        5: [[1,1,1,1],[1,1,1,0],[0,0,1,1],[1,1,1,0]],
        6: [[0,1,1,0],[1,0,0,0],[1,1,1,0],[1,1,1,1]],
        7: [[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,1,0,0]],
        8: [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]],
        9: [[1,1,1,1],[1,0,0,1],[1,1,1,1],[0,0,0,1]],
    }
    vtot = {0:0.3, 1:1.0, 2:-0.2, 3:-0.3, 4:0.7, 5:0.2, 6:0.5, 7:-0.2, 8:0.4, 9:0.5}
    htot = {0:0.3, 1:-0.8, 2:0.6, 3:0.7, 4:0.2, 5:0.6, 6:0.3, 7:0.6, 8:0.4, 9:0.3}

    # gentle rebalance: push down the magnets (5,6), lift the never-chosen (0,2,7) etc.
    bias = {0:+0.3, 1:-0.1, 2:+0.3, 3:+0.2, 4:0.0, 5:-0.4, 6:-0.2, 7:+0.3, 8:+0.15, 9:+0.1}

    Gi, Gv, Gh = 8.0, 6.0, 6.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    for d in range(10):
        t = np.array(Tink[d], dtype=np.float32)
        t = t - t.mean()
        for r in range(4):
            for c in range(4):
                pos = r * 4 + c
                fc_w[d, 0 * 16 + pos] = Gi * t[r, c] / 16.0
                fc_w[d, 1 * 16 + pos] = Gv * vtot[d] / 16.0
                fc_w[d, 2 * 16 + pos] = Gh * htot[d] / 16.0
        fc_b[d] = bias[d]

    w['fc.weight'] = fc_w
    w['fc.bias'] = fc_b
    return w
```
