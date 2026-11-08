## Step 18: try a smaller scale

**What step 17 showed**
- Scaling the weights up to ±1.5 raised the loss to 0.578, against 0.516 at ±1.
- So the model is already over-confident at ±1.
- The best scale is probably below 1.

**This step**
- I scale all four linear weights down to ±0.7, keeping the prior bias.
- Comparing three points (0.7, 1.0 and 1.5) will show roughly where the best scale lies.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    s = 0.7          # overall scale probe (1.5 was worse than 1.0)
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
