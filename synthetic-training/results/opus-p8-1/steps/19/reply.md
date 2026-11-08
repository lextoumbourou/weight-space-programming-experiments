## Step 19: group test for interactions among the "null" features

**What step 18 showed.** Adding 0.4·|x9| gave 0.520, matching the ~0.519 expected for no effect. So x9 has no symmetric effect, and I drop that term.

**What I'm doing now.** The single-feature symmetric effects found so far are all small. The likeliest remaining non-linearity is a pairwise interaction, such as an XOR-like product x_i·x_j. That would be invisible to every marginal probe I've run, and the features with no linear effect (x0, x2, x3, x5, x8, x10) are good candidates.

**How the group probe works.**

- I use T = |Σ c_i·x_i| / √6 over those six features. Since T² = (Σ x_i² + 2·Σ c_i·c_j·x_i·x_j) / 6, T responds to every pairwise product in the group, each with sign c_i·c_j, and to the squares.
- This step uses all c_i = +1. Later steps will use other sign patterns, and the differences between them will isolate which pairs matter.
- T needs two units, relu(z) and relu(−z), with z = Σ c_i·x_i / √6. The term added is s·(T − 0.798), with s = 0.7.

**The base.** I keep the scale-1 linear part plus 0.4·|x7|, which scored 0.513, and drop |x9|.

**How to read the result.** With no interaction effect, the loss should be about 0.532. A large move either way flags an interaction in this group.

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

    # ---- Kept: |x7| term (units 2,3) ----
    W1[2, 7] = 1.0
    W1[3, 7] = -1.0
    W2[1, 2] = 0.4
    W2[1, 3] = 0.4
    b2[1] -= 0.4 * 0.798

    # ---- Group interaction probe (units 4,5) ----
    # z = sum_i c_i x_i / sqrt(6) over the 'null' features; logit1 += s*(|z| - 0.798)
    group = [0, 2, 3, 5, 8, 10]
    c = [1, 1, 1, 1, 1, 1]          # sign pattern A (all +)
    s = 0.7
    for f, ci in zip(group, c):
        W1[4, f] = ci / np.sqrt(6.0)
        W1[5, f] = -ci / np.sqrt(6.0)
    W2[1, 4] = s
    W2[1, 5] = s
    b2[1] -= s * 0.798

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
