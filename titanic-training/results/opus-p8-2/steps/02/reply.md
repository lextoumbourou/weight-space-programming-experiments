## Step 2: shift the score toward survival

**What I'm changing.** Step 1 scored 80.3% accuracy and a loss of 0.430. The confusion matrix shows the model is biased toward "died": it caught only 129 of 230 survivors, while wrongly predicting survival for just 17 passengers who died.

The likeliest cause is 3rd-class women. With step 1's weights, a typical one (age 30, travelling alone) scored about −0.3, so she was always predicted to die. In reality this group survived about half the time.

I'm making two adjustments:
- **Intercept:** raised from −1.0 to −0.8, which nudges everyone's survival score up a little.
- **3rd-class female penalty:** reduced from −1.5 to −1.0.

Everything else is the same as step 1.

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
    s_bias = -0.8 - 1.2 + 1.0  # intercept raised from -1.0 to -0.8

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

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0
    W2[1, 2] = -1.0   # 3rd-class female penalty, reduced from -1.5
    W2[1, 3] = 2.5    # young-boy boost

    return {"fc1.weight": W1, "fc1.bias": b1,
            "fc2.weight": W2, "fc2.bias": b2}
```
