## Step 3: probe feature x2

**What step 2 showed.** x1 is useful and points towards class 1.
- Putting +0.5 on x1 dropped the loss from about 0.665 to 0.620, even though a useless weight of that size would add about 0.03.
- That puts x1's correlation with the label at roughly +0.3.
- 142 rows (24%) had x1 > 0.98 and were predicted class 1, at about 65% precision.

**This step.** Run the same probe on x2 alone, with weight +0.5. Earlier features stay at zero until all the probes are done.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[2] = 0.5          # probing feature x2 alone this step

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
