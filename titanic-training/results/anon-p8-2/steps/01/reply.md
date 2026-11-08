## Step 1: probe feature x0

I can't see any rows, so I'll start by measuring each feature on its own. The 13 features may be confounded, so this is only a first estimate.

**Baseline.** If the class-1 rate is about 38%, a constant bias of −0.47 on the class-1 logit (the log-odds of that rate) gives a loss of about 0.666. I'll check this against the first readout.

**Probe.** Each step adds a linear term w·x_i on the class-1 logit, with w = 0.5. A ReLU network can pass a feature through linearly with two hidden units: relu(x) − relu(−x) = x.

**Reading the result.** To first order, the change in loss is ΔL ≈ −0.243·r + 0.03, where r is the correlation between x_i and class 1. That gives r ≈ (0.03 − ΔL)/0.243.
- The sign of ΔL tells me which direction the feature points.
- The size of ΔL tells me how strong it is.

This step probes x0.

```python
import numpy as np
import math

def build_weights():
    PROBE = 0        # feature being probed this step
    W = 0.5          # probe weight on class-1 logit
    PRIOR = math.log(0.384 / 0.616)  # assumed log-odds of class 1 (~ -0.47)

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(x_p), hidden 1 = relu(-x_p); h0 - h1 = x_p (linear pass-through)
    fc1_w[0, PROBE] = 1.0
    fc1_w[1, PROBE] = -1.0

    # class-1 logit = PRIOR + W * x_p ; class-0 logit = 0
    fc2_w[1, 0] = W
    fc2_w[1, 1] = -W
    fc2_b[1] = PRIOR

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
