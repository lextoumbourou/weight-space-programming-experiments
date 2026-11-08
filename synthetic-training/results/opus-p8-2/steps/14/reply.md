## Step 14: drop x10, probe x11

**What step 13 showed**
- Adding x10 raised the loss from 0.516 to 0.606, about +0.09.
- That matches the noise penalty, so x10 looks linearly uninformative.

**This step**
- I keep x1 at +1, x4 at −1, x7 at +1, x9 at −1 and the prior bias.
- I add x11 linearly with coefficient +1, judged against the baseline of 0.516.
- After this, all 12 features will have been probed linearly.

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
    lin[11] = 1.0   # probe: x11   (x10 looked uninformative linearly)

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
