## Step 28: tune x5

**x9 result.** Fitting a parabola through its three tries puts the best value at about 0.12, though the gain is tiny:

| x9 weight | Loss |
|---|---|
| 0 | 0.4590 |
| 0.20 | 0.4584 |
| 0.45 | 0.4653 |

**This step.** I'm setting x9 to 0.12 and testing x5 at 0.40, up from 0.15. In its probe x5 was one of the strong positive features (r ≈ +0.33), so it may be under-weighted.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20
    coef[4]  = -0.40
    coef[1]  = 0.30
    coef[9]  = 0.12   # tuned (parabola fit)
    coef[5]  = 0.40   # testing larger (was 0.15)
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
