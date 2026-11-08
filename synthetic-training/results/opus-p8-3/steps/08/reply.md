## Step 8: probe feature x7

**What step 7 showed**
- x6 has a moderate negative effect.
- The loss of 0.849 is above the ≈0.79 noise level.
- Only 33% of rows predicted class 1 were truly class 1, against 43% of rows predicted class 0.

**Survey so far**

| Feature | Linear effect |
| --- | --- |
| x0 | none |
| x1 | strong + |
| x2 | weak + |
| x3 | none |
| x4 | strong − |
| x5 | weak + |
| x6 | moderate − |

**What I'm doing now**
- I probe x7 with the same linear setup.

```python
import numpy as np

def build_weights():
    FEAT = 7        # feature index being probed
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
