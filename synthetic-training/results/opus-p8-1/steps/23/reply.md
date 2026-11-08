## Step 23: add the negative |x| effect from the other linear features

**What step 22 showed.** The loss was 0.517, against about 0.510 expected for no effect. So the three product terms add up to a slightly negative effect overall, with a total cov of only about −0.03. There are no meaningful interactions among x1, x7 and x9. Testing every remaining pair would use most of my steps, so I'll use the signals I already have instead.

**What I'm doing now.** Step 16 showed that the linear features together have a negative symmetric effect. Step 17 then showed x7's share is positive (about +0.02) and step 18 that x9's is zero. So the remaining features, x1, x4, x6 and x11, together carry about −0.07.

I add −0.3·(|x_f| − 0.798) for each of these four, keeping the |x7| term as well.

**How to read the result.** The base is 0.493.

- If the estimate is right, the loss should drop below 0.493, to roughly 0.486.
- If these features have no symmetric effect, it would rise to about 0.506.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear part (units 0,1): logit1 += w.x ----
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.68    # x1
    w[2] = 0.10    # x2 (weak)
    w[4] = -0.60   # x4
    w[5] = 0.10    # x5 (weak)
    w[6] = -0.34   # x6
    w[7] = 0.78    # x7 (strongest)
    w[9] = -0.67   # x9
    w[11] = 0.21   # x11
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0

    # ---- |x| terms: units (u,u+1) = relu(x_f), relu(-x_f), both weighted s ----
    def add_abs(u, f, s):
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798   # centre using E|x| = 0.798

    add_abs(2, 7, 0.4)     # kept: |x7| slightly positive
    add_abs(4, 1, -0.3)    # probe: |x1| negative
    add_abs(6, 4, -0.3)    # probe: |x4| negative
    add_abs(8, 6, -0.3)    # probe: |x6| negative
    add_abs(10, 11, -0.3)  # probe: |x11| negative

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
