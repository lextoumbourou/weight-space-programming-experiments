## Step 2: probe x1, with a class-prior bias

**What step 1 showed**
- The class counts are 605 for class 0 and 395 for class 1.
  - A model that only predicts these priors would score a loss of about 0.671.
  - Its logit-gap bias would be ln(395/605) ≈ −0.43.
- x0 on its own scored 0.822 loss and 0.509 accuracy.
  - A feature unrelated to the labels, with coefficient 1, should score about 0.81.
  - So x0 looks linearly uninformative, possibly slightly harmful.
  - I may still check |x0| later in case it matters nonlinearly.

**This step**
- I add the prior bias of −0.43, so the baseline for comparison is 0.671 rather than 0.693.
- I probe x1 linearly with coefficient 1.
- If x1 is unrelated to the labels, I expect a loss of about 0.79.
  - A clearly lower loss means x1 is informative with positive sign.
  - A clearly higher loss suggests it is informative with negative sign.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior: 395 class-1 vs 605 class-0

    # ---- Step 2 probe: x1 linear, coefficient 1.0 ----
    lin[1] = 1.0

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden-unit pairs per used feature: unit 2k = relu(x_f), unit 2k+1 = relu(-x_f)
    #   c*x  = c*relu(x) - c*relu(-x);   a*|x| = a*relu(x) + a*relu(-x)
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:8]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        cp = lin[f] + absc[f]
        cn = -lin[f] + absc[f]
        W2[1, u] = 0.5 * cp;  W2[0, u] = -0.5 * cp
        W2[1, v] = 0.5 * cn;  W2[0, v] = -0.5 * cn

    # Bias split symmetrically over the two logits
    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
