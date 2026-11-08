## Step 11: smaller penalty for siblings and spouses

The missing-age penalty made no real difference (0.4144 against 0.4141), so this step goes back to the step 8 settings:

- age slope −0.3 per decade;
- age_known weight 0.9;
- men's base log-odds −0.85.

**Siblings and spouses.** Historically, passengers with one sibling or spouse aboard (usually a spouse) did about as well as, or better than, those travelling alone. Only large sibling groups did badly. The large-family unit h4 already penalises families of 5 or more. So this step:

- weakens the linear sibsp penalty from −0.35 to −0.2 per person;
- leaves h4 unchanged.

```python
import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    P1, P2, P3, FEM, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

    # ---- Linear survival score z ----
    w = np.zeros(13, dtype=np.float32)
    w[P2] = -1.1          # 2nd class vs 1st
    w[P3] = -1.3          # 3rd class vs 1st
    w[FEM] = 3.65         # female
    w[AGE] = -0.3         # per decade
    w[AGEK] = 0.9         # centres age term at 30 yrs
    w[SIB] = -0.2         # siblings/spouses (weaker; big families handled by h4)
    w[PAR] = -0.1         # parents/children
    w[FARE] = 0.1         # log fare
    w[EC] = 0.35          # Cherbourg
    w[CAB] = 0.5          # cabin recorded
    bz = -0.85            # base log-odds (men)

    # h0/h1: pass z through ReLU pair
    W1[0] = w;  b1[0] = bz
    W1[1] = -w; b1[1] = -bz

    # h2: female AND 3rd class
    W1[2, FEM] = 1.0; W1[2, P3] = 1.0; b1[2] = -1.0

    # h3: child bonus (known age < 15)
    W1[3, AGEK] = 1.5; W1[3, AGE] = -1.0

    # h4: large family, relu(sibsp + parch - 3)
    W1[4, SIB] = 1.0; W1[4, PAR] = 1.0; b1[4] = -3.0

    # h5: child in 1st/2nd class
    W1[5, AGEK] = 1.5; W1[5, AGE] = -1.0; W1[5, P3] = -1.5

    # ---- Output ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.7    # 3rd-class women
    W2[1, 3] = 0.9     # children
    W2[1, 4] = -0.8    # large families
    W2[1, 5] = 0.8     # 1st/2nd class children extra

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
```
