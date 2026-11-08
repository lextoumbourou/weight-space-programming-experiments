## Step 38: flip the sign of the x10·x11 interaction

**What step 37 showed**
- The x10·x11 interaction at g = +0.5 gave a loss of 0.4935.
- That is about 0.008 worse than the matching model with no interaction, roughly 0.485.
- This is a little more than noise, so the interaction may have the opposite sign.

**This step**
- I keep everything else the same: the linear weights and the magnitude part m = −0.2 on x10 and x11.
- I set the interaction gain to g = −0.5.
- This gives −0.45 on |x10+x11| and +0.05 on |x10−x11|.
- How to read the result:
  - A loss below 0.4848 means a real negative interaction, and I will tune it.
  - Otherwise I will go back to the plain magnitude terms.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i
    #         + p*|x10 + x11| + q*|x10 - x11|      (pair block on x10, x11)
    #   p = m + g/2, q = m - g/2:
    #     m part -> magnitude effect, g part -> interaction sign(x10*x11)*min(|x10|,|x11|)
    lin  = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Main linear features
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative
    lin[6] = -0.45   # x6 negative

    # Pair block on (x10, x11)
    a_idx, b_idx = 10, 11
    m = -0.2          # magnitude part (~ -0.4 per |x|)
    g = -0.5          # ---- probe: interaction gain, negative sign ----
    p = m + 0.5 * g   # coef on |x10 + x11|
    q = m - 0.5 * g   # coef on |x10 - x11|
    bias -= 1.128 * (p + q)   # centre: E|a +/- b| ~ 1.128

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Units 0..9: linear pairs relu(x_f), relu(-x_f)
    feats = [i for i in range(12) if lin[i] != 0][:5]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        add_out(u, lin[f])
        add_out(v, -lin[f])

    # Units 10..13: pair block
    W1[10, a_idx] = 1.0;  W1[10, b_idx] = 1.0     # relu(a+b)
    W1[11, a_idx] = -1.0; W1[11, b_idx] = -1.0    # relu(-a-b)
    W1[12, a_idx] = 1.0;  W1[12, b_idx] = -1.0    # relu(a-b)
    W1[13, a_idx] = -1.0; W1[13, b_idx] = 1.0     # relu(b-a)
    add_out(10, p); add_out(11, p)                # p*|a+b|
    add_out(12, q); add_out(13, q)                # q*|a-b|
    # Units 14, 15 unused

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
