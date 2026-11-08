## Step 4: probe feature x3

**What step 3 showed**
- x2 has at most a weak positive effect.
- The loss of 0.768 is only slightly below the ≈0.79 I expect for an irrelevant feature.
- 45% of rows predicted class 1 were truly class 1, against 37% of rows predicted class 0.
- I'll note x2 as "weak +" and come back to it later, including a test for non-linear effects.

**What I'm doing now**
- I probe x3 with the same linear setup.

```python
import numpy as np

def build_weights():
    FEAT = 3        # feature index being probed
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
