## Step 17: individual |x| probe on x7

**What step 16 showed.** The loss was 0.549, against about 0.536 expected for no effect. So the linear features have, in total, a mild negative symmetric effect: larger |x| leans slightly towards class 0. That could mean saturating or asymmetric (one-sided) responses in some of them. The total effect is modest, so I'll locate it one feature at a time, starting with the strongest feature, x7.

**What I'm doing now.**

- The base is the scale-1 linear part, which scored 0.516.
- I add 0.4·(|x7| − 0.798) to the class-1 logit.

**How to read the result.**

- With no symmetric effect, the loss should be about 0.516 + 0.006 ≈ 0.522.
- Above that means a negative symmetric effect in x7. That would suggest its response flattens or bends at the extremes.
- Below that means the opposite.

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

    # ---- |x| probe on a single feature (units 2,3) ----
    s = 0.4
    f = 7
    W1[2, f] = 1.0     # relu(x_f)
    W1[3, f] = -1.0    # relu(-x_f)
    W2[1, 2] = s
    W2[1, 3] = s       # logit1 += s*|x_f|
    b2[1] -= s * 0.798 # centre: subtract s*E|x|

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
