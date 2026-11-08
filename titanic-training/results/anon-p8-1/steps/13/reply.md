## Step 13: probe feature x12, the last single-feature probe

**What step 12 showed.** x11 is weak.
- The loss rose about 0.015 above the 0.665 baseline. That is less than the roughly 0.03 a useless feature would add, so the correlation is near zero to slightly positive (about +0.05).
- Its high tail of 55 rows is about 45% class 1, close to the 38% base rate.

**Running summary of estimated correlations with class 1:**

| Feature | Estimated correlation | Note |
|---|---|---|
| x0 | about −0.12 | |
| x1 | about +0.3 | |
| x2 | about +0.15 | |
| x3 | about −0.05 | tail favours class 0 |
| x4 | about −0.33 | |
| x5 | about +0.3 | |
| x6 | about +0.1 | |
| x7 | about +0.08 | |
| x8 | about 0 or slightly negative | |
| x9 | about +0.3 | |
| x10 | about +0.5 | dominant |
| x11 | about +0.05 | |

**This step.** Same single-feature probe on x12 at +0.5. After this I move on to combined models.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[12] = 0.5         # probing feature x12 alone this step

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
