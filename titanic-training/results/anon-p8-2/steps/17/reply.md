## Step 17: decrease the weight on x10

**Step 16 result.** Raising x10's weight to 1.5 made the loss worse (0.4761). So the best weight is at or below 1.2.

That fits x10 overlapping with the other positive features: they already carry part of its signal.

**This step.** I'm testing x10 at 1.0, with the bias kept at −0.68.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.00   # strongest positive (testing lower)
    coef[4]  = -0.50  # strong negative
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
