## Step 15: start probing nonlinear |x| terms, beginning with x0

**Linear probing is complete**
- Clearly informative: x1 (+), x4 (−), x7 (+), x9 (−). Together they give a loss of 0.516.
- x11 added only +0.058, a bit less than the noise penalty, so it may be weakly positive. I will revisit it.
- x6 may be weakly negative and x5 weakly positive.
- x0, x2, x3, x8 and x10 look linearly unrelated.

**Why look for nonlinear terms**
- The task says the labels may depend on features nonlinearly.
- So a feature that looks "irrelevant" linearly might still matter through its magnitude, |x|.

**This step**
- I add 1.0·|x0| to the current best model.
- |x| has mean about 0.80 for standardised data, so I subtract 0.80 from the bias to keep the logits centred.
- If |x0| is irrelevant, the loss should rise only slightly, about +0.03 to 0.05, because |x| has small variance.
  - A clear drop means large |x0| pushes towards class 1.
  - A large rise means large |x0| pushes towards class 0.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    lin[1] = 1.0    # known: x1 positive
    lin[4] = -1.0   # known: x4 negative
    lin[7] = 1.0    # known: x7 positive
    lin[9] = -1.0   # known: x9 negative

    # ---- probe: |x0| (centred: E|x| ~ 0.798 for standardised data) ----
    absc[0] = 1.0
    bias -= 0.798 * float(np.sum(absc))

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

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
