## Step 20: re-weight the linear part by estimated feature strength

**What step 19 showed.** The loss was 0.523, against about 0.532 expected for no effect. That is a small positive, most likely from the weak symmetric effects already seen in step 15. There is no sign of a strong interaction among the null features.

**What I'm doing now.** So far every linear feature has had the same weight, 0.5. But the covariances I estimated for each feature differ quite a lot:

| Feature | Estimated cov with label |
|---|---|
| x7 | +0.15 |
| x1 | +0.13 |
| x9 | −0.13 |
| x4 | −0.115 |
| x6 | −0.066 |
| x11 | +0.04 |
| x5 | +0.02 |
| x2 | +0.02 |

With roughly independent features, the best logistic direction is roughly proportional to these covariances. I set w_i = k·cov_i, with k chosen so the average size matches the best equal-weight scale (about 1.1 × 0.5).

**New linear weights:** x7 0.78, x1 0.68, x9 −0.67, x4 −0.60, x6 −0.34, x11 0.21, x5 0.10, x2 0.10.

**Unchanged:** the 0.4·|x7| term stays in, and the interaction probe is removed. Base to compare against: 0.513.

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
    # Weights proportional to estimated covariance with the label.
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

    # ---- Kept: |x7| term (units 2,3): logit1 += 0.4*(|x7| - 0.798) ----
    W1[2, 7] = 1.0
    W1[3, 7] = -1.0
    W2[1, 2] = 0.4
    W2[1, 3] = 0.4
    b2[1] -= 0.4 * 0.798

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
