## Step 3: keep x1 and add x2

**What step 2 showed**
- x1 is clearly informative, with positive sign.
- Loss was 0.640, against about 0.79 expected for an unrelated feature and 0.671 for the prior alone.

**This step**
- I keep x1 at coefficient 1 and the prior bias.
- I add x2 linearly with coefficient 1.
- If x2 is unrelated to the labels, the extra noise should push the loss up by roughly 0.1, to about 0.74.
  - A loss clearly below 0.640 means x2 helps, with positive sign.
  - A large jump in loss suggests x2 is informative with negative sign.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    lin[1] = 1.0   # known: x1 positive
    lin[2] = 1.0   # probe: x2

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
