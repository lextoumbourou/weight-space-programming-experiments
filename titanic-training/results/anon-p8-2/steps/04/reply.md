## Step 4: probe feature x3

**What x2 shows.**
- The loss fell slightly to 0.6569, so ΔL ≈ −0.009. That gives r ≈ +0.16, weakly positive for class 1.
- 107 rows (about 18%) were pushed past the threshold.
- 59 of those 107 (55%) were truly class 1.

So x2 looks like an indicator for a smaller subgroup with a moderately raised class-1 rate.

**This step.** Same probe on x3.

```python
import numpy as np
import math

def build_weights():
    PROBE = 3        # feature being probed this step
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
