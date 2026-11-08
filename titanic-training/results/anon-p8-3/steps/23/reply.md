## Step 23: add an interaction between x10 and x4

**Why change approach:** single-weight tweaks have levelled off at a loss of about 0.461, so the purely linear model seems to have reached its limit. The hidden layer can capture interactions, which a linear model cannot.

**What I suspect:**
- When x10 is high and x4 is high, the class-1 rate is lower than the additive model predicts.
- When x10 is high and x4 is low, the rate is higher than the additive model predicts.
- This would explain why raising w[10] hurt: it also raised the high-x4 subgroup.

**How the new unit works:** hidden unit 2 = ReLU(x10 + x4 − 1.2), using approximate standardized values for the two features.

| x10 | x4 | Approximate sum | Unit 2 output |
|---|---|---|---|
| high (≈ +1.36) | high (≈ +0.88) | 2.24 | ≈ 1.04 |
| high | low (≈ −1.14) | 0.22 | 0 |
| low (≈ −0.73) | high | 0.15 | 0 |
| low | low | −1.87 | 0 |

So unit 2 fires only for rows where both features are high.

**Changes this step:**
- Unit 2's output enters the logit difference with weight −0.8.
- At the same time I raise w[10] to 1.5, so the high-x10 / low-x4 group gets the boost it seems to need.
- I also restore w[4] = −0.6, since −0.8 was worse.

```python
import numpy as np

def build_weights():
    # linear score z = w . x  ->  contributes z to logit(class1) - logit(class0)
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.50   # strongest positive predictor (raised; interaction compensates)
    w[4]  = -0.60  # strong negative predictor (-0.8 was worse)
    w[1]  = 0.30   # strong positive (overlaps with x4/x5)
    w[9]  = 0.15   # overlaps with x10
    w[5]  = 0.15   # continuous/skewed positive
    w[2]  = 0.15   # moderate positive
    w[11] = 0.00
    w[0]  = -0.05  # weak negative
    w[3]  = -0.40  # conditional negative
    w[12] = -0.35  # conditional negative
    w[7]  = 0.00
    c = -0.70      # intercept

    # interaction unit: fires only when x10 high AND x4 high
    INT_THR = 1.2
    INT_W = -0.8   # contribution to logit difference per unit of activation

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
