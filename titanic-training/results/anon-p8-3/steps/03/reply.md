## Step 3: probe feature x2

**What step 2 showed about x1:**
- 142 rows have x1 > 0.475, and 93 of them (65%) are class 1.
- Among the other 458 rows, 137 (30%) are class 1.
- So x1 is a fairly strong positive predictor. It looks like a skewed indicator or a heavy-tailed variable that marks a high-rate subgroup.

**Findings so far:**
- x0: weak negative predictor.
- x1: strong positive predictor.

**This step:** I probe x2 the same way, with a = +1 and b = −0.475.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 2        # which input feature is being probed this step
    A = 1.0            # logit difference (class1 - class0) = A * x_FEATURE + B
    B = -0.475         # log(230/370): prior log-odds of class 1

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden unit 0 = relu(+x_k), hidden unit 1 = relu(-x_k); difference = x_k
    W1[0, FEATURE] = 1.0
    W1[1, FEATURE] = -1.0

    # symmetric split of the coefficient across the two logits
    W2[1, 0] = A / 2;  W2[1, 1] = -A / 2
    W2[0, 0] = -A / 2; W2[0, 1] = A / 2

    # prior bias
    b2[1] = B / 2
    b2[0] = -B / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
