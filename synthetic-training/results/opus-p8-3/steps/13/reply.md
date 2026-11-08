## Step 13: first combined linear model

**What step 12 showed**
- x11 is moderately to strongly positive.
- 52% of rows predicted class 1 were truly class 1.

**Estimating each feature's weight**

Under a simple quadratic approximation, the probe loss is roughly
`L ≈ L0 + 0.12·s² − s·cov(x, y)`, with L0 ≈ 0.671 and slope s = 1.

So for each feature, `cov ≈ 0.790 − loss`, and a logistic weight is roughly `β ≈ cov / 0.239`.

| Feature | Estimated β |
| --- | --- |
| x1 | +0.63 |
| x7 | +0.63 |
| x4 | −0.49 |
| x9 | −0.52 |
| x11 | +0.44 |
| x6 | −0.24 |
| x2 | +0.10 |
| x5 | +0.10 |
| x0, x3, x8, x10 | ≈ 0 |

**What I'm doing now**
- I combine these weights into one linear logit and keep the prior bias.
- The combined direction is built from a ReLU(+z) / ReLU(−z) pair.
- The remaining hidden units stay at zero, kept free for non-linear terms later.
- Single-feature estimates tend to be attenuated, so the optimal overall scale may be above 1. I'll tune it next.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds
    GAIN = 1.0                     # overall scale on the linear direction

    # Estimated per-feature logistic coefficients from single-feature probes
    beta = np.array([
        0.0,    # x0  none
        0.63,   # x1  strong +
        0.10,   # x2  weak +
        0.0,    # x3  none
        -0.49,  # x4  strong -
        0.10,   # x5  weak +
        -0.24,  # x6  moderate -
        0.63,   # x7  strong +
        0.0,    # x8  none
        -0.52,  # x9  strong -
        0.0,    # x10 none
        0.44,   # x11 moderate +
    ], dtype=np.float32) * GAIN

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden 0 = relu(beta.x), hidden 1 = relu(-beta.x)
    W1[0] = beta
    W1[1] = -beta

    # logit1 - logit0 = h0 - h1 = beta.x
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Class prior in output bias
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
