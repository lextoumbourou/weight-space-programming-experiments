## Step 20: tuned linear model plus a pair of interaction units

**x4 result.** Fitting a parabola through its three tries puts x4's best weight at about −0.4, so I'm using that:

| x4 weight | Loss |
|---|---|
| −0.25 | 0.4699 |
| −0.5 | ~0.4693 |
| −0.8 | 0.4816 |

**Why add interactions.** The linear model is stuck near 0.469. My working hypothesis is that:
- x10 is a binary indicator for a favoured group, taking +1.36 when on and −0.73 when off.
- x4 is a binary indicator for a disadvantaged majority, taking about +0.9 when on and −1.1 when off.

If x10's advantage depends strongly on x4, a purely additive model can't capture it. The ReLU layer can build an AND of two binary features.

**The new units.**
- **Unit 2** = relu(x10 + x4 − 1.5). It is positive only when both x10 and x4 are on (value about 0.76). Its output weight is −0.5, which lowers class-1 odds for that cell.
- **Unit 3** = relu(x10 − x4 − 1.0). It is positive only when x10 is on and x4 is off (value about 1.46). Its output weight is +0.5, which raises class-1 odds for that cell.

If the loss gets worse, the hypothesis is wrong and I'll remove these units.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20   # strongest positive (binary, ~+1.36 / -0.73)
    coef[4]  = -0.40  # strong negative (binary, ~+0.9 / -1.1), tuned
    coef[1]  = 0.30
    coef[9]  = 0.20
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
    fc2_w[1, 3] = 0.5

    fc2_b[1] = BIAS

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
