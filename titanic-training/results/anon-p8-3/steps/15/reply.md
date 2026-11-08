## Step 15: lower the intercept

**What step 14 showed:**
- The combined model reached a loss of 0.4735, a big gain over the best single feature (0.535).
- It predicts class 1 for 263 rows, but only 230 rows are truly class 1.
- So the model seems biased toward class 1.

**This step:** I make one change only, lowering the intercept c from −0.6 to −0.8, so I can measure its effect on the loss directly. Next I'll tune the individual feature weights.

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
    w[3]  = -0.10  # weak; guessed negative once others controlled
    c = -0.80      # intercept (lowered from -0.60)

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
