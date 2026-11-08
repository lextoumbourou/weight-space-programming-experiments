## Step 23: settle x9 and add a first nonlinear interaction unit

**What steps 20–22 showed.**
- The linear model has levelled off at a loss of about 0.472.
- For x9, a weight of 0 gives 0.4748, 0.25 gives about 0.4725 and 0.5 gives 0.4786. The best value is about 0.2, so I fix x9 there.
- Further gains need nonlinearity.

**The hypothesis.**
- x10 is the dominant positive binary feature, held by about 35% of rows.
- x4 is a negative binary feature held by about half the rows, and its value never exceeds about 1.
- These two may interact: rows with both high might have a much lower class-1 rate than the linear model predicts, while rows with x10 high and x4 low might be higher.

**The new unit.** Hidden unit 2 is `relu(x10 + x4 − 1.5)`.
- It fires only when both x10 and x4 sit at their high values, giving about 0.76 there. It is 0 or near 0 everywhere else.
- It feeds the class-1 logit with weight −1.5.
- I also raise the x10 coefficient a little, from 1.2 to 1.35, to offset part of what the unit takes away from the high-x10 rows.

If the loss drops clearly, the interaction is real and I will tune its size and threshold.

```python
import numpy as np
import math

def build_weights():
    # ---- linear part (units 0/1 carry w.x through ReLU pair) ----
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.35   # dominant positive feature (slightly up to offset interaction)
    w[4]  = -0.3   # negative binary feature
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.2    # positive (optimum ~0.2)
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.7       # bias for class-1 logit

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    # ---- interaction unit: fires only when x10 high AND x4 high ----
    fc1_w[2, 10] = 1.0
    fc1_w[2, 4]  = 1.0
    fc1_b[2] = -1.5

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = w.x + b + v*h2 ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_w[1, 2] = -1.5    # penalty when both x10 and x4 are high
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
