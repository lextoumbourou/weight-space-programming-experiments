## Step 39: drop the interaction and probe |x6|

**What step 38 showed**
- Both signs of the x10·x11 interaction made the loss worse: 0.4935 at g = +0.5 and 0.4977 at g = −0.5.
- So there is no interaction between x10 and x11, and their effect is a plain magnitude effect.

**This step**
- I return to the step-33 model, which scored 0.4851:
  - x1 at +0.85, x4 at −0.7, x7 at +0.85, x9 at −0.7, x6 at −0.45;
  - −0.5 on |x10| and |x11|.
- I probe |x6|, the only magnitude term not yet tested.
- I give it −0.5, following the negative pattern of |x10| and |x11|.
- This uses all 16 hidden units.
- How to read the result:
  - A null term should cost only about +0.002.
  - A clear drop means |x6| matters with negative sign.
  - A clear rise means it matters with positive sign.

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
    lin[6] = -0.45   # x6 negative

    # Negative magnitude terms (best config, step 33)
    absc[10] = -0.5
    absc[11] = -0.5

    # ---- probe: |x6| ----
    absc[6] = -0.5

    bias -= 0.798 * float(np.sum(absc))   # keep logits centred (E|x| ~ 0.798)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Per-feature pairs relu(x_f), relu(-x_f): 7 features -> units 0..13
    #   lin*x = lin*relu(x) - lin*relu(-x);  a*|x| = a*relu(x) + a*relu(-x)
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
