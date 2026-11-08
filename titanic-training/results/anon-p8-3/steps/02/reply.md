## Step 2: probe feature x1

**What step 1 showed about x0:**
- The class counts are 370 for class 0 and 230 for class 1, so the prior bias of −0.47 is correct.
- 443 rows have x0 > 0.47, which suggests a skewed, near-binary feature with about 74% of rows at the high value.
- Among those high-x0 rows, 153 of 443 (35%) are class 1. Among the rest, 77 of 157 (49%) are class 1.
- So x0 is weakly and negatively associated with class 1. I'll keep this result and move on.

**This step:** I probe x1 the same way, with a = +1 and b = −0.47. The predicted-class split again tells me how many rows have x1 above the threshold, and the class-1 rate on each side.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 1        # which input feature is being probed this step
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
