## Step 26: strengthen the weak features

**What step 25 showed**
- Adding x11 (+0.3), x5 (+0.25) and x6 (−0.25) lowered the loss to 0.498, a new best.
- So at least some of these weak signals are real.

**This step**
- I increase all three together to see whether they want more weight:
  - x11 to +0.5;
  - x5 to +0.4;
  - x6 to −0.4.
- How to read the result:
  - A further drop means I should keep pushing.
  - A rise means the step-25 values are near optimal, and I will tune each one separately.

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

    # Weak features (step 25 helped at 0.3/0.25/-0.25) -- probe larger
    lin[11] =  0.5   # x11 positive
    lin[5]  =  0.4   # x5 positive
    lin[6]  = -0.4   # x6 negative

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
