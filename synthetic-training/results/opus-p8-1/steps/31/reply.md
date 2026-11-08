## Step 31: narrow the x7 interaction within group A

**What step 30 showed.** The negative x7 × A probe gave 0.4772, a new best, against about 0.492 expected for no effect.

- That implies the sum of cov(x7·x_j, y) over A = {x0, x2, x3, x4, x5} is about −0.10.
- So group A holds nearly all of the −0.12 found in step 29.

**What I'm doing now.** I split A further and test x7 against {x3, x4, x5}.

- Let g = (x3 + x4 + x5) / √3.
- The probe adds −0.6·½(|x7 + g| − |x7 − g|).

**How to read the result.**

- With no interaction in this subgroup, the loss should be about 0.492.
- If the cov ≈ −0.1 pair is in here, the gain is larger than in step 30 because the dilution is smaller. The loss should then reach about 0.472.
- If the loss comes out near 0.49, the pair is in {x0, x2}.

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

    # ---- Group interaction probe: x7 * g, g = sum(group)/sqrt(|group|) ----
    # logit1 += s * 0.5*(|x7 + g| - |x7 - g|)   with s negative
    s = -0.6
    group = [3, 4, 5]
    gv = np.zeros(12, dtype=np.float32)
    for f in group:
        gv[f] = 1.0 / np.sqrt(len(group))
    e7 = np.zeros(12, dtype=np.float32)
    e7[7] = 1.0
    W1[12, :] = e7 + gv
    W1[13, :] = -(e7 + gv)
    W1[14, :] = e7 - gv
    W1[15, :] = -(e7 - gv)
    W2[1, 12] = s / 2
    W2[1, 13] = s / 2
    W2[1, 14] = -s / 2
    W2[1, 15] = -s / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
