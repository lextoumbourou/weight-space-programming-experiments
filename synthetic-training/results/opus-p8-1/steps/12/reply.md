## Step 12: add −0.5·x9, probe x10

**What step 11 showed.** x9 is strongly negative. The loss was 0.637, against about 0.573 expected for a useless feature. That implies cov(x9, y) ≈ −0.13.

**What I'm doing now.**

- The base is the prior bias plus 0.5·x1 − 0.5·x4 − 0.5·x6 + 0.5·x7 − 0.5·x9. I expect it to score about 0.51 on its own.
- I add a probe of 0.5·x10.

**How to read the result.** If x10 is useless, the loss should be about 0.51 + 0.024 ≈ 0.535.

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

    add_linear(0, 1, 0.5)     # confirmed: x1 positive
    add_linear(2, 4, -0.5)    # confirmed: x4 negative
    add_linear(4, 6, -0.5)    # confirmed: x6 negative
    add_linear(6, 7, 0.5)     # confirmed: x7 positive (strong)
    add_linear(8, 9, -0.5)    # confirmed: x9 negative (strong)
    add_linear(10, 10, 0.5)   # probe: x10

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
