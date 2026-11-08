## Step 45: use the fitted scale and nudge the bias towards class 1

**What step 44 showed**
- Scale 1.1 gave 0.4769, slightly better than 0.4774 at scale 1.0.
- A parabola through the three scales (0.9, 1.0 and 1.1) puts the best scale at about 1.07.
- I set the scale to 1.07.

**Is the bias right?**
- The bias has always been the plain class prior, re-centred with E|x| ≈ 0.798.
- Since the |x| terms are nonlinear, that centring may be slightly off.
- The confusion matrix shows 377 rows predicted as class 1, against 395 true class-1 rows.
- So the model predicts class 1 slightly less often than it occurs.

**This step**
- I add +0.1 to the logit-gap bias.
- How to read the result:
  - A lower loss means I keep the shift.
  - A higher loss means I will test −0.1 next.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Best configuration (step 42), before scaling
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative
    lin[6] = -0.3    # x6 negative (linear part)
    absc[10] = -0.5  # |x10| negative
    absc[11] = -0.5  # |x11| negative
    absc[6]  = -0.55 # |x6| negative

    # Overall scale: parabola fit over 0.9 / 1.0 / 1.1 -> ~1.07
    s = 1.07
    lin  *= s
    absc *= s

    bias -= 0.798 * float(np.sum(absc))   # keep logits centred (E|x| ~ 0.798)

    # ---- probe: bias shift towards class 1 ----
    bias += 0.1

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
