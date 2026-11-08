## Step 14: put all linear terms in two units and scale them up

**What step 13 showed.** x11 lowered the loss to 0.516, against about 0.535 expected for a useless feature. So it is mildly positive, with cov ≈ +0.04. I keep it.

**Two changes this step.**

1. **Fewer hidden units.** A linear score z = w·x needs only two ReLU units, because relu(z) − relu(−z) = z. Putting the whole linear part into units 0 and 1 frees units 2–15 for non-linear probes later, such as |x_i| or interactions.
2. **Larger weights.** Weights of 0.5 were a probe size, not a fitted size. From the estimated covariances divided by p(1−p) ≈ 0.24, the best weights should be around 0.5–0.65 or larger. Logistic coefficients are usually larger than this marginal estimate once the other features are in the model. So I multiply the whole linear direction by 1.4.

**The linear direction before scaling:** +0.5·x1 − 0.5·x4 − 0.5·x6 + 0.5·x7 − 0.5·x9 + 0.5·x11.

**How to read the result.** If the loss drops below 0.516, larger weights help.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # Linear direction w (class-1 logit contribution = scale * w.x)
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.5    # x1 positive
    w[4] = -0.5   # x4 negative
    w[6] = -0.5   # x6 negative
    w[7] = 0.5    # x7 positive (strong)
    w[9] = -0.5   # x9 negative (strong)
    w[11] = 0.5   # x11 positive (mild)
    scale = 1.4

    # Unit 0 = relu(w.x), unit 1 = relu(-w.x); logit1 += scale*(h0 - h1)
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = scale
    W2[1, 1] = -scale

    # Units 2..15 unused (reserved for nonlinear probes)

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
