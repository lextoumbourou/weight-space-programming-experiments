## Step 15: strengthen the dominant feature x10

**Where things stand.** The first combined model brought the loss down to 0.478, from about 0.62 for the best single feature. Accuracy is 76%.

**Method from here.** I will tune one coefficient at a time and keep a change only if the validation loss improves.

**This step.** I raise the weight on x10, the dominant feature, from 1.2 to 1.5. A well-fitted logistic model usually puts a larger weight on its strongest binary feature than my first guess did. Everything else stays the same as in step 14.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.5    # dominant positive feature (was 1.2)
    w[4]  = -0.6   # strong negative feature (binary)
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
