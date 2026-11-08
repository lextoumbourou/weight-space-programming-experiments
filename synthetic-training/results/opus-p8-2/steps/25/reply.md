## Step 25: add the three weak candidate features together

**What step 24 showed**
- Raising x7 to 1.0 also left the loss essentially unchanged, at 0.507.
- The four main weights are near optimal at roughly equal size, around 0.7 to 0.85.

**This step**
- I add the weak hints from the earlier linear probes, all at small weights, in a single test.
- The three candidates, and what their earlier loss increases suggested:
  - x11: added +0.058 against an expected +0.1, so it may be positive. I give it +0.3.
  - x5: added +0.076, so it may be weakly positive. I give it +0.25.
  - x6: added +0.155, so it may be weakly negative. I give it −0.25.
- If the loss improves, I will keep them and then separate their effects.
- The builder now allows up to 7 linear features, using units 0 to 13.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    #         + sum_(i,j,g) g * (|x_i + x_j| - |x_i - x_j|) / 2
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    # Main features (weights roughly optimal, loss surface flat here)
    lin[1] =  0.85   # x1 positive
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.85   # x7 positive
    lin[9] = -0.7    # x9 negative

    # ---- probe: weak candidates together ----
    lin[11] =  0.3   # x11 weakly positive?
    lin[5]  =  0.25  # x5 weakly positive?
    lin[6]  = -0.25  # x6 weakly negative?

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
