## Step 1: probe feature x0

I can't see any data, so I'll start by probing features one at a time.

**How the probe works**
- Two hidden units compute ReLU(x0) and ReLU(−x0).
- The output weights are set so that `logit1 − logit0 = 0.5·x0`.
- Every other parameter is zero.

**How to read the result**
- Validation loss below ln 2 ≈ 0.693 means x0 is positively associated with class 1.
- Loss above 0.693 means the association is negative.
- Loss near 0.693 means there is little linear signal.
- The accuracy and confusion matrix will also show the class balance and how strong the effect is.

```python
import numpy as np

def build_weights():
    # Probe settings: which feature to test and how strongly
    FEAT = 0      # feature index being probed
    SCALE = 0.5   # logit-difference slope applied to that feature

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden unit 0 = relu(x_FEAT), hidden unit 1 = relu(-x_FEAT)
    W1[0, FEAT] = 1.0
    W1[1, FEAT] = -1.0

    # Class-1 logit gets +SCALE/2 * x, class-0 logit gets -SCALE/2 * x,
    # so logit1 - logit0 = SCALE * (relu(x) - relu(-x)) = SCALE * x
    W2[1, 0] = SCALE / 2
    W2[1, 1] = -SCALE / 2
    W2[0, 0] = -SCALE / 2
    W2[0, 1] = SCALE / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
