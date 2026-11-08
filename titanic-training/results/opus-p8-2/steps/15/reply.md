## Step 15: split 3rd-class women by port of embarkation

**What I'm changing.** The class-split boy boost in step 14 tied the best loss (0.4127). Boys are a small group, so I'm keeping it as harmless.

The biggest uncertain group is 3rd-class women, who survived about half the time overall. That average hides a large difference by port. Those who boarded at Southampton survived only about 38% of the time, while those from Cherbourg or Queenstown survived roughly 65–70%.

**3rd-class women by port.**
- **New unit 7:** it computes `relu(female + pclass3 + embarked_s − 2)`, so it equals 1 only for 3rd-class women who boarded at Southampton. It adds −0.7 to their survival logit.
- **Unit 2 (all 3rd-class women):** the general penalty eases from −1.0 to −0.6.

Combined, Southampton women now get −1.3, slightly more than before, while Cherbourg and Queenstown women get only −0.6.

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
    s[AGEK] = 1.2    # known age: 0 at age 30; missing age: 0
    s[FARE] = 0.2    # higher fare within class -> better survival
    s_bias = -1.0 - 0.55

    # Units 0/1: pass s through exactly as relu(s) - relu(-s)
    W1[0] = s
    b1[0] = s_bias
    W1[1] = -s
    b1[1] = -s_bias

    # ---- Unit 2: female AND 3rd class ----
    W1[2, FEM] = 1.0
    W1[2, P3] = 1.0
    b1[2] = -1.0

    # ---- Unit 3: young boy, any class ----
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

    # ---- Unit 6: young boy in 1st/2nd class ----
    W1[6, AGEK] = 1.0
    W1[6, FEM] = -1.0
    W1[6, AGE] = -0.7
    W1[6, P3] = -1.0

    # ---- Unit 7 (new): 3rd-class female from Southampton ----
    W1[7, FEM] = 1.0
    W1[7, P3] = 1.0
    W1[7, ES] = 1.0
    b1[7] = -2.0

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -0.6   # 3rd-class female penalty (eased from -1.0)
    W2[1, 3] = 2.0    # young-boy boost, all classes
    W2[1, 4] = -0.7   # large 3rd-class family penalty
    W2[1, 5] = 0.8    # 1st/2nd-class women boost
    W2[1, 6] = 1.5    # extra boost for 1st/2nd-class boys
    W2[1, 7] = -0.7   # extra penalty for 3rd-class Southampton women

    return {"fc1.weight": W1, "fc1.bias": b1,
            "fc2.weight": W2, "fc2.bias": b2}
```
