## Step 3: penalise large families in 3rd class

**What I'm changing.** Step 2 helped a little: accuracy rose to 80.8% and loss fell to 0.426.

The next gap I'm targeting is large families in 3rd class. These passengers (several siblings, or parents travelling with many children) died at very high rates. That includes the women and children, whom the current model often predicts to survive. A per-person sibsp/parch penalty is too gentle to capture this.

**New hidden unit 4.** It computes `relu(sibsp + parch + 3·pclass3 − 4.5)`, which behaves like this:
- In 3rd class, it starts firing once the family is about 2 or more, and grows with each extra relative.
- Outside 3rd class, it only fires for family sizes of 5 or more, which are rare.

Each unit of activation lowers the survival logit by 0.7. Everything else is unchanged from step 2.

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

    # ---- Unit 4 (new): large family in 3rd class ----
    # relu(sibsp + parch + 3*pclass3 - 4.5): in 3rd class fires from family ~2 up
    W1[4, SIB] = 1.0
    W1[4, PAR] = 1.0
    W1[4, P3] = 3.0
    b1[4] = -4.5

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.0   # 3rd-class female penalty
    W2[1, 3] = 2.5    # young-boy boost
    W2[1, 4] = -0.7   # large 3rd-class family penalty (per unit of activation)

    return {"fc1.weight": W1, "fc1.bias": b1,
            "fc2.weight": W2, "fc2.bias": b2}
```
