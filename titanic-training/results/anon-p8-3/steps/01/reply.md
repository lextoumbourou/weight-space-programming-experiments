## Step 1: probe feature x0

I can't see the data, so I'll first find out which features predict the class and in which direction. Each probe step uses a model that depends on one feature only:

- **Hidden units:** unit 0 = ReLU(x_k) and unit 1 = ReLU(−x_k). Their difference is exactly x_k, because ReLU(z) − ReLU(−z) = z.
- **Output:** logit1 − logit0 = a·x_k + b.
- **Bias b:** b = log(prior odds). I guess a class split of about 38% class 1 to 62% class 0, so b ≈ −0.47.
- **Reference point:** with a = 0, the model predicts the prior alone, and the loss would be about 0.666.

How I'll read the result for this step (k = 0, a = +1):

- If the loss is well below 0.666, x0 is positively associated with class 1.
- If the loss is well above 0.666, the association is probably negative.
- The confusion matrix will help confirm the direction.

All other weights are zero.

```python
import numpy as np

def build_weights():
    # ---- probe configuration ----
    FEATURE = 0        # which input feature is being probed this step
    A = 1.0            # coefficient: logit difference (class1 - class0) = A * x_FEATURE + B
    B = -0.47          # log prior odds guess for class 1 (~38% positives)

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden unit 0 = relu(+x_k), hidden unit 1 = relu(-x_k); difference = x_k
    W1[0, FEATURE] = 1.0
    W1[1, FEATURE] = -1.0

    # split the coefficient symmetrically across the two logits
    W2[1, 0] = A / 2;  W2[1, 1] = -A / 2     # class 1 logit gets +A/2 * x_k
    W2[0, 0] = -A / 2; W2[0, 1] = A / 2      # class 0 logit gets -A/2 * x_k

    # prior bias
    b2[1] = B / 2
    b2[0] = -B / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
