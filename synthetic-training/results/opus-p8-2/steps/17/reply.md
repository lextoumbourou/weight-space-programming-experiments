## Step 17: check calibration by scaling the linear weights

**What step 16 showed**
- Adding |x1| raised the loss by +0.044, from 0.516 to 0.560.
- That is a bit more than |x0| did, so there is no sign of a useful |x1| term.
- At most it hints that |x1| pushes slightly towards class 0.
- I drop |x1|.

**This step**
- Before probing more nonlinear terms, I check whether the overall size of the logits is right.
- I scale all four linear weights from ±1 to ±1.5, keeping the prior bias.
- How to read the result:
  - A loss below 0.516 means the model was under-confident, so a larger scale is better.
  - A loss above 0.516 means ±1 is about right or already too large.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    s = 1.5          # overall scale probe
    lin[1] =  1.0 * s   # x1 positive
    lin[4] = -1.0 * s   # x4 negative
    lin[7] =  1.0 * s   # x7 positive
    lin[9] = -1.0 * s   # x9 negative

    bias -= 0.798 * float(np.sum(absc))   # centring for any |x| terms (none now)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden-unit pairs per used feature: unit 2k = relu(x_f), unit 2k+1 = relu(-x_f)
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
