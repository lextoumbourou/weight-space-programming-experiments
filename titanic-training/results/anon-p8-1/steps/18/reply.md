## Step 18: weaken x4 further

**What step 17 showed.** Weakening x4 from −0.6 to −0.4 improved the loss to 0.4724, the best so far.

| x4 weight | Validation loss |
|---|---|
| −0.9 | 0.498 |
| −0.6 | 0.478 |
| −0.4 | 0.472 |

The loss keeps falling as the weight shrinks. This suggests x4's signal is largely already carried by the other features (x1, x5, x9 or x10).

**This step.** Set x4 to −0.2 to find where its optimum lies. Everything else is unchanged.

```python
import numpy as np
import math

def build_weights():
    # Linear logistic coefficients on standardised features
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.2    # dominant positive feature
    w[4]  = -0.2   # negative feature, mostly redundant (testing weaker: was -0.4)
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.25   # positive
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.6       # bias for class-1 logit

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = h0 - h1 + b = w.x + b ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
