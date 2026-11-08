## Step 25: return to step 23 and raise the intercept

**What step 24 showed:**
- Pushing the interaction further made the loss worse: 0.4618, against 0.4573 in step 23.
- That step also predicted class 1 for only 155 rows, against 230 true class-1 rows.
- Step 23 already predicted only 172 class-1 rows, so the model may now lean too far toward class 0.

**This step:** I go back to the step-23 weights (w[10] = 1.5, interaction weight −0.8) and make one change: the intercept moves from −0.70 to −0.55.

```python
import numpy as np

def build_weights():
    # linear score z = w . x  ->  contributes z to logit(class1) - logit(class0)
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.50   # strongest positive predictor (step-23 value)
    w[4]  = -0.60  # strong negative predictor
    w[1]  = 0.30   # strong positive (overlaps with x4/x5)
    w[9]  = 0.15   # overlaps with x10
    w[5]  = 0.15   # continuous/skewed positive
    w[2]  = 0.15   # moderate positive
    w[11] = 0.00
    w[0]  = -0.05  # weak negative
    w[3]  = -0.40  # conditional negative
    w[12] = -0.35  # conditional negative
    w[7]  = 0.00
    c = -0.55      # intercept (raised from -0.70)

    # interaction unit: fires only when x10 high AND x4 high
    INT_THR = 1.2
    INT_W = -0.8   # step-23 value

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
