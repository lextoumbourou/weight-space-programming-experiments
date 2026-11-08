## Step 11: probe feature x10

**What step 10 showed.** x9 is a fairly strong positive feature, about the same strength as x1 and x5 (correlation roughly +0.3).
- The loss dropped to 0.618.
- The 133 rows with high x9 are about 68% class 1, against a base rate of 38%.

**Still missing.** No feature so far has a correlation near ±0.5, which I would expect if one of them is the dominant predictor. It may still be among x10–x12.

**This step.** Same single-feature probe on x10 at weight +0.5.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 0.5         # probing feature x10 alone this step

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
