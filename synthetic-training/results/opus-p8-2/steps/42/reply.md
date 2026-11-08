## Step 42: try a smaller linear weight on x6

**What step 41 showed**
- Raising x6's linear weight to −0.65 made the loss worse: 0.4842, against 0.4783 at −0.45.
- That is a clear rise of about 0.006, so the best linear weight is −0.45 or smaller.

**This step**
- I try a linear weight of −0.3 on x6, keeping |x6| at −0.55.
- This gives about −0.85 for positive x6 and +0.25 for negative x6, so x6 acts more like a pure magnitude term.
- How to read the result, against 0.4783:
  - A lower loss means the smaller linear weight is better.
  - A higher loss means about −0.45 is the best value.

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
    lin[6] = -0.3    # x6 negative  <-- probe: lowered (-0.65 was worse than -0.45)

    # Negative magnitude terms
    absc[10] = -0.5
    absc[11] = -0.5
    absc[6]  = -0.55

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
