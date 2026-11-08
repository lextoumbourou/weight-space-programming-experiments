## Step 24: keep the interaction unit and raise x10 to compensate

**What step 23 showed.** Adding the interaction unit (fires when x10 and x4 are both high, then lowers the class-1 logit) nudged the loss down to 0.4719, the best so far.
- Predicted positives fell sharply, from about 230 to 138.
- So the unit fires on many of the rows where x10 is high, and it now pushes many true positives below the threshold (113 false negatives).

**The hypothesis.** The interaction is real, but the rows where x10 is high and x4 is low are now under-predicted. Their logit only got the small step from 1.2 to 1.35 on x10.

**This step.**
- Keep the interaction unit at −1.5.
- Raise the x10 coefficient to 1.6, so the rows where x10 is high but the unit does not fire get a clearly higher class-1 logit.
- Leave everything else unchanged.

```python
import numpy as np
import math

def build_weights():
    # ---- linear part (units 0/1 carry w.x through ReLU pair) ----
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.6    # dominant positive feature (raised: interaction unit handles x10&x4 case)
    w[4]  = -0.3   # negative binary feature
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.2    # positive
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.7       # bias for class-1 logit

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    # ---- interaction unit: fires only when x10 high AND x4 high ----
    fc1_w[2, 10] = 1.0
    fc1_w[2, 4]  = 1.0
    fc1_b[2] = -1.5

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = w.x + b + v*h2 ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_w[1, 2] = -1.5    # penalty when both x10 and x4 are high
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
```
