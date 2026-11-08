## Step 16: group |x| probe on the linear features

**What step 15 showed.** The loss was 0.520, against about 0.536 expected for no effect. That is a small net positive. The six features may have a weak symmetric effect overall, or larger effects that cancel each other out. Neither case gives a strong lead, so I'll come back to this group if needed.

**What I'm doing now.** I run the same symmetric test on the features that do have linear effects: x1, x4, x6, x7, x9 and x11.

- The base is the scale-1 linear part, which scored 0.516.
- Each of the six features adds 0.3·(|x| − 0.798) to the class-1 logit.

**How to read the result.** If there is no symmetric effect, the loss should be about 0.536.

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

    # ---- Group |x| probe on the linear features (units 2..13) ----
    # Each feature f: relu(x_f) and relu(-x_f) both weighted +s -> logit1 += s*|x_f|,
    # centred by subtracting s*0.798 from the bias.
    s = 0.3
    group = [1, 4, 6, 7, 9, 11]
    u = 2
    for f in group:
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798
        u += 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
