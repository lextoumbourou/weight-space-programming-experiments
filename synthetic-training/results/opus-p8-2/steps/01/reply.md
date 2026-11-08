## Step 1: probe feature x0 on its own

I have no information yet, so the first steps will probe one feature at a time.

**How the network does it**
- Two hidden units carry the feature exactly, using x = ReLU(x) − ReLU(−x).
  - Unit 0 computes ReLU(x0).
  - Unit 1 computes ReLU(−x0).
- The output layer is set so that the logit gap (logit1 − logit0) equals x0.
- All other units and weights are zero.

**What I learn from the feedback**
- The rows of the confusion matrix show the class balance.
- The loss compared with ln 2 ≈ 0.693 shows how much x0 alone helps, and its sign.
  - Loss below ln 2 means x0 predicts the labels in the expected direction.
  - Loss above ln 2 means it predicts them, but with the opposite sign.

The code is written in a general form, with a linear coefficient and an |x| coefficient per feature. Later steps will only change the coefficient tables.

```python
import numpy as np

def build_weights():
    # Coefficients for the logit gap  d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = 0.0

    # ---- Step 1 probe: only x0, linear, coefficient 1.0 ----
    lin[0] = 1.0

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Use hidden-unit pairs: unit 2k = relu(x_f), unit 2k+1 = relu(-x_f)
    #   linear term:  c*x  = c*relu(x) - c*relu(-x)
    #   abs term:     a*|x| = a*relu(x) + a*relu(-x)
    # Each feature with a nonzero coefficient gets one pair (max 8 features).
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:8]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0    # relu(x_f)
        W1[v, f] = -1.0   # relu(-x_f)
        cp = lin[f] + absc[f]      # coefficient on relu(x_f)
        cn = -lin[f] + absc[f]     # coefficient on relu(-x_f)
        # Split the gap symmetrically across the two logits
        W2[1, u] = 0.5 * cp;  W2[0, u] = -0.5 * cp
        W2[1, v] = 0.5 * cn;  W2[0, v] = -0.5 * cn

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
