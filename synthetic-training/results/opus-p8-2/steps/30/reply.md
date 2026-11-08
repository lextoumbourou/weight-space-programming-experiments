## Step 30: set x6 to its fitted weight and probe |x2|, |x3| and |x8| together

**Best weight for x6**
- Three results so far:
  - x6 at 0: about 0.507;
  - x6 at −0.35: 0.4901;
  - x6 at −0.55: 0.4909.
- A parabola through these puts the optimum near −0.45, so I set x6 to −0.45.
- That change alone should shift the loss by only about −0.001.

**Probing nonlinear terms in several features at once**
- An irrelevant 0.5·|x| term costs only about +0.004, as seen with |x4| and |x7|.
- So I can probe three features together using the six free hidden units: |x2|, |x3| and |x8|, each at +0.5.
- The bias is shifted to keep the logits centred.
- How to read the result, against 0.490:
  - A clear drop means at least one of them matters, with large values pushing towards class 1.
  - A clear rise means at least one matters with the opposite sign.
  - About +0.01 means none of them matter.

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
    lin[6] = -0.45   # x6 negative (parabola fit over 0, -0.35, -0.55)

    # ---- probe: |x2|, |x3|, |x8| jointly ----
    absc[2] = 0.5
    absc[3] = 0.5
    absc[8] = 0.5

    inter = []       # no interaction terms

    bias -= 0.798 * float(np.sum(absc))   # keep logits centred (E|x| ~ 0.798)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Per-feature pairs relu(x_f), relu(-x_f): up to 8 features -> units 0..15
    #   lin*x = lin*relu(x) - lin*relu(-x);  a*|x| = a*relu(x) + a*relu(-x)
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:8]
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
