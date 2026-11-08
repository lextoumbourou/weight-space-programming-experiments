## Step 5: probe x4

**What step 4 showed.** The loss was 0.668, almost exactly the 0.665 expected for a useless feature. So x3 has no clear linear effect. I drop it, though it may still matter non-linearly, which I'll check later.

**What I'm doing now.** The base stays as the prior bias plus 0.5·x1. I add a probe of 0.5·x4.

**How to read the result.** As before, if x4 is useless the loss should be about 0.665.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    def add_linear(unit, feat, s):
        # Units (unit, unit+1) = relu(x), relu(-x); class-1 logit += s*x
        W1[unit, feat] = 1.0
        W1[unit + 1, feat] = -1.0
        W2[1, unit] = s
        W2[1, unit + 1] = -s

    add_linear(0, 1, 0.5)   # confirmed: x1 positive
    add_linear(2, 4, 0.5)   # probe: x4

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
