## Step 25: push x10 further

**What step 24 showed.** Raising x10 to 1.6 alongside the interaction unit gave the best loss so far, 0.4683.

This supports the idea behind the interaction unit:
- Rows where x10 is high and x4 is low have a much higher class-1 rate than the plain linear model gave them.
- Rows where both are high are held down separately by the interaction unit.

The confusion matrix still shows many false negatives (103), so the high-x10, low-x4 rows probably deserve an even larger logit.

**This step.** Raise the x10 coefficient from 1.6 to 2.0 and keep everything else the same.

```python
import numpy as np
import math

def build_weights():
    # ---- linear part (units 0/1 carry w.x through ReLU pair) ----
    w = np.zeros(13, dtype=np.float32)
    w[10] = 2.0    # dominant positive feature (raised from 1.6)
    w[4]  = -0.3   # negative binary feature
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.2    # positive
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
