## Step 43: check overall calibration with a 0.9 scale

**What step 42 showed**
- Lowering x6's linear weight to −0.3 gave 0.4774, a new best.
- A parabola through the three linear-weight results (−0.3, −0.45 and −0.65) puts the optimum near −0.33.
- So −0.3 is close enough, and I keep it.

**This step**
- Since several terms were added after the last calibration check, I re-check the overall size of the logits.
- I multiply every linear and magnitude coefficient by 0.9. The bias keeps the class prior and is re-centred for the new magnitude weights.
- How to read the result:
  - A lower loss means the model is slightly over-confident.
  - A higher loss means I should try 1.1 or stay at 1.0.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Best configuration so far (step 42)
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative
    lin[6] = -0.3    # x6 negative (linear part)
    absc[10] = -0.5  # |x10| negative
    absc[11] = -0.5  # |x11| negative
    absc[6]  = -0.55 # |x6| negative

    # ---- probe: overall scale ----
    s = 0.9
    lin  *= s
    absc *= s

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
