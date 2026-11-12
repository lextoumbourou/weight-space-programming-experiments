## Step 17: a measurement step to find out how large the features really are

**Why measure:** step 16 showed that raising β from 0.04 to 0.06 hurt, and it hit 8 hardest. The absence penalty −β·s·ΣT_d assumes a present feature is worth about s = 1.5. If real features are smaller, the penalty is too strong for classes with large templates such as 8. I can't see feature values directly, but I can read them off the confusion matrix.

**What this step does:** it is a deliberate probe, and its loss will be poor. It costs nothing in the final score, because only the step with the lowest training loss is kept.
- The fc layer computes the total feature mass S = Σ f over all 256 features.
- It sets logit_k = a·(k·S − Σ_{j≤k} t_j). Because these are lines of increasing slope, the argmax is the number of thresholds t_j that S exceeds.
- The thresholds are 20, 30, 40, 50, 60, 70, 85, 100 and 120.
- So "predicted column k" means S fell in bin k, and each row of the confusion matrix is a histogram of S for that true digit.

**How I will use it:** comparing S for each digit with that digit's template mass ΣT_d gives a calibrated feature scale s per digit. That replaces the guess s = 1.5. The conv1 and conv2 layers are exactly as in steps 15 and 16.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors (unchanged) ----------------
    alphas = [k * 45.0 for k in range(8)]
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    for k, al in enumerate(alphas):
        a = math.radians(al)
        gx, gy = math.cos(a), math.sin(a)
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                t = dx * gx + dy * gy
                s = -dx * gy + dy * gx
                w[r, c] = t * math.exp(-t * t / 2.0) * math.exp(-s * s / (2 * 1.5 ** 2))
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15

    # ---------------- conv2: two grids of the 8 edge maps (unchanged) ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(8):
        W2[j, j, 1:4, 1:4] = K
        W2[8 + j, j, 2:5, 2:5] = K

    # ---------------- fc: PROBE - histogram of total feature mass S = sum(f) ----------------
    # logit_k = a*(k*S - sum_{j<=k} t_j)  ->  argmax = number of thresholds below S
    thr = np.array([20, 30, 40, 50, 60, 70, 85, 100, 120], dtype=np.float64)
    a = 5.0
    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    for k in range(10):
        Wfc[k, :] = a * k
        bfc[k] = -a * thr[:k].sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
```
