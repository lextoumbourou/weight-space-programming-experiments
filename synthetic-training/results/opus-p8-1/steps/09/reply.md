## Step 9: add −0.5·x6, probe x7

**What the mirrored pair (steps 7 and 8) showed.**

- **x6:** the losses with +0.5·x6 and −0.5·x6 differ by 0.066. That gives cov(x6, y) ≈ −0.066, so x6 is genuinely negative. I keep it at −0.5.
- **Null reference:** the average of the two runs, 0.630, is what a useless feature would have scored on that base. Step 6's x5 probe scored 0.621, only slightly better. So x5 has at most a weak positive effect, with cov ≈ +0.02, and stays out for now.

**What I'm doing now.**

- The base is now the prior bias plus 0.5·x1 − 0.5·x4 − 0.5·x6, which scored 0.597.
- I add a probe of 0.5·x7.

**How to read the result.** If x7 is useless, the loss should be about 0.597 + 0.027 ≈ 0.624.

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
    add_linear(6, 7, 0.5)    # probe: x7

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
