## Step 1: probe feature x0

**Plan.** With 891 rows and 13 standardised features, I will start by finding out how each feature relates to the label, one feature per step.

**How the probe works.** The network is set up to act as a plain logistic model:
- Hidden unit 0 computes `relu(w·x)`.
- Hidden unit 1 computes `relu(-w·x)`.
- The class-1 logit is `h0 - h1 + b = w·x + b`. The class-0 logit is fixed at 0.
- All other hidden units are switched off.

**Settings for this step.**
- The bias b is the log prior odds, assuming about 38% of rows are class 1.
- w = 0.5 on x0 only, with every other weight at zero.

**How to read the result.** The baseline loss with no features is about 0.666.
- If the loss drops below that, x0 is positively associated with class 1.
- If the loss rises, the association is negative.
- The size of the change shows how strong the feature is.

```python
import numpy as np
import math

def build_weights():
    # Probe vector: linear coefficients on the 13 standardised features
    w = np.zeros(13, dtype=np.float32)
    w[0] = 0.5          # probing feature x0 alone this step

    # Bias = log prior odds of class 1 (approx 38% positives assumed)
    b = math.log(0.38 / 0.62)

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
