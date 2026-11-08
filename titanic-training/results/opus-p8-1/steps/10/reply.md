## Step 10: penalise a missing age

**Age slope.** Going from −0.3 to −0.4 per decade made the loss worse (0.4150), so the slope goes back to −0.3. The age_known weight returns to its centring value of 0.9 before the change below.

**Missing age.** This step tests how passengers with no recorded age are treated. Missing ages were more common among passengers who died, partly because their records were never completed. So a missing age may itself predict a lower chance of survival.

- The age_known weight goes from 0.9 to 1.1.
- Known-age passengers gain +0.2 relative to unknown ones. Unknown-age passengers therefore score 0.2 lower than an average 30-year-old.
- The base log-odds drops from −0.85 to −1.0 to offset the +0.2. This keeps known-age passengers roughly where they were.

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
    w[AGEK] = 1.1         # 0.9 centres age at 30; +0.2 = known age bonus vs missing
    w[SIB] = -0.35        # siblings/spouses
    w[PAR] = -0.1         # parents/children
    w[FARE] = 0.1         # log fare
    w[EC] = 0.35          # Cherbourg
    w[CAB] = 0.5          # cabin recorded
    bz = -1.0             # base log-odds (men), offset for the +0.2 on known age

    # h0/h1: pass z through ReLU pair
    W1[0] = w;  b1[0] = bz
    W1[1] = -w; b1[1] = -bz

    # h2: female AND 3rd class
    W1[2, FEM] = 1.0; W1[2, P3] = 1.0; b1[2] = -1.0

    # h3: child bonus (known age < 15)
    W1[3, AGEK] = 1.5; W1[3, AGE] = -1.0

    # h4: large family
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
