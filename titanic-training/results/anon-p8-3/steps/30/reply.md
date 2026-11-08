## Step 30: settle x1 and make x5 stronger

**What steps 26–29 showed about x1:**

| w[1] | Loss |
|---|---|
| −0.10 | 0.4561 |
| 0.10 | 0.4517 |
| 0.30 | ≈ 0.4532 |

Fitting a parabola through these three points puts the best value near 0.15, so I set w[1] = 0.15.

**This step:** I tune x5 next.
- x5 was a good positive predictor on its own, with continuous, skewed values.
- I raise w[5] from 0.15 to 0.35. Everything else stays the same.

```python
import numpy as np

def build_weights():
    # linear score z = w . x  ->  contributes z to logit(class1) - logit(class0)
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.50   # strongest positive predictor
    w[4]  = -0.60  # strong negative predictor
    w[1]  = 0.15   # parabola optimum from steps 26/28/29
    w[9]  = 0.15   # overlaps with x10
    w[5]  = 0.35   # test: up from 0.15
    w[2]  = 0.15   # moderate positive
    w[11] = 0.00
    w[0]  = -0.05  # weak negative
    w[3]  = -0.40  # conditional negative
    w[12] = -0.35  # conditional negative
    w[7]  = 0.00
    c = -0.45      # intercept

    # interaction unit: fires only when x10 high AND x4 high
    INT_THR = 1.2
    INT_W = -0.8

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(z), hidden 1 = relu(-z): linear part
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = 0.5;  W2[1, 1] = -0.5
    W2[0, 0] = -0.5; W2[0, 1] = 0.5

    # hidden 2 = relu(x10 + x4 - INT_THR): x10-high & x4-high interaction
    W1[2, 10] = 1.0
    W1[2, 4] = 1.0
    b1[2] = -INT_THR
    W2[1, 2] = INT_W / 2
    W2[0, 2] = -INT_W / 2

    # intercept
    b2[1] = c / 2
    b2[0] = -c / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
