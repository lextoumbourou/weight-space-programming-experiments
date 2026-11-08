## Step 10: probe feature x9

**What step 9 showed.** x8 is weak.
- The loss rose to 0.701, about 0.035 above the baseline. That is roughly the penalty a useless weight of this size would add.
- So x8's correlation with the label is near zero, perhaps slightly negative.
- Its high tail (49 rows) is 35% class 1, close to the 38% base rate.

**This step.** Same single-feature probe on x9 at +0.5.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[9] = 0.5          # probing feature x9 alone this step

    # Bias = log prior odds of class 1 (230/600 positives)
    b = math.log(230.0 / 370.0)

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
