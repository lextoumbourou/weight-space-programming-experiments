## Step 12: probe feature x11

**What step 11 showed.** x10 is the strongest single feature so far.
- Putting +0.5 on x10 dropped the loss to 0.572, and accuracy rose to 77%.
- That points to a correlation of roughly +0.5 with class 1.
- The roughly 35% of rows with high x10 are about 72% class 1. This looks like a dominant binary indicator.

**This step.** Same single-feature probe on x11 at +0.5. One more probe (x12) follows, then I will combine all the features.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[11] = 0.5         # probing feature x11 alone this step

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
