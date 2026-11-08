## Step 11: probe feature x10

**What step 10 showed about x9:**
- 133 rows have x9 > 0.475, and 90 of them (68%) are class 1.
- Among the other 467 rows, 140 (30%) are class 1.
- So x9 is a strong positive predictor, similar in strength to x1.

**Findings so far:**
- Strong positive: x1, x9.
- Good positive: x5.
- Strong negative: x4.
- Moderate positive: x2.
- Weak: x0 (negative), x3, x6, x7 (positive).
- About neutral: x8.

**This step:** I probe x10 the same way, with a = +1 and b = −0.475.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 10       # which input feature is being probed this step
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
