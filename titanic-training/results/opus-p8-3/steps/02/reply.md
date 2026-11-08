## Step 2: penalise large families in third class

Step 1 gave loss 0.433 and accuracy 79.7%. There were 64 false "survived" predictions and 58 missed survivors.

A known pattern is that large third-class families almost all died. The plain linear sibsp/parch terms are too weak to capture this. I am adding one new unit for it and leaving everything else unchanged, so the effect of this change can be seen on its own.

- **Unit 5** is ReLU(sibsp + parch + 4·pclass_3 − 6).
- For anyone not in third class it is 0, because sibsp + parch never gets close to 6 there in practice.
- In third class it switches on once sibsp + parch ≥ 3, meaning a family of 4 or more. It grows by 1 for each extra relative.
- It applies −0.7 per unit to the survival logit.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Feature indices
    P1, P2, P3, F, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

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
    W2[1, 2] = -0.6

    # Unit 3: male AND second class
    W1[3, P2] = 1.0; W1[3, F] = -1.0
    W2[1, 3] = -1.0

    # Unit 4: child bonus, ReLU(1.5*age_known - age_decades)
    W1[4, AGEK] = 1.5; W1[4, AGE] = -1.0
    W2[1, 4] = 1.5

    # Unit 5: large family in third class, ReLU(sib + par + 4*P3 - 6)
    # nonzero only for 3rd class with sib+par >= 3 (family of 4+)
    W1[5, SIB] = 1.0; W1[5, PAR] = 1.0; W1[5, P3] = 4.0; b1[5] = -6.0
    W2[1, 5] = -0.7

    return {
        "fc1.weight": W1.astype(np.float32),
        "fc1.bias": b1.astype(np.float32),
        "fc2.weight": W2.astype(np.float32),
        "fc2.bias": b2.astype(np.float32),
    }
```
