## Step 38: drop the diffuse x1 probe and test x9 for interactions

**What step 37 showed.** The x1 × {x6, x11} probe accounts for only about −0.03 of the summed covariance. Combining steps 34–37, x1's interaction signal is spread out:

| Subgroup | Summed cov |
|---|---|
| {x0, x2, x3, x5} | about −0.04 |
| {x6, x11} | about −0.03 |
| {x8, x9, x10} | about −0.03 |

No single partner stands out, and each piece is near noise level.

**Why I drop it.** The full-group x1 probe has cov ≈ −0.019. That makes its best coefficient only about 0.26, worth roughly 0.0025. At s = −0.6 it actually cost a little compared with the base of about 0.453. So I remove it and free its four units.

**What I'm doing now.** I use those units to test x9, the third strongest linear feature, against the rest.

- Let g = (sum of all features except x1, x4, x7 and x9) / √8.
- The probe adds +0.6·½(|x9 + g| − |x9 − g|).

**How to read the result.**

- The base without the probe is about 0.453.
- With no effect, the probe's noise cost puts the loss at about 0.466.
- A clear move either way means x9 has an interaction.

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
    add_abs(4, 6, -0.3)    # |x6| negative
    add_abs(6, 11, -0.3)   # |x11| negative

    # ---- Product term via 4 units: logit1 += s * 0.5*(|u+v| - |u-v|) ~ s*u*v ----
    def add_product(unit, uvec, vvec, s):
        W1[unit, :] = uvec + vvec
        W1[unit + 1, :] = -(uvec + vvec)
        W1[unit + 2, :] = uvec - vvec
        W1[unit + 3, :] = -(uvec - vvec)
        W2[1, unit] = s / 2
        W2[1, unit + 1] = s / 2
        W2[1, unit + 2] = -s / 2
        W2[1, unit + 3] = -s / 2

    def e(f):
        v = np.zeros(12, dtype=np.float32)
        v[f] = 1.0
        return v

    # Confirmed interaction: x7 * x4 (negative)
    add_product(8, e(7), e(4), -0.8)

    # Probe: x9 * g, g = sum of features except 1, 4, 7, 9, normalised
    others = [f for f in range(12) if f not in (1, 4, 7, 9)]
    g = np.zeros(12, dtype=np.float32)
    for f in others:
        g[f] = 1.0 / np.sqrt(len(others))
    add_product(12, e(9), g, 0.6)

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
