## Step 15: probe for a symmetric non-linear effect in x0

**What step 14 showed**
- GAIN = 1.5 was slightly worse than 1.0 (loss 0.519 vs 0.508), so the best scale is around 1.0–1.2.
- I'll fine-tune the scale and intercept later, because larger gains probably come from non-linear structure.
- The task says the labels may depend on features non-linearly.

**What I'm testing now**
- I keep the GAIN = 1.0 linear model as the base.
- I add a term `+0.5·(|x0| − 0.8)`, built from ReLU(x0) + ReLU(−x0) with a bias offset. Subtracting 0.8, roughly the mean of |x| for a standard normal, keeps the term centred.

**How to read the result**
- Baseline is 0.5075.
- If x0 has no |x| effect, loss should rise by only about 0.008.
- A clear drop means larger |x0| favours class 1.
- A clear rise beyond about 0.008 means larger |x0| favours class 0.

I'll then go through the other features the same way, starting with the ones that look linearly irrelevant.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds
    GAIN = 1.0                     # overall scale on the linear direction

    # Linear direction from single-feature probes
    beta = np.array([
        0.0, 0.63, 0.10, 0.0, -0.49, 0.10,
        -0.24, 0.63, 0.0, -0.52, 0.0, 0.44,
    ], dtype=np.float32) * GAIN

    # Non-linear probe: add ABS_COEF * (|x_F| - 0.8) to the logit difference
    PROBE_F = 0
    ABS_COEF = 0.5
    ABS_MEAN = 0.8   # approx E|x| for standardised feature

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Units 0/1: linear part, relu(beta.x) - relu(-beta.x) = beta.x
    W1[0] = beta
    W1[1] = -beta
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Units 2/3: relu(x_F) + relu(-x_F) = |x_F|
    W1[2, PROBE_F] = 1.0
    W1[3, PROBE_F] = -1.0
    W2[1, 2] = W2[1, 3] = ABS_COEF / 2
    W2[0, 2] = W2[0, 3] = -ABS_COEF / 2

    # Output bias: class prior, minus centring of the |x| term
    d = PRIOR - ABS_COEF * ABS_MEAN
    b2[1] = d / 2
    b2[0] = -d / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
