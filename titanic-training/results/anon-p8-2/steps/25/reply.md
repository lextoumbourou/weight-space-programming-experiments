## Step 25: try the low-tail unit on x7

**Step 24 result.** Again nothing changed at all, so neither x8 nor x11 has values below −1.5. Like x12, they look like counts or indicators with a floor near their low end.

**Choosing the next candidate.** Of the features not yet ruled out, x7 is the most likely continuous one, with a spread of values on both sides of zero. In its probe, 20% of rows sat above +0.95, with a class-1 rate (46%) above the base rate.

**This step.** I'm removing the two dead units and adding:
- **Unit 4** = relu(−x7 − 1.5), output weight +0.8 on the class-1 logit. It checks whether very low x7 values favour class 1.

```python
import numpy as np
import math

def build_weights():
    # linear score coefficients (per standardised feature) for class-1 log-odds
    coef = np.zeros(13, dtype=np.float32)
    coef[10] = 1.20
    coef[4]  = -0.40
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
    fc2_w[1, 3] = 0.9

    # hidden 4: low tail of x7 (x7 < -1.5) -> raises class-1 logit
    fc1_w[4, 7] = -1.0
    fc1_b[4] = -1.5
    fc2_w[1, 4] = 0.8

    fc2_b[1] = BIAS

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
