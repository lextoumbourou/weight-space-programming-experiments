## Step 10: probe feature x9

**What step 9 showed about x8:**
- Only 49 rows have x8 > 0.475, and 17 of them (35%) are class 1.
- Among the other 551 rows, 213 (39%) are class 1.
- So x8 is a rare indicator-like feature with almost no association. I'll treat it as roughly neutral.

**Findings so far:**

| Feature | Association with class 1 |
|---|---|
| x0 | weak negative |
| x1 | strong positive |
| x2 | moderate positive |
| x3 | weak positive |
| x4 | strong negative |
| x5 | good positive |
| x6 | weak positive |
| x7 | weak positive |
| x8 | about neutral |

**This step:** I probe x9 the same way, with a = +1 and b = −0.475.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 9        # which input feature is being probed this step
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
