## Step 24: try the low-tail unit on x8 and x11

**Step 23 result.** Loss and predictions were exactly unchanged, so unit 4 never fired. No row has x12 < −1.5, which means x12 has no long low tail.

**This step.** I'm moving the same low-tail idea to two other features that might be continuous, x8 and x11:
- **Unit 4** = relu(−x8 − 1.5), output weight +0.8 on the class-1 logit.
- **Unit 5** = relu(−x11 − 1.5), output weight +0.8 on the class-1 logit.

If the loss doesn't change, neither feature has values below −1.5. If it does change, I'll separate the two next step.

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

    # hidden 4: low tail of x8 (x8 < -1.5) -> raises class-1 logit
    fc1_w[4, 8] = -1.0
    fc1_b[4] = -1.5
    fc2_w[1, 4] = 0.8

    # hidden 5: low tail of x11 (x11 < -1.5) -> raises class-1 logit
    fc1_w[5, 11] = -1.0
    fc1_b[5] = -1.5
    fc2_w[1, 5] = 0.8

    fc2_b[1] = BIAS

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
