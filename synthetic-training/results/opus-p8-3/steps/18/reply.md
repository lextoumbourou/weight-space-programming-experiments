## Step 18: probe an interaction between x1 and x7

**What step 17 showed**
- `+0.5·(|x1| − 0.8)` raised the loss by 0.019.
- The pure-noise part is about 0.009 (see x3), so about 0.01 is real: extreme x1 slightly favours class 0, a mild saturation.
- Fitting a parabola to these two numbers puts the optimal |x1| coefficient near −0.28, worth only about 0.003. That isn't worth a step now.

**What I'm testing now**
- Single-feature |x| effects look small, so I'm testing an interaction between the two strongest features, x1 and x7.
- The product proxy is `p = (|x1 + x7| − |x1 − x7|) / 2 = sign(x1·x7)·min(|x1|, |x7|)`.
- p is built from 4 ReLU units and has mean ≈ 0 for symmetric features, so it needs no bias correction.
- I add `+0.5·p` to the linear base.

**How to read the result**
- Pure noise should add about 0.008 to the loss.
- A drop means positive synergy between x1 and x7.
- A large rise means the interaction is negative.

```python
import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds
    GAIN = 1.0                     # overall scale on the linear direction

    # Linear direction from single-feature probes
    beta = np.array([
        0.0, 0.63, 0.10, 0.0, -0.49, 0.10,
        -0.24, 0.63, 0.0, -0.52, 0.0, 0.44,
    ], dtype=np.float32) * GAIN

    # Interaction probe between features A and B
    A, B = 1, 7
    INT_COEF = 0.5

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Units 0/1: linear part, relu(beta.x) - relu(-beta.x) = beta.x
    W1[0] = beta
    W1[1] = -beta
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Units 2/3: relu(xA+xB), relu(-(xA+xB))  -> sum = |xA+xB|
    W1[2, A], W1[2, B] = 1.0, 1.0
    W1[3, A], W1[3, B] = -1.0, -1.0
    # Units 4/5: relu(xA-xB), relu(-(xA-xB))  -> sum = |xA-xB|
    W1[4, A], W1[4, B] = 1.0, -1.0
    W1[5, A], W1[5, B] = -1.0, 1.0

    # logit diff += INT_COEF * (|xA+xB| - |xA-xB|) / 2
    c = INT_COEF / 2
    for u, s in [(2, 1.0), (3, 1.0), (4, -1.0), (5, -1.0)]:
        W2[1, u] = s * c / 2
        W2[0, u] = -s * c / 2

    # Output bias: class prior
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
