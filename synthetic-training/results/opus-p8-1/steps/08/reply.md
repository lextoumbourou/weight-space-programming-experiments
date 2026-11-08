## Step 8: probe −0.5·x6 to pin down the baseline

**What step 7 showed.** The loss was 0.664, above the ~0.637 expected for a useless x6, so x6 looks negative. The trouble is that my baseline is only an estimate.

**Why mirror the probe.**

- Steps 6 and 7 together say only that x5's covariance with the label minus x6's is about 0.084. They can't tell whether that comes from x5, from x6, or from both.
- Running the same probe with the opposite sign gives the base loss plus the probe's curvature cost on its own: it is the average of the two runs.
- Half the difference between the two runs, divided by the strength 0.5, gives cov(x6, y) precisely.
- This gives a reliable reference point for judging the earlier probes, including x5.

**What I'm doing now.** The base is the prior bias plus 0.5·x1 − 0.5·x4, and I add −0.5·x6.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    def add_linear(unit, feat, s):
        # Units (unit, unit+1) = relu(x), relu(-x); class-1 logit += s*x
        W1[unit, feat] = 1.0
        W1[unit + 1, feat] = -1.0
        W2[1, unit] = s
        W2[1, unit + 1] = -s

    add_linear(0, 1, 0.5)    # confirmed: x1 positive
    add_linear(2, 4, -0.5)   # confirmed: x4 negative
    add_linear(4, 6, -0.5)   # mirrored probe: x6 with negative sign

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
