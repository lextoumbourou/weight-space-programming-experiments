## Step 8: probe feature x7

**What step 7 showed.** x6 is weakly positive (higher x6 means more likely class 1).
- The loss rose only 0.007 above the 0.665 baseline. That is less than the roughly 0.03 a feature with no signal would add at weight 0.5, so its correlation is about +0.1.
- No row was predicted class 1, so x6's largest value is below about 1. Like x0 and x4, it looks like a binary indicator that most rows have.

**This step.** Same single-feature probe on x7, at weight +0.5.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[7] = 0.5          # probing feature x7 alone this step

    # Bias = log prior odds of class 1 (230/600 positives)
    b = math.log(230.0 / 370.0)

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = h0 - h1 + b = w.x + b ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
