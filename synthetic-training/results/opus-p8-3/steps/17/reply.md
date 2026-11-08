## Step 17: |x| probe on x1

**What step 16 showed**
- The |x3| term raised the loss by 0.009, about the noise level.
- With no linear effect either, x3 looks irrelevant.

**What I'm changing**
- Non-linear structure is more likely in features that already carry signal, so I'm switching the |x| probe to the strong features.
- This step tests `+0.5·(|x1| − 0.8)` on top of the linear base.

**How to read the result**
- Combined with the linear term, the probe also picks up asymmetry, for example an effect that only exists for positive x1.
- A drop means extreme x1 values on either side push towards class 1.
- A rise well beyond 0.008 means the opposite: extremes push towards class 0, or the effect saturates.

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
    PROBE_F = 1
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
