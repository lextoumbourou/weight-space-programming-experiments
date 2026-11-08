## Step 7: probe feature x6

**What step 6 showed**
- x5 has a weak positive effect.
- The loss of 0.765 is a little below the ≈0.79 noise level.
- 42% of rows predicted class 1 were truly class 1, against 37% of rows predicted class 0.

**Survey so far**

| Feature | Linear effect |
| --- | --- |
| x0 | none |
| x1 | strong + |
| x2 | weak + |
| x3 | none |
| x4 | strong − |
| x5 | weak + |

**What I'm doing now**
- I probe x6 with the same linear setup.

```python
import numpy as np

def build_weights():
    FEAT = 6        # feature index being probed
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
