## Step 22: probe the interaction x1·x7

**What step 21 showed**
- Adding 0.5·|x9| raised the loss by +0.011, from 0.506 to 0.517.
- At most it hints that large |x9| pushes slightly towards class 0. I leave it out.
- No useful |x| terms were found on the four relevant features.

**Plan from here**
- Pairwise interactions are the next likely form of nonlinearity.

**How the network does it**
- I use the identity (|a+b| − |a−b|)/2 = sign(ab)·min(|a|,|b|).
- This acts like a bounded product: it is zero on average and positive when a and b have the same sign.
- It needs four hidden units:
  - ReLU(a+b) and ReLU(−a−b), whose sum is |a+b|;
  - ReLU(a−b) and ReLU(b−a), whose sum is |a−b|.
- I rewrote the builder around a generic list of interaction terms, using units 8 to 15.

**This step**
- I keep the best linear model and add 0.5·sign(x1·x7)·min(|x1|,|x7|).
- How to read the result:
  - A drop in loss means x1 and x7 having the same sign pushes towards class 1.
  - A rise of more than about 0.02 means the opposite sign.
  - Little change means no interaction.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    #         + sum_(i,j,g) g * (|x_i + x_j| - |x_i - x_j|) / 2      (interaction terms)
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    s = 0.7             # best overall scale found
    lin[1] =  1.0 * s   # x1 positive
    lin[4] = -1.0 * s   # x4 negative
    lin[7] =  1.0 * s   # x7 positive
    lin[9] = -1.0 * s   # x9 negative

    # ---- probe: interaction x1*x7 (sign-product style) ----
    inter = [(1, 7, 0.5)]   # (i, j, gain)

    bias -= 0.798 * float(np.sum(absc))   # centring for |x| terms (none now)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        # add coef to the logit gap via this unit (split over the two logits)
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Units 0..7: per-feature pairs relu(x_f), relu(-x_f) for linear / |x| terms
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:4]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        add_out(u, lin[f] + absc[f])
        add_out(v, -lin[f] + absc[f])

    # Units 8..15: interaction terms, 4 units each (max 2)
    for n, (i, j, g) in enumerate(inter[:2]):
        base = 8 + 4 * n
        W1[base + 0, i] = 1.0;  W1[base + 0, j] = 1.0    # relu(xi+xj)
        W1[base + 1, i] = -1.0; W1[base + 1, j] = -1.0   # relu(-xi-xj)
        W1[base + 2, i] = 1.0;  W1[base + 2, j] = -1.0   # relu(xi-xj)
        W1[base + 3, i] = -1.0; W1[base + 3, j] = 1.0    # relu(xj-xi)
        # g/2 * (|xi+xj| - |xi-xj|)
        add_out(base + 0, 0.5 * g)
        add_out(base + 1, 0.5 * g)
        add_out(base + 2, -0.5 * g)
        add_out(base + 3, -0.5 * g)

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
