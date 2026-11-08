## Step 18: x3 more negative

**What step 17 showed:**
- w[12] = −0.45 gave a loss of 0.4654, essentially the same as −0.25 (0.4652).
- So the best value is probably in between, and I set w[12] = −0.35.

**This step:** I test x3 next.
- On its own, x3 was weakly positive, but features like this often turn negative once the others are controlled for.
- I move w[3] from −0.10 to −0.30. Everything else stays the same.

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
    w[3]  = -0.30  # test: stronger conditional negative (was -0.10)
    w[12] = -0.35  # conditional negative (-0.25 and -0.45 tied)
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
