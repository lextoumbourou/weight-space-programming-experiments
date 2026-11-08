## Step 6: probe feature x5

**What step 5 showed.** x4 is strongly negative: higher x4 means less likely class 1.
- The loss rose by about 0.11 above the 0.665 baseline.
- That rise is far more than the roughly 0.03 a useless weight of this size would add, which puts x4's correlation with the label at about −0.33.
- No row was predicted class 1, so x4's largest value is below about 1. That again points to a binary indicator held by roughly half the rows.

**This step.** Same single-feature probe on x5 at +0.5.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[5] = 0.5          # probing feature x5 alone this step

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
