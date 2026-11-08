## Step 5: probe feature x4

**What step 4 showed.** x3 is weakly negative.
- The loss rose to 0.705, about 0.04 above the 0.665 baseline.
- Part of that rise is the penalty any weight of this size adds. Without it, the correlation is only slightly negative, roughly −0.05.
- The rows with a high x3 (above about 1) are much less often class 1: 9 of 42, or 21%, against 38% overall. So x3 looks skewed, with a long tail that is linked to class 0.
- I note this as a candidate for a nonlinear hidden unit later.

**This step.** Same single-feature probe on x4 at +0.5.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[4] = 0.5          # probing feature x4 alone this step

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
