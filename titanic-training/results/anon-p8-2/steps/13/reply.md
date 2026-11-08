## Step 13: probe feature x12, the last one

**What x11 shows.**
- The loss rose to 0.6802, so ΔL ≈ +0.014. That gives r ≈ +0.06, weak.
- 55 rows were pushed past the threshold, and 25 of them (45%) were class 1, close to the base rate.

**Summary so far.**

| Feature | Estimated r | Strength |
|---|---|---|
| x10 | +0.5 | strongest |
| x4 | −0.33 | strong |
| x5 | +0.33 | strong |
| x9 | +0.32 | strong |
| x1 | +0.31 | strong |
| x2 | +0.16 | weak |
| x0 | −0.12 | weak |
| x6 | +0.10 | weak |
| x7 | +0.08 | weak |
| x11 | +0.06 | weak |
| x3 | −0.04 | negligible |
| x8 | −0.02 | negligible |

**This step.** Same probe on x12.

```python
import numpy as np
import math

def build_weights():
    PROBE = 12       # feature being probed this step
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
