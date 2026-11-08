## Step 27: try x9 at zero

**Step 26 result.** Raising x9 to 0.45 made the loss worse (0.4653 vs 0.4584), so its best weight is at or below 0.2.

That fits x9 overlapping heavily with x10 and the interaction units: once those are in the model, x9 adds little on its own.

**This step.** I'm testing x9 = 0. Together with the values at 0.20 and 0.45, that gives a third point to fit a parabola.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20
    coef[4]  = -0.40
    coef[1]  = 0.30
    coef[9]  = 0.00   # testing zero (0.20 -> 0.4584, 0.45 -> 0.4653)
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
