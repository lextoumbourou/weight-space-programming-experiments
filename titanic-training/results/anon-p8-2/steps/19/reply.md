## Step 19: decrease the weight on x4

**Step 18 result.** Raising x4 to −0.8 made the loss clearly worse (0.4816 vs about 0.4697). Its best weight is probably below −0.5 in magnitude: the overlapping features (x1, x9, x5, and maybe x10) already carry much of its signal.

**This step.** I'm testing x4 at −0.25.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20   # strongest positive
    coef[4]  = -0.25  # strong negative (testing smaller)
    coef[1]  = 0.30   # positive indicator
    coef[9]  = 0.20   # positive
    coef[5]  = 0.15   # positive
    coef[2]  = 0.10   # weak positive
    coef[0]  = -0.10  # weak negative
    coef[3]  = -0.20  # heavy-tailed count, negative
    coef[6]  = 0.05
    BIAS = -0.68

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(z), hidden 1 = relu(-z)  ->  h0 - h1 = z = coef . x
    fc1_w[0] = coef
    fc1_w[1] = -coef

    # class-1 logit = BIAS + z ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_b[1] = BIAS

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
