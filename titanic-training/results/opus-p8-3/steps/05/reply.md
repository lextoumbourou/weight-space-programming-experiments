## Step 5: check whether the outputs are too timid or too confident

The female-third-class penalty of −0.9 flipped a batch of predictions to "died". False "survived" fell from 60 to 45, but missed survivors rose from 58 to 74, and the loss was slightly worse than step 2. So I am settling that penalty at −0.7, between the two values tried.

This step also tests calibration. Every output weight is multiplied by a single scale factor of 1.15. This makes all predictions more confident without changing any decisions. If the loss drops, the model was under-confident and I will push the scale further. If it rises, I will try a scale below 1.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Feature indices
    P1, P2, P3, F, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

    SCALE = 1.15  # global confidence multiplier on all output weights

    # ---- Linear log-odds score s (survived vs died) ----
    s = np.zeros(13, dtype=np.float32)
    s[F]    = 2.5    # female
    s[P2]   = -0.9   # second class (relative to first)
    s[P3]   = -1.9   # third class
    s[AGE]  = -0.35  # per decade of age
    s[AGEK] = 1.0    # offsets age term (30-yr-old ~ unknown age)
    s[SIB]  = -0.3   # siblings/spouses
    s[PAR]  = -0.1   # parents/children
    s[FARE] = 0.1    # log fare
    s[EC]   = 0.3    # Cherbourg
    s[ES]   = -0.1   # Southampton
    s[CAB]  = 0.5    # cabin recorded
    s_bias = -0.1

    # Units 0/1: pass the linear score through (h0 - h1 = s)
    W1[0] = s;  b1[0] = s_bias
    W1[1] = -s; b1[1] = -s_bias
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0

    # Unit 2: female AND third class
    W1[2, F] = 1.0; W1[2, P3] = 1.0; b1[2] = -1.0
    W2[1, 2] = -0.7

    # Unit 3: male AND second class
    W1[3, P2] = 1.0; W1[3, F] = -1.0
    W2[1, 3] = -1.0

    # Unit 4: child bonus, ReLU(1.5*age_known - age_decades)
    W1[4, AGEK] = 1.5; W1[4, AGE] = -1.0
    W2[1, 4] = 1.5

    # Unit 5: large family in third class, ReLU(sib + par + 4*P3 - 6)
    W1[5, SIB] = 1.0; W1[5, PAR] = 1.0; W1[5, P3] = 4.0; b1[5] = -6.0
    W2[1, 5] = -0.8

    W2 *= SCALE

    return {
        "fc1.weight": W1.astype(np.float32),
        "fc1.bias": b1.astype(np.float32),
        "fc2.weight": W2.astype(np.float32),
        "fc2.bias": b2.astype(np.float32),
    }
```
