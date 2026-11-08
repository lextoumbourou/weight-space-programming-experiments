## Step 16: revert x10 and strengthen x4

**What step 15 showed.** Raising x10 to 1.5 made the loss slightly worse (0.483 against 0.478).
- The model now predicts class 1 too often: 274 predicted, against 230 that really are class 1.
- One likely reason is that x5 and x9 overlap with x10, so x10's effect was already being counted more than once.

**This step.** Two changes from step 14:
- x10 goes back to 1.2.
- x4, the strong negative binary feature, is strengthened from −0.6 to −0.9. This also pulls down the false positives.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.2    # dominant positive feature
    w[4]  = -0.9   # strong negative feature (was -0.6)
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.25   # positive
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.6       # bias for class-1 logit

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = h0 - h1 + b = w.x + b ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
