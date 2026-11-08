## Step 24: narrow down which |x| terms help

**What step 23 showed.** Adding −0.3·|x| for x1, x4, x6 and x11 gave a new best: loss 0.484 and accuracy 0.777. Without a real effect, the loss would have risen to about 0.506, so the combined signal is roughly −0.07, as estimated.

**What I'm doing now.** I need to know whether the effect is spread across all four features or sits in a few, so I bisect the group.

- I keep −0.3·|x1| and −0.3·|x4|.
- I remove the |x6| and |x11| terms.
- Removing two terms saves about 0.0065 of noise cost.

**How to read the result.**

- If the loss goes below 0.484, x6 and x11 weren't helping.
- If it goes clearly above 0.484, they carry real signal and should go back in, possibly stronger.

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
    add_abs(4, 1, -0.3)    # |x1| negative
    add_abs(6, 4, -0.3)    # |x4| negative
    # bisection: |x6| and |x11| removed this step

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
