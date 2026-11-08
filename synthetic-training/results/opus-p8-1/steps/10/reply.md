## Step 10: add 0.5·x7, probe x8

**What step 9 showed.** x7 is strongly positive. The loss fell to 0.548 and accuracy rose to 0.738, against about 0.624 expected for a useless feature. That implies cov(x7, y) ≈ 0.15, the strongest feature found so far. It stays in at 0.5 for now, and I'll tune the strengths later.

**What I'm doing now.**

- The base is the prior bias plus 0.5·x1 − 0.5·x4 − 0.5·x6 + 0.5·x7, which scored 0.548.
- I add a probe of 0.5·x8.

**How to read the result.** If x8 is useless, the loss should be about 0.573.

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

    add_linear(0, 1, 0.5)    # confirmed: x1 positive
    add_linear(2, 4, -0.5)   # confirmed: x4 negative
    add_linear(4, 6, -0.5)   # confirmed: x6 negative
    add_linear(6, 7, 0.5)    # confirmed: x7 positive (strong)
    add_linear(8, 8, 0.5)    # probe: x8

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
