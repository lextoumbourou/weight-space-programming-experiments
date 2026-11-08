## Step 11: separate age slopes for men and women

**What I'm changing.** Fare weights of 0.2 (step 9) and 0.3 (step 10) gave almost identical losses, 0.4127 and 0.4131. I'm settling on 0.25, with the intercept correction in between.

Next I'm looking at age. "Women and children first" suggests that age mattered mostly for males: an older man was much less likely to get a lifeboat seat. For women, survival depended far less on age.

**Age slopes.**
- **Males:** the base age slope becomes steeper, −0.5 per decade instead of −0.4. The age_known weight rises to 1.5, so a 30-year-old still scores 0.
- **Females:** two new hidden units cancel most of that slope, leaving women with −0.2 per decade. Women aged 30 are unchanged.

**New hidden units.**
- **Unit 6** computes `relu(age_dec + 10·female − 10)`. This equals age_dec for women and 0 for men, since no one is older than 100. It adds +0.3 per decade back for women.
- **Unit 7** computes `relu(age_known + female − 1)`. This is 1 for women with a recorded age. Its −0.9 output weight keeps a 30-year-old woman centred at 0.

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
    s[AGE] = -0.5    # male age slope (women partly restored below)
    s[AGEK] = 1.5    # with -0.5*age: 0 at age 30; missing age: 0
    s[FARE] = 0.25   # higher fare within class -> better survival
    s_bias = -1.0 - 0.72  # intercept -1.0, minus 0.25 * ~2.9 typical log-fare

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

    # ---- Unit 6: age for women only -> relu(age + 10*female - 10) ----
    W1[6, AGE] = 1.0
    W1[6, FEM] = 10.0
    b1[6] = -10.0

    # ---- Unit 7: female with known age -> relu(age_known + female - 1) ----
    W1[7, AGEK] = 1.0
    W1[7, FEM] = 1.0
    b1[7] = -1.0

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.0   # 3rd-class female penalty
    W2[1, 3] = 2.5    # young-boy boost
    W2[1, 4] = -0.7   # large 3rd-class family penalty
    W2[1, 5] = 0.8    # 1st/2nd-class women boost
    W2[1, 6] = 0.3    # women's age slope -0.5+0.3 = -0.2 per decade
    W2[1, 7] = -0.9   # re-centre women at age 30 (0.3*3)

    return {"fc1.weight": W1, "fc1.bias": b1,
            "fc2.weight": W2, "fc2.bias": b2}
```
