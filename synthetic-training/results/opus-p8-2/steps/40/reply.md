## Step 40: push |x6| further

**What step 39 showed**
- Adding −0.5·|x6| lowered the loss to 0.4783, a new best and about 0.007 better than before.

**How x6 acts**
- Combined with the linear −0.45·x6, x6 now acts almost one-sidedly.
- For positive values its weight is −0.95.
- For negative values its weight is about +0.05.
- So x6 mainly matters when it is large and positive, which then pushes towards class 0.

**This step**
- I strengthen the magnitude term to −0.8·|x6|.
- The weights become about −1.25 for positive x6 and +0.35 for negative x6.
- A loss below 0.4783 means the term wants to be stronger.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Main linear features
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative
    lin[6] = -0.45   # x6 negative

    # Negative magnitude terms
    absc[10] = -0.5
    absc[11] = -0.5
    absc[6]  = -0.8  # ---- probe: stronger |x6| (-0.5 helped) ----

    bias -= 0.798 * float(np.sum(absc))   # keep logits centred (E|x| ~ 0.798)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Per-feature pairs relu(x_f), relu(-x_f): 7 features -> units 0..13
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:8]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        add_out(u, lin[f] + absc[f])
        add_out(v, -lin[f] + absc[f])

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
