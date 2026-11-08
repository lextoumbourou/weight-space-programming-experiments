## Step 7: probe feature x6

**What step 6 showed about x5:**
- 165 rows have x5 > 0.475, and 95 of them (58%) are class 1.
- Among the other 435 rows, 135 (31%) are class 1.
- The loss of 0.6159 is the best single-feature loss so far.
- So x5 is a good positive predictor, and it looks like a continuous, right-skewed variable.

**Findings so far:**

| Feature | Association with class 1 |
|---|---|
| x0 | weak negative |
| x1 | strong positive |
| x2 | moderate positive |
| x3 | weak positive |
| x4 | strong negative |
| x5 | good positive |

**This step:** I probe x6 the same way, with a = +1 and b = −0.475.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 6        # which input feature is being probed this step
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
