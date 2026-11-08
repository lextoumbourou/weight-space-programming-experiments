## Step 14: first combined model

**What step 13 showed.** x12 is near zero; its high tail of 96 rows is 40% class 1, against a 38% base rate.

**What the single-feature probes give, as rough correlations with class 1:**

| Feature | Rough correlation | What it suggests |
|---|---|---|
| x10 | +0.5 | Dominant binary indicator |
| x4 | −0.33 | Binary feature (max value below 1) |
| x1, x5, x9 | about +0.3 each | Strongly positive |
| x2 | +0.15 | Weakly positive |
| x0 | −0.12 | Weak, binary |
| x3 | slightly negative | Long tail that favours class 0 |
| x8 | about 0 to slightly negative | Weak |
| x6, x7, x11, x12 | about 0 to +0.1 | Weak |

**This step.** All features go into one logistic model, still built from the same ±(w·x) pair of hidden units.
- Coefficients are roughly proportional to the correlations above.
- x1, x5 and x9 are scaled down, because they probably overlap with x10.
- The bias is a little more negative than the prior. Once strong features are included, the average row sits further from the decision boundary.

From here I will tune one coefficient at a time against the validation loss.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features (guesses from single-feature probes)
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.2    # dominant positive feature
    w[4]  = -0.6   # strong negative feature (binary)
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive (may overlap with x10)
    w[9]  = 0.25   # positive (may overlap with x10)
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative
    # x6, x7, x11, x12 left at 0 for now

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
