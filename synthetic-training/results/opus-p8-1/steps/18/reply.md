## Step 18: keep the |x7| term, probe |x9|

**What step 17 showed.** Adding 0.4·|x7| lowered the loss to 0.513, a new best, against about 0.522 expected for no effect. So x7 has a small positive symmetric effect, with cov ≈ +0.02. I keep it.

The group result from step 16 therefore implies the other five linear features together carry a negative symmetric effect of about −0.07.

**What I'm doing now.**

- The base is the scale-1 linear part plus 0.4·|x7|, centred, which scored 0.513.
- I add a probe of 0.4·(|x9| − 0.798).

**How to read the result.** With no effect, the loss should be about 0.519. Above that means x9 has a negative symmetric effect.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear part (units 0,1): logit1 += scale * w.x ----
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.5    # x1 positive
    w[4] = -0.5   # x4 negative
    w[6] = -0.5   # x6 negative
    w[7] = 0.5    # x7 positive (strong)
    w[9] = -0.5   # x9 negative (strong)
    w[11] = 0.5   # x11 positive (mild)
    scale = 1.0
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = scale
    W2[1, 1] = -scale

    # ---- |x| terms: units (u, u+1) = relu(x_f), relu(-x_f), both weighted s ----
    def add_abs(u, f, s):
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798   # centre using E|x| = 0.798

    add_abs(2, 7, 0.4)   # kept: |x7| slightly positive
    add_abs(4, 9, 0.4)   # probe: |x9|

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
