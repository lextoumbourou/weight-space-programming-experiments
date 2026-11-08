## Step 20: revert x1, lower the bias

**What step 19 showed.** Raising x1 to 0.5 made the loss worse (0.4798 against 0.4723). It also pushed predicted positives up to 263, against 230 true positives.

The same thing happened in steps 15 and 17: strengthening positive features makes the model over-predict class 1. That suggests the intercept is too high.

**This step.** x1 goes back to 0.3 and the bias drops from −0.6 to −0.75. x4 stays at −0.3. Every other weight is unchanged.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.2    # dominant positive feature
    w[4]  = -0.3   # negative feature, mostly redundant
    w[1]  = 0.3    # positive (reverted)
    w[5]  = 0.25   # positive
    w[9]  = 0.25   # positive
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.75      # bias for class-1 logit (testing lower: was -0.6)

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
