## Step 2: probe feature x1

**Step 1 result.** All 600 rows were predicted class 0, giving a 370/230 split. So the class-1 rate is 230/600 = 0.383, and the baseline loss is about 0.666.

**What x0 shows.**
- With the probe, the loss rose to 0.7254, so ΔL ≈ +0.059.
- That gives r ≈ (0.03 − 0.059)/0.243 ≈ −0.12. x0 is weakly negative for class 1.
- No row was predicted class 1, so x0 never went above about 0.94. That suggests x0 is left-skewed, possibly a common binary flag.

**This step.** Same probe on x1.

```python
import numpy as np
import math

def build_weights():
    PROBE = 1        # feature being probed this step
    W = 0.5          # probe weight on class-1 logit
    PRIOR = math.log(230 / 370)  # log-odds of class 1 (~ -0.475)

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(x_p), hidden 1 = relu(-x_p); h0 - h1 = x_p
    fc1_w[0, PROBE] = 1.0
    fc1_w[1, PROBE] = -1.0

    # class-1 logit = PRIOR + W * x_p ; class-0 logit = 0
    fc2_w[1, 0] = W
    fc2_w[1, 1] = -W
    fc2_b[1] = PRIOR

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
