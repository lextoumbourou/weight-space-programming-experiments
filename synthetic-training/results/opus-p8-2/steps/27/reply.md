## Step 27: remove x6 to isolate its effect

**What step 26 showed**
- Strengthening all three weak features made the loss worse: 0.511, against 0.498 at the step-25 values.
- So either some of them are too strong, or one of them does not belong at all.
- x6 was the least certain: its +0.155 rise in step 8 could also have been noise.

**This step**
- I return to the step-25 settings, but drop x6.
- The model is now:
  - x1 at +0.85, x4 at −0.7, x7 at +0.85, x9 at −0.7;
  - x11 at +0.3 and x5 at +0.25;
  - the prior bias.
- How to read the result:
  - A loss below 0.498 means x6 was hurting.
  - A loss above 0.498 means x6 at −0.25 was helping.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    #         + sum_(i,j,g) g * (|x_i + x_j| - |x_i - x_j|) / 2
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Main features
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative

    # Weak features: back to step-25 values, x6 removed (probe)
    lin[11] =  0.3   # x11 positive
    lin[5]  =  0.25  # x5 positive
    lin[6]  =  0.0   # x6 removed for this probe

    inter = []       # no interaction terms

    bias -= 0.798 * float(np.sum(absc))   # centring for |x| terms (none now)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Per-feature pairs relu(x_f), relu(-x_f): up to 7 features -> units 0..13
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:7]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        add_out(u, lin[f] + absc[f])
        add_out(v, -lin[f] + absc[f])

    # Interaction terms use 4 units each from the remaining units (none now)
    nxt = 2 * len(feats)
    for (i, j, g) in inter:
        if nxt + 4 > 16:
            break
        W1[nxt + 0, i] = 1.0;  W1[nxt + 0, j] = 1.0
        W1[nxt + 1, i] = -1.0; W1[nxt + 1, j] = -1.0
        W1[nxt + 2, i] = 1.0;  W1[nxt + 2, j] = -1.0
        W1[nxt + 3, i] = -1.0; W1[nxt + 3, j] = 1.0
        add_out(nxt + 0, 0.5 * g)
        add_out(nxt + 1, 0.5 * g)
        add_out(nxt + 2, -0.5 * g)
        add_out(nxt + 3, -0.5 * g)
        nxt += 4

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
