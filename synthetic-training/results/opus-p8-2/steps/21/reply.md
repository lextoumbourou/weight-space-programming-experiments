## Step 21: probe |x9|

**What step 20 showed**
- Adding 0.5·|x7| changed the loss by only +0.002, from 0.506 to 0.508.
- That is within noise, so x7 appears to act linearly.

**This step**
- I keep the best linear model (±0.7 on x1, x4, x7, x9, plus the prior bias).
- I add 0.5·|x9|, with the bias shifted to keep it centred.
- This completes the |x| checks on the four useful features.
- If nothing shows up, I will move on to:
  - probing pairwise interactions;
  - re-weighting the individual features;
  - adding the weak candidates x11, x5 and x6.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    s = 0.7             # best overall scale found
    lin[1] =  1.0 * s   # x1 positive
    lin[4] = -1.0 * s   # x4 negative
    lin[7] =  1.0 * s   # x7 positive
    lin[9] = -1.0 * s   # x9 negative

    # ---- probe: |x9| ----   (|x0|, |x1|, |x4|, |x7| showed no useful effect)
    absc[9] = 0.5
    bias -= 0.798 * float(np.sum(absc))   # keep logits centred

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
