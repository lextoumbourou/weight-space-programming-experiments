## Step 23: add a "very low x12" unit

**Step 22 result.** Switching unit 2 off made the loss worse (0.4612 vs 0.4584), so unit 2 is useful. I'll restore it at −0.5.

**Next idea.** The linear model may be missing an effect at one extreme of a weak-looking feature. x12 looks continuous: about 16% of rows sit above +0.95, at roughly the base class-1 rate. A narrow band of very low x12 values might be strongly class 1 without showing much in the overall correlation.

**This step.** I'm adding hidden unit 4 = relu(−x12 − 1.5), which is only active when x12 < −1.5. Its output weight is +0.8 on the class-1 logit. If the loss drops, the hypothesis holds; otherwise I'll remove the unit.

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

    # hidden 2: AND(x10 high, x4 high) -> lowers class-1 logit (restored)
    fc1_w[2, 10] = 1.0
    fc1_w[2, 4] = 1.0
    fc1_b[2] = -1.5
    fc2_w[1, 2] = -0.5

    # hidden 3: AND(x10 high, x4 low) -> raises class-1 logit
    fc1_w[3, 10] = 1.0
    fc1_w[3, 4] = -1.0
    fc1_b[3] = -1.0
    fc2_w[1, 3] = 0.9

    # hidden 4: very low x12 (x12 < -1.5) -> raises class-1 logit
    fc1_w[4, 12] = -1.0
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
