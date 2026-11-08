## Step 5: probe feature x4

**What x3 shows.**
- The loss rose to 0.7052, so ΔL ≈ +0.039. That gives r ≈ −0.04, close to zero.
- Only 42 rows (7%) were pushed past the threshold, and just 9 of them (21%) were class 1.

So x3 looks like a heavy-tailed count. Its large values are mildly bad for class 1, but it is weak overall. It might be worth a nonlinear treatment later.

**This step.** Same probe on x4.

```python
import numpy as np
import math

def build_weights():
    PROBE = 4        # feature being probed this step
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
