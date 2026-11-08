## Step 28: test whether the label behaves like an AND of conditions

**What step 27 showed.** c = 0.3 gave 0.4792, slightly better again. A quadratic fit through c = 0, 0.2 and 0.3 puts the optimum at c ≈ 0.33, so I keep 0.3.

**What the learned shapes suggest.** Look at the slope each feature has on its positive and negative sides:

| Feature | Steeper side | Pushes towards |
|---|---|---|
| x1 | negative (low x1) | class 0 |
| x4 | positive (high x4) | class 0 |
| x6 | positive (high x6) | class 0 |
| x11 | negative (low x11) | class 0 |
| x7 | positive (high x7) | class 1 |

So most features matter most when they point towards class 0. That is what an AND-like rule produces, something like "class 1 only if x1 is not low and x4 is not high and …". For such a rule the logit behaves like the minimum of per-feature margins m_i.

**How I test it.** Writing the minimum as min(m_a, m_b) = (m_a + m_b)/2 − |m_a − m_b|/2 suggests adding −s·|m_a − m_b| terms.

- With m₁ = x1 and m₄ = −x4, the pair term is −s·|x1 + x4|.
- With m₇ = x7 and m₉ = −x9, it is −s·|x7 + x9|.
- I use s = 0.2. Each term is centred with E|a+b| ≈ 1.128.
- These use the four free units, 12–15.

**How to read the result.** The noise cost is about 0.006, so with no effect I'd expect about 0.485. Anything clearly below 0.4792 supports the AND idea.

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

    # ---- 'min'-style pair terms: logit1 += s*(|x_a + x_b| - 1.128) ----
    def add_abs_sum(u, a, b, s):
        W1[u, a] = 1.0;  W1[u, b] = 1.0
        W1[u + 1, a] = -1.0; W1[u + 1, b] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798 * np.sqrt(2.0)

    add_abs_sum(12, 1, 4, -0.2)   # probe: -|x1 + x4|  (min of margins x1, -x4)
    add_abs_sum(14, 7, 9, -0.2)   # probe: -|x7 + x9|  (min of margins x7, -x9)

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
