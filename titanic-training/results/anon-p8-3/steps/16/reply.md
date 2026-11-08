## Step 16: test x12 with a negative weight

**What step 15 showed:**
- Lowering the intercept to −0.8 left the loss almost unchanged: 0.4749 versus 0.4735 at −0.6.
- So the best intercept is probably near −0.7, and I'll use that.

**This step:** I test whether x12 helps once the other features are in the model.
- On its own, x12 looked neutral.
- That pattern fits a continuous feature whose effect only shows up after other features are accounted for.
- I give it a weight of −0.25. If the loss drops, x12 stays in the model; if not, I'll try the other sign or drop it.

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
    w[12] = -0.25  # test: neutral alone, maybe negative conditionally
    c = -0.70      # intercept (between -0.6 and -0.8, which tied)

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
