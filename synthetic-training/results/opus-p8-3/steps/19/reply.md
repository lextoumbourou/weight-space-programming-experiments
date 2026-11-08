## Step 19: start fine-tuning the linear weights, one coordinate at a time (x1)

**What step 18 showed**
- The x1·x7 interaction raised the loss by 0.014, only slightly above the ≈0.008 noise level.
- So the interaction is negligible, perhaps weakly negative.
- Together with the earlier |x| probes, the problem looks close to linear. The remaining gains probably come from getting each linear weight right.

**Method**
- I perturb one weight by δ = +0.3 and keep everything else at the step-13 model, which had loss 0.5075.
- Near the optimum, `L(δ) ≈ L + δ·g + ½·h·δ²`.
- Earlier probes suggest h ≈ 0.2 for a standardised feature, so the curvature term is about 0.009 at δ = 0.3.
- From the observed loss change I can estimate the gradient g and the best step `−g/h` for that weight.

**What I'm testing now**
- x1, increased from 0.63 to 0.93.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds

    # Linear direction (step-13 baseline)
    beta = np.array([
        0.0, 0.63, 0.10, 0.0, -0.49, 0.10,
        -0.24, 0.63, 0.0, -0.52, 0.0, 0.44,
    ], dtype=np.float32)

    # Coordinate perturbation probe
    PERT_F = 1
    DELTA = 0.3
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
