## Step 21: test a larger scale for the improved linear direction

**What step 20 showed.** Re-weighting by covariance gave a clear gain: loss 0.493 (down from 0.513) and accuracy 0.767.

**What I'm doing now.** The earlier scale test found an optimum near 1.1, but that was for equal weights, which were partly wrong. Some of the weight was "wasted" on noise, which keeps the best scale small. With a better direction, the best scale is likely larger. So I multiply the whole linear direction by 1.2 and keep 0.4·|x7| unchanged.

**How to read the result.** If the loss falls below 0.493, I'll push the scale further. If it rises, I'll go back to about 1.0.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear part (units 0,1): logit1 += scale * w.x ----
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.68    # x1
    w[2] = 0.10    # x2 (weak)
    w[4] = -0.60   # x4
    w[5] = 0.10    # x5 (weak)
    w[6] = -0.34   # x6
    w[7] = 0.78    # x7 (strongest)
    w[9] = -0.67   # x9
    w[11] = 0.21   # x11
    scale = 1.2
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = scale
    W2[1, 1] = -scale

    # ---- Kept: |x7| term (units 2,3): logit1 += 0.4*(|x7| - 0.798) ----
    W1[2, 7] = 1.0
    W1[3, 7] = -1.0
    W2[1, 2] = 0.4
    W2[1, 3] = 0.4
    b2[1] -= 0.4 * 0.798

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
