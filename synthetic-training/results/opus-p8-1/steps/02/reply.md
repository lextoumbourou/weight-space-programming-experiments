## Step 2: probing x1, with the class prior added

**What step 1 showed.**

- **Class balance:** the true counts are 605 class 0 and 395 class 1. The best constant bias on the class-1 logit is therefore ln(395/605) ≈ −0.43.
- **x0:** with no bias, a useless feature at strength 0.5 would give a loss of about 0.693 + 0.25/8 ≈ 0.724. The observed 0.733 is close to that, and accuracy is at chance. So x0 looks weak or irrelevant, at least linearly. It may be slightly negative.

**What I'm doing now.** I add the prior bias, which alone gives a loss of about 0.671. Then I probe x1 with weight 0.5.

**How to read the result.**

- If x1 is useless, the loss should be about 0.671 + 0.5·0.25·0.239 ≈ 0.701.
- Clearly lower means x1 is positively related to class 1.
- Clearly higher means it is negatively related.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    probe = 1   # feature being probed this step
    s = 0.5     # probe strength

    # Hidden unit 0 = relu(x_probe), hidden unit 1 = relu(-x_probe)
    W1[0, probe] = 1.0
    W1[1, probe] = -1.0

    # Class-1 logit += s*(h0 - h1) = s*x_probe
    W2[1, 0] = s
    W2[1, 1] = -s

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
