## Step 3: keep x1, probe x2

**What step 2 showed.** x1 is clearly positive for class 1. The loss was 0.635, against about 0.701 expected for a useless feature. That gain suggests cov(x1, y) ≈ 0.13, which is a correlation of roughly 0.27.

**What I'm doing now.** From here I build the model up step by step. Features I've confirmed stay in, and each step adds one new probe on top.

- The current base is the prior bias plus 0.5·x1, which gave a loss of 0.635.
- I add a probe of 0.5·x2, using two new hidden units.

**How to read the result.**

- If x2 is useless, the loss should rise to about 0.635 + 0.03 ≈ 0.665.
- Lower than that means x2 is positive for class 1.
- Higher means it is negative.

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
    add_linear(2, 2, 0.5)   # probe: x2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
