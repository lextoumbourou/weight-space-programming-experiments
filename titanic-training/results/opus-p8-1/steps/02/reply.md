## Step 2: favour children outside 3rd class and nudge the baseline up

Step 1 scored 0.4197 loss and 80.8% accuracy. It predicted "died" for 67 actual survivors and "survived" for only 48 passengers who died. So it slightly under-predicts survival overall.

Changes in this step:

1. **Baseline.** The base log-odds goes up from −0.6 to −0.45.
2. **Children by class.** Nearly all 1st- and 2nd-class children survived, while 3rd-class children often died. To capture this:
   - The general child bonus (h3) drops from 1.2 to 0.9.
   - A new unit, h5, gives an extra bonus to known-age children outside 3rd class.
   - h5 = ReLU(1.5·age_known − age_decades − 1.5·pclass_3). For 3rd class the input is at most 0, so the unit stays off. For other children it equals h3.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Feature indices
    P1, P2, P3, FEM, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

    # ---- Linear survival score z (log-odds of survival) ----
    w = np.zeros(13, dtype=np.float32)
    w[P2] = -1.1          # 2nd class vs 1st
    w[P3] = -1.3          # 3rd class vs 1st (women in 3rd handled by h2)
    w[FEM] = 3.4          # female
    w[AGE] = -0.2         # per decade of age
    w[AGEK] = 0.6         # centres age term at 30 yrs (0 when age unknown)
    w[SIB] = -0.35        # siblings/spouses
    w[PAR] = -0.1         # parents/children
    w[FARE] = 0.1         # log fare
    w[EC] = 0.35          # Cherbourg
    w[CAB] = 0.5          # cabin recorded
    bz = -0.45            # base log-odds (raised from -0.6)

    # h0 = relu(z), h1 = relu(-z); output h0 - h1 = z
    W1[0] = w;  b1[0] = bz
    W1[1] = -w; b1[1] = -bz

    # h2: female AND 3rd class
    W1[2, FEM] = 1.0; W1[2, P3] = 1.0; b1[2] = -1.0

    # h3: child bonus (known age < 15), all classes
    W1[3, AGEK] = 1.5; W1[3, AGE] = -1.0

    # h4: large family, relu(sibsp + parch - 3)
    W1[4, SIB] = 1.0; W1[4, PAR] = 1.0; b1[4] = -3.0

    # h5: child in 1st/2nd class -> relu(1.5*agek - age - 1.5*p3)
    W1[5, AGEK] = 1.5; W1[5, AGE] = -1.0; W1[5, P3] = -1.5

    # ---- Output layer: logit[0] = 0 (died), logit[1] = survival score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.7    # 3rd-class women
    W2[1, 3] = 0.9     # children, all classes
    W2[1, 4] = -0.8    # large families
    W2[1, 5] = 0.8     # extra for 1st/2nd class children

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
