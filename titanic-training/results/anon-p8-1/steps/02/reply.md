## Step 2: probe feature x1

**What step 1 showed.**
- With no features the loss should be about 0.665, the cost of predicting the 38% prior for every row.
- Putting +0.5 on x0 pushed the loss up to 0.725. The extra loss is about twice what a useless feature would add, so x0 leans towards class 0: higher x0 means less likely class 1.
- The effect is fairly weak. My estimate is a correlation of roughly −0.1 to −0.15.
- No row was predicted class 1, so 0.5·x0 never exceeded 0.49. That means x0's largest standardised value is below about 1. This points to a skewed binary feature where most rows sit at the positive value.

**This step.** Run the same probe on x1 alone, with weight +0.5. x0 is left at zero for now; I will set its final weight once all the probes are done.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[1] = 0.5          # probing feature x1 alone this step

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
