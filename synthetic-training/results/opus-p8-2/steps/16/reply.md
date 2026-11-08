## Step 16: probe |x1|

**What step 15 showed**
- Adding |x0| raised the loss by only +0.017, from 0.516 to 0.533.
- That is within noise, so x0 looks irrelevant both linearly and through its magnitude.

**Why switch to the useful features**
- Probing |x| for every "irrelevant" feature would use many steps.
- Nonlinear effects are more likely in features that already matter.
- So I now probe |x| on the four useful features, one at a time, starting with |x1|.

**This step**
- I add 1.0·|x1| on top of the linear model x1 (+), x4 (−), x7 (+), x9 (−).
- I subtract 0.80 from the bias to keep the logits centred.
- In the network, this changes x1's hidden-unit pair from c·x to c·x + a·|x|.
  - Positive values of x1 now get weight 2.
  - Negative values of x1 now get weight 0.
- How to read the result:
  - A loss below 0.516 would mean x1's effect is asymmetric, or that |x1| itself pushes towards class 1.
  - A loss clearly above 0.516 would mean |x1| pushes towards class 0.

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

    # ---- probe: |x1| (centred with E|x| ~ 0.798) ----
    absc[1] = 1.0
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
