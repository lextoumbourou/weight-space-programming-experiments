## Step 5: more confidence for men in 2nd and 3rd class

**What I'm changing.** Step 4 brought accuracy to 81.7% and loss to 0.414.

Adult men in 2nd and 3rd class survived only about 8–14% of the time. The model currently gives them a survival logit of roughly −1.4 to −1.8, which is a probability of about 0.14–0.20. That is too optimistic, and it costs loss across a very large group of passengers.

**New hidden unit 6.** It computes `relu(1 − female − pclass1)`, so it equals 1 only for males in 2nd or 3rd class. It adds −0.5 to their survival logit.

Young boys still get the separate +2.5 boost from unit 3, which offsets this penalty for them. Everything else is unchanged from step 4.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Feature indices
    P1, P2, P3, FEM, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

    # ---- Linear survival score s (logit of survival) ----
    s = np.zeros(13, dtype=np.float32)
    s[FEM] = 3.0     # women survived far more often
    s[P1] = 0.6      # 1st class bonus
    s[P2] = -0.6     # 2nd class penalty
    s[P3] = -0.8     # 3rd class penalty
    s[CAB] = 0.4     # recorded cabin
    s[EC] = 0.3      # Cherbourg boarders
    s[SIB] = -0.3    # siblings/spouses aboard
    s[PAR] = -0.1    # parents/children aboard
    s[AGE] = -0.4    # -0.4 per decade of age
    s[AGEK] = 1.2    # with the -1.2 below: 0 at age 30, missing age -> -0.2
    s_bias = -0.8 - 1.2 + 1.0

    # Units 0/1: pass s through exactly as relu(s) - relu(-s)
    W1[0] = s
    b1[0] = s_bias
    W1[1] = -s
    b1[1] = -s_bias

    # ---- Unit 2: female AND 3rd class ----
    W1[2, FEM] = 1.0
    W1[2, P3] = 1.0
    b1[2] = -1.0

    # ---- Unit 3: young boy (male, known age, fades out by ~14) ----
    W1[3, AGEK] = 1.0
    W1[3, FEM] = -1.0
    W1[3, AGE] = -0.7

    # ---- Unit 4: large family in 3rd class ----
    W1[4, SIB] = 1.0
    W1[4, PAR] = 1.0
    W1[4, P3] = 3.0
    b1[4] = -4.5

    # ---- Unit 5: female in 1st/2nd class ----
    W1[5, FEM] = 1.0
    W1[5, P3] = -1.0

    # ---- Unit 6 (new): male in 2nd/3rd class -> relu(1 - female - pclass1) ----
    W1[6, FEM] = -1.0
    W1[6, P1] = -1.0
    b1[6] = 1.0

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.0   # 3rd-class female penalty
    W2[1, 3] = 2.5    # young-boy boost
    W2[1, 4] = -0.7   # large 3rd-class family penalty
    W2[1, 5] = 0.8    # 1st/2nd-class women boost
    W2[1, 6] = -0.5   # 2nd/3rd-class men penalty

    return {"fc1.weight": W1, "fc1.bias": b1,
            "fc2.weight": W2, "fc2.bias": b2}
```
