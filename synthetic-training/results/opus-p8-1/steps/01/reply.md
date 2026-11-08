## Step 1: probing feature x0

I have no information yet, so I'll start by testing one feature at a time.

**The probe.** The class-1 logit minus the class-0 logit is set to 0.5·x0. Everything else is zero.

- A linear term needs two ReLU units, because ReLU cuts off negative values: relu(x0) − relu(−x0) = x0.
- All other hidden units and biases are zero.

**What the feedback will tell me.**

- **Confusion matrix:** its row sums give the class balance.
- **Loss compared with ln 2 ≈ 0.693:**
  - Below ln 2 means x0 is positively related to class 1.
  - Above ln 2 means it is negatively related.
  - About ln 2 means x0 has little linear relationship with the label.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    probe = 0   # feature being probed this step
    s = 0.5     # probe strength

    # Hidden unit 0 = relu(x_probe), hidden unit 1 = relu(-x_probe)
    W1[0, probe] = 1.0
    W1[1, probe] = -1.0

    # Class-1 logit = s*(h0 - h1) = s*x_probe ; class-0 logit = 0
    W2[1, 0] = s
    W2[1, 1] = -s

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
