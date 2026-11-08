## Step 26: tune x9's linear weight

**Steps 23–25 result.** The extra low-tail units never changed anything, so x7, x8, x11 and x12 have no rows below −1.5. Most features here look binary, or are counts bounded near their low end. I'm dropping the search for a hidden tail effect.

**Back to the linear weights.** The current best is 0.4584. I'll spend the remaining steps tuning the linear coefficients one at a time, starting with the next-strongest features.

**This step.** I'm raising x9 from 0.20 to 0.45. In its probe, x9 was as strong as x1 and x5 (r ≈ +0.32), but it may be under-weighted in the joint model.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20
    coef[4]  = -0.40
    coef[1]  = 0.30
    coef[9]  = 0.45   # testing larger (was 0.20)
    coef[5]  = 0.15
    coef[2]  = 0.10
    coef[0]  = -0.10
    coef[3]  = -0.20
    coef[6]  = 0.05
    BIAS = -0.68

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)

    # hidden 0/1: linear pass-through of z = coef . x
    fc1_w[0] = coef
    fc1_w[1] = -coef
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0

    # hidden 2: AND(x10 high, x4 high) -> lowers class-1 logit
    fc1_w[2, 10] = 1.0
    fc1_w[2, 4] = 1.0
    fc1_b[2] = -1.5
    fc2_w[1, 2] = -0.5

    # hidden 3: AND(x10 high, x4 low) -> raises class-1 logit
    fc1_w[3, 10] = 1.0
    fc1_w[3, 4] = -1.0
    fc1_b[3] = -1.0
    fc2_w[1, 3] = 0.9

    fc2_b[1] = BIAS

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
