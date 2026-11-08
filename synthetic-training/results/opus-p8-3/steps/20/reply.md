## Step 20: perturb x1 the other way to calibrate the curvature

**What step 19 showed**
- With x1 at +0.3 the loss rose by 0.0107.
- If the curvature is h ≈ 0.2, the gradient is about zero, so x1 is already close to optimal.
- That depends entirely on my assumed h, though.

**What I'm testing now**
- x1 at −0.3, i.e. 0.33. Combined with step 19, this gives a two-sided measurement:
  - gradient: `g = (L+ − L−) / 0.6`
  - curvature: `h = (L+ + L− − 2·L0) / 0.09`
- The measured h then calibrates the one-sided probes for the remaining features.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds

    # Linear direction (step-13 baseline)
    beta = np.array([
        0.0, 0.63, 0.10, 0.0, -0.49, 0.10,
        -0.24, 0.63, 0.0, -0.52, 0.0, 0.44,
    ], dtype=np.float32)

    # Coordinate perturbation probe (negative side for x1)
    PERT_F = 1
    DELTA = -0.3
    beta[PERT_F] += DELTA

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Units 0/1: relu(beta.x) - relu(-beta.x) = beta.x  -> logit difference
    W1[0] = beta
    W1[1] = -beta
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Output bias: class prior
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
