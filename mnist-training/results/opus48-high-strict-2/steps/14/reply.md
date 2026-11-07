## Step 14

Step 13 regressed to 43.4%: lowering b3 killed class 3, raising b5 turned 5 into a magnet, and the new hollow "8" template didn't help (8 still ~0). So I revert the "8" template to all-ones and go back to the **step-12 configuration (45.0%, best loss)**, making only two tiny, targeted moves: lower b4 a touch (it absorbs true 6, 7, 9) and raise b9 a touch (true 9 was draining into 4). Everything else stays at the step-12 values that produced the best loss, so I keep this near my best while testing one more small rebalance before the final step.

```python
import numpy as np

def build_weights():
    w = {}

    # ---------------- conv1 ----------------
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

    # ---------------- conv2 ----------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_w[0, 0, :, :] = 1.0 / 25.0   # ink
    conv2_w[1, 1, :, :] = 1.0 / 25.0   # vert
    conv2_w[2, 2, :, :] = 1.0 / 25.0   # horiz
    conv2_b = np.zeros(16, dtype=np.float32)
    w['conv2.weight'] = conv2_w
    w['conv2.bias'] = conv2_b

    # ---------------- fc: step-12 templates (8 back to all-ones) + tiny tweaks ----------------
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

    # step-12 biases with small moves: 4 down, 9 up
    bias = {0:+0.3, 1:-0.1, 2:+0.3, 3:+0.3, 4:0.0, 5:-0.05, 6:-0.05, 7:+0.25, 8:-0.05, 9:+0.15}

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
