## Step 22: test x9 at zero

**What step 21 showed.** Raising x9 from 0.25 to 0.5 made the loss worse (0.4786 against about 0.472). x9 probably duplicates information already carried by x10, the dominant feature.

**This step.** I set x9 to 0 and leave every other weight as it was.
- If the loss stays near 0.472 or improves, x9 is redundant, and the optimum lies between 0 and 0.25.
- If the loss rises, x9 adds some information of its own, and about 0.25 is right.

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
    w[9]  = 0.0    # testing removal (was 0.25)
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
