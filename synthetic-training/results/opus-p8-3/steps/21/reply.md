## Step 21: adopt the better x1 weight and probe x7

**What steps 19 and 20 showed**

| Probe | x1 weight | Loss |
| --- | --- | --- |
| step 13 baseline | 0.63 | 0.5075 |
| step 19, +0.3 | 0.93 | 0.5182 |
| step 20, −0.3 | 0.33 | 0.5060 |

- Gradient: g = (0.5182 − 0.5060) / 0.6 ≈ +0.020.
- Curvature: h = (0.5182 + 0.5060 − 2·0.5075) / 0.09 ≈ 0.10.
- So the best x1 weight is about 0.63 − 0.20 = **0.43**, which should lower the loss by about 0.002, to ≈ 0.5055.
- x1 being over-weighted suggests the features are correlated. Single-feature probes double-count shared signal, which also explains why the larger gain in step 14 hurt.

**What I'm doing now**
- I set x1 = 0.43 and probe x7 at −0.3 (0.63 → 0.33).
- With h ≈ 0.1 measured, a ±0.3 move costs about 0.0045 from curvature alone.
- So for x7, `g ≈ (0.0045 − ΔL) / 0.3`, measured relative to the predicted baseline of 0.5055 (positive g if lowering the weight helps). The best x7 is then `0.63 − g/0.1`.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds

    # Linear direction: step-13 baseline with x1 updated to its tuned value
    beta = np.array([
        0.0,    # x0
        0.43,   # x1  (tuned: was 0.63)
        0.10,   # x2
        0.0,    # x3
        -0.49,  # x4
        0.10,   # x5
        -0.24,  # x6
        0.63,   # x7
        0.0,    # x8
        -0.52,  # x9
        0.0,    # x10
        0.44,   # x11
    ], dtype=np.float32)

    # Coordinate perturbation probe on x7
    PERT_F = 7
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
