## Step 27: push the convexity of the linear score further

**What step 26 showed.** Making the positive slope steeper than the negative one helped: loss 0.4799, a new best.

**Estimating the best size.** I write the added term as c·|z|, where c = (a₊ − a₋)/2 and c = 0.2 in step 26.

- The variance of |z| is 0.363·σ_z² ≈ 0.75, so c = 0.2 had a noise cost of only about 0.003.
- So the real signal was about 0.007, which means cov(|z|, y) ≈ 0.036.
- The best coefficient is then about 0.036 / (0.75 × 0.2) ≈ 0.24.

**What I'm doing now.** I try c = 0.3, with a₊ = 1.35 and a₋ = 0.75, to bracket that estimate from above. Everything else is unchanged.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear score z = w.x (units 0,1 = relu(z), relu(-z)) ----
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

    # Asymmetric slopes: logit1 += a_pos*relu(z) - a_neg*relu(-z)
    #   = 1.05*z + ((a_pos - a_neg)/2)*|z|
    a_pos, a_neg = 1.35, 0.75
    W2[1, 0] = a_pos
    W2[1, 1] = -a_neg
    sigma_z = float(np.sqrt(np.sum(w.astype(np.float64) ** 2)))
    b2[1] -= 0.5 * (a_pos - a_neg) * 0.798 * sigma_z   # centre the |z| part

    # ---- |x| terms: units (u,u+1) = relu(x_f), relu(-x_f), both weighted s ----
    def add_abs(u, f, s):
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798   # centre using E|x| = 0.798

    add_abs(2, 7, 0.4)     # |x7| positive
    add_abs(4, 1, -0.3)    # |x1| negative
    add_abs(6, 4, -0.3)    # |x4| negative
    add_abs(8, 6, -0.3)    # |x6| negative
    add_abs(10, 11, -0.3)  # |x11| negative

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
