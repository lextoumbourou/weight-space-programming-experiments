## Step 20: test x7 with a negative weight

**What step 19 showed:**
- w[3] = −0.50 gave a loss of 0.4615, about the same as −0.30 (0.4609).
- So I settle on w[3] = −0.40.

**This step:** I test x7 next.
- x7 is another weak positive, skewed, indicator-like feature.
- It may behave like x3: weakly positive alone but negative once the main predictors are included.
- I try w[7] = −0.20. Everything else stays the same.

```python
import numpy as np

def build_weights():
    # linear score z = w . x + c  ->  logit(class1) - logit(class0) = z
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.20   # strongest positive predictor
    w[4]  = -0.60  # strong negative predictor
    w[1]  = 0.30   # strong positive (likely overlaps with x4/x5)
    w[9]  = 0.15   # strong positive alone, likely overlaps with x10
    w[5]  = 0.15   # good positive, continuous/skewed
    w[2]  = 0.15   # moderate positive
    w[11] = 0.00   # moderate positive alone
    w[0]  = -0.05  # weak negative
    w[3]  = -0.40  # conditional negative (-0.30 / -0.50 tied)
    w[12] = -0.35  # conditional negative
    w[7]  = -0.20  # test: weak positive alone, maybe negative conditionally
    c = -0.70      # intercept

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(z), hidden 1 = relu(-z)
    W1[0, :] = w
    W1[1, :] = -w

    # logit1 - logit0 = h0 - h1 + c
    W2[1, 0] = 0.5;  W2[1, 1] = -0.5
    W2[0, 0] = -0.5; W2[0, 1] = 0.5
    b2[1] = c / 2
    b2[0] = -c / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
