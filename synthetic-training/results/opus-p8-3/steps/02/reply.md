## Step 2: probe feature x1

**What step 1 showed**
- The classes are imbalanced: 605 rows are class 0 and 395 are class 1.
- A constant prediction would therefore score loss ≈ 0.671, using the class-1 log-odds of ln(395/605) ≈ −0.426.
- x0 shows no linear signal. About 39% of rows were class 1 among those predicted class 1, and about the same among those predicted class 0.
- The loss of 0.733 is about what pure noise at that slope would give.

**What I'm changing**
- From now on the output bias carries the prior log-odds, so the baseline loss is ≈ 0.671.
- I probe x1 with slope 1.0.

**How to read the result**
- If x1 is irrelevant, I expect loss ≈ 0.671 + 0.12 ≈ 0.79.
- A clearly lower loss means a positive effect.
- A clearly higher loss, or a confusion matrix that looks inverted, means a negative effect.

```python
import numpy as np

def build_weights():
    FEAT = 1        # feature index being probed
    SCALE = 1.0     # slope of logit difference in that feature
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds from observed class balance

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden 0 = relu(x), hidden 1 = relu(-x)  -> together they reconstruct x
    W1[0, FEAT] = 1.0
    W1[1, FEAT] = -1.0

    # logit1 - logit0 = SCALE * x
    W2[1, 0] = SCALE / 2
    W2[1, 1] = -SCALE / 2
    W2[0, 0] = -SCALE / 2
    W2[0, 1] = SCALE / 2

    # Output bias carries the class prior
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
