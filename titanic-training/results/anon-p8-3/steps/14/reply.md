## Step 14: first combined model

All 13 features are now probed. I converted each probe's split into a rough standardized log-odds effect. Then I shrank the effects of features that probably overlap with stronger ones.

| Feature | Rough effect | Starting weight | Notes |
|---|---|---|---|
| x10 | ≈ +1.1 | +1.2 | dominant feature |
| x4 | ≈ −0.7 | −0.6 | |
| x1 | ≈ +0.6 | +0.3 | likely overlaps with x4 and x5 |
| x9 | ≈ +0.66 | +0.15 | likely overlaps heavily with x10 |
| x5 | ≈ +0.5 | +0.15 | likely overlaps with x1 and x4 |
| x2 | ≈ +0.3 | +0.15 | |
| x11 | ≈ +0.3 | 0 | |
| x0 | ≈ −0.3 | −0.05 | |
| x3 | weak | −0.1 | features like this often turn negative once the others are controlled for |
| x6, x7, x8, x12 | weak or neutral | 0 | |

**How the network computes it:**
- One linear score z = w·x + c.
- Hidden unit 0 = ReLU(z) and hidden unit 1 = ReLU(−z), so their difference is exactly z.
- The logit difference is z itself, and c = −0.6.
- The other 14 hidden units stay at zero for now. I'll use them later for non-linear effects and interactions.

From here I'll tune the weights one at a time against the validation loss.

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
    w[11] = 0.00   # moderate positive alone, overlaps with others
    w[0]  = -0.05  # weak negative
    w[3]  = -0.10  # weak positive alone; guess negative once others controlled
    c = -0.60      # intercept

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(z), hidden 1 = relu(-z)  (intercept handled in output bias)
    W1[0, :] = w
    W1[1, :] = -w

    # logit1 - logit0 = h0 - h1 = w.x  (split symmetrically)
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
