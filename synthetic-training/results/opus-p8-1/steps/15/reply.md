## Step 15: group probe for |x| effects in the "linear-null" features

**What step 14 showed.** Scaling the linear part by 1.4 made the loss worse, 0.524 against 0.516. I fitted a quadratic in the scale through three points: zero weights (about 0.671), scale 1 and scale 1.4. Its optimum is a scale of about 1.1, where the loss would be only about 0.514.

So the linear part is close to as good as it gets. The remaining signal must be non-linear.

**What I'm doing now.**

- I keep the linear part at scale 1, which scored 0.516, in units 0 and 1.
- I test a symmetric (|x|-shaped) effect in the six features that showed no clear linear effect: x0, x2, x3, x5, x8 and x10.
- Each feature gets two units, relu(x) and relu(−x). Both feed the class-1 logit with weight +0.3, so the pair adds 0.3·|x|.
- I subtract 0.3·0.798 per feature in the output bias. That keeps the average logit unchanged, because the mean of |x| for a standard normal is 0.798.

**How to read the result.**

- If none of these features has a symmetric effect, the loss should rise slightly, to about 0.536.
- A clear drop or a clear jump means some of them have a symmetric (|x|- or x²-like) effect. A drop means larger |x| favours class 1; a jump means the opposite.
- I'll then split the group in half to narrow it down.

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

    # ---- Group |x| probe (units 2..13) ----
    # For each feature f: units relu(x_f), relu(-x_f), both weighted +s
    # -> logit1 += s*|x_f|; subtract s*E|x| (=0.798) in the bias to keep it centred.
    s = 0.3
    group = [0, 2, 3, 5, 8, 10]
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
