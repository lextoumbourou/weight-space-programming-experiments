## Step 19: probe |x4| on the calibrated linear model

**What step 18 showed**
- At scale 0.7 the loss fell to 0.506 and accuracy rose to 0.769.
- Fitting a parabola through the three scales (0.7, 1.0, 1.5) puts the best scale at about 0.71.
- So the purely linear model has reached about 0.506, and further gains must come from nonlinear terms or from re-weighting the features.

**This step**
- I keep the linear model at ±0.7 and add 0.5·|x4|, with the bias shifted by −0.5 × 0.80 to keep it centred.
- At this scale an irrelevant |x| term should change the loss by only about +0.01.
- Anything clearly larger, in either direction, means x4 acts asymmetrically or quadratically:
  - A drop in loss would mean large |x4| pushes towards class 1.
  - A clear rise would mean large |x4| pushes towards class 0, which I can then test with the opposite sign.

```python
import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    s = 0.7             # best overall scale found (0.7 < 1.0 < 1.5 in loss)
    lin[1] =  1.0 * s   # x1 positive
    lin[4] = -1.0 * s   # x4 negative
    lin[7] =  1.0 * s   # x7 positive
    lin[9] = -1.0 * s   # x9 negative

    # ---- probe: |x4| ----
    absc[4] = 0.5
    bias -= 0.798 * float(np.sum(absc))   # keep logits centred (E|x| ~ 0.798)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden-unit pairs per used feature: unit 2k = relu(x_f), unit 2k+1 = relu(-x_f)
    #   c*x  = c*relu(x) - c*relu(-x);   a*|x| = a*relu(x) + a*relu(-x)
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:8]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        cp = lin[f] + absc[f]
        cn = -lin[f] + absc[f]
        W2[1, u] = 0.5 * cp;  W2[0, u] = -0.5 * cp
        W2[1, v] = 0.5 * cn;  W2[0, v] = -0.5 * cn

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
