## Step 1

My plan: turn the fixed network into a **coarse ink-density template matcher**.

- **conv1**: only channel 0 is active, a 5×5 averaging filter that measures local ink. The other 7 channels are zero.
- **conv2**: all 16 output channels read channel 0 with a 5×5 averaging filter, so after the second pool each channel carries the same 4×4 ink-density map `M` of the digit (16 copies for gain).
- **fc**: for each digit `d` I write a hand-drawn 4×4 ink template, mean-subtract it (so overall ink amount doesn't bias the logits), and spread it across the 16 identical channels. The logit for `d` is then `G · correlation(template_d, M)`.

The receptive fields overlap heavily, so `M` is very blurred — I expect only modest accuracy, but the confusion matrix will tell me which templates to fix next.

```python
import numpy as np

def build_weights():
    w = {}

    # ---- conv1: channel 0 = 5x5 ink-averaging filter; others zero ----
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, :, :] = 1.0 / 25.0          # local mean ink
    conv1_b = np.zeros(8, dtype=np.float32)
    w['conv1.weight'] = conv1_w
    w['conv1.bias'] = conv1_b

    # ---- conv2: every output channel averages ink from channel 0 ----
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(16):
        conv2_w[k, 0, :, :] = 1.0 / 25.0      # 16 identical ink-density maps
    conv2_b = np.zeros(16, dtype=np.float32)
    w['conv2.weight'] = conv2_w
    w['conv2.bias'] = conv2_b

    # ---- fc: hand-drawn 4x4 ink templates, matched against the map ----
    # rows: 0=top .. 3=bottom ; cols: 0=left .. 3=right
    T = {
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

    G = 20.0  # overall gain so logits have a usable spread
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    for d in range(10):
        t = np.array(T[d], dtype=np.float32)
        t = t - t.mean()                      # cancel overall-ink bias
        for k in range(16):                   # same template across 16 channels
            for r in range(4):
                for c in range(4):
                    fc_w[d, k * 16 + r * 4 + c] = G * t[r, c] / 16.0

    w['fc.weight'] = fc_w
    w['fc.bias'] = fc_b
    return w
```
