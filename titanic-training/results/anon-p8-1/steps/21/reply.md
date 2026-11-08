## Step 21: test a larger weight on x9

**Where things stand.** The linear model has levelled off at a loss of about 0.472.
- Moving the bias from −0.6 to −0.75 changed almost nothing, so the intercept is close to right. I set it to −0.7.
- x10, x4 and x1 have each been tuned in both directions already.

**This step.** I raise x9 from 0.25 to 0.5; all other weights stay the same. x9 was one of the stronger positive features on its own (correlation about +0.3). If it carries information that x10 does not, a larger weight should lower the loss. If it mostly duplicates x10, the loss will rise.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.2    # dominant positive feature
    w[4]  = -0.3   # negative feature, mostly redundant
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.5    # positive (testing stronger: was 0.25)
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.7       # bias for class-1 logit

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
