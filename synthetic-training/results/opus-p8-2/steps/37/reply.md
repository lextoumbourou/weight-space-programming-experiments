## Step 37: probe an x10·x11 interaction

**What step 36 showed**
- Raising x4 and x9 to −0.85 (with the magnitude terms at −0.4) gave 0.4868, slightly worse than the best of 0.4848.
- So I revert x4 and x9 to −0.7.
- The linear part is essentially optimised.

**Why test x10·x11**
- The small negative magnitude effects of x10 and x11 might really come from an interaction between them.
- A pure x10·x11 product would have looked like noise in every probe so far.

**How the network does it**
- I replace the two |x| pairs with four units on x10 and x11: ReLU(±(x10+x11)) and ReLU(±(x10−x11)).
- These units give |x10+x11| and |x10−x11| separately, and both terms can be built from them:
  - The magnitude part: since |a+b| + |a−b| = 2·max(|a|,|b|), giving each a weight of −0.2 approximates the old −0.4·(|x10|+|x11|).
  - The interaction part: g/2·(|a+b| − |a−b|) acts like a bounded product of x10 and x11, as in step 22.
- I use g = +0.5, so the weights are +0.05 on |x10+x11| and −0.45 on |x10−x11|.
- The bias is re-centred using E|a±b| ≈ 1.128.

**How to read the result**
- A clear drop below about 0.485 means x10 and x11 having the same sign pushes towards class 1.
- A clear rise means the opposite sign. In that case I will try g = −0.5.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i
    #         + p*|x10 + x11| + q*|x10 - x11|      (pair block on x10, x11)
    #   with p = m + g/2, q = m - g/2:
    #     m*(|a+b|+|a-b|) = 2m*max(|a|,|b|)   -> magnitude effect (m=-0.2 ~ old -0.4 per |x|)
    #     g/2*(|a+b|-|a-b|) = g*sign(ab)*min(|a|,|b|) -> interaction x10*x11
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
    m = -0.2          # magnitude part
    g = 0.5           # ---- probe: interaction gain ----
    p = m + 0.5 * g   # coef on |x10 + x11|
    q = m - 0.5 * g   # coef on |x10 - x11|
    # centre: E|a +/- b| = 0.798*sqrt(2) ~ 1.128
    bias -= 1.128 * (p + q)

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
