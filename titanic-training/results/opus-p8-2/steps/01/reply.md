## Step 1: a hand-written logistic-style baseline

**What I'm trying.** I'm encoding the well-known Titanic survival patterns as one linear "survival score" `s` per passenger:

- **Sex:** women survived far more often (+3.0).
- **Class:** first class helps (+0.6), second class hurts (−0.6), third class hurts more (−0.8).
- **Cabin:** having a recorded cabin helps (+0.4).
- **Port:** boarding at Cherbourg helps a little (+0.3).
- **Family size:** siblings/spouses (−0.3 each) and parents/children (−0.1 each) hurt.
- **Age:** −0.4 per decade, centred so that a 30-year-old scores 0. A missing age gets a fixed −0.2.

**How the network carries this score.** A ReLU layer cannot pass a signed number through one unit, so I split it across two units:

- Unit 0 holds `relu(s)`.
- Unit 1 holds `relu(−s)`.
- The output computes `logit_survived = h0 − h1`, which equals `s` exactly.

**Two interaction units** capture what a purely linear score misses:

- **Unit 2, "female in 3rd class":** these women survived only about half the time, much less often than other women. This unit lowers their score by 1.5.
- **Unit 3, "young boy":** it fires for males with a known age, strongest for the youngest and fading to zero around age 14. It raises their score by 2.5.

All other hidden units are left at zero. `logit_died` is fixed at 0, so the survival probability is `sigmoid(score)`.

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
    s[CAB] = 0.4     # recorded cabin (mostly upper decks / wealthier)
    s[EC] = 0.3      # Cherbourg boarders survived more
    s[SIB] = -0.3    # siblings/spouses aboard
    s[PAR] = -0.1    # parents/children aboard
    # Age term: -0.4*age_dec + 1.2*age_known, combined with the -1.2 below,
    # gives 0 at age 30; a missing age gets a fixed -0.2 in total.
    s[AGE] = -0.4
    s[AGEK] = 1.2
    s_bias = -1.0 - 1.2 + 1.0  # base intercept -1.0, age centering -1.2, missing-age fix +1.0

    # Unit 0 = relu(s), unit 1 = relu(-s); together they pass s through exactly
    W1[0] = s
    b1[0] = s_bias
    W1[1] = -s
    b1[1] = -s_bias

    # ---- Unit 2: female AND 3rd class -> fires as 1 only when both are 1 ----
    W1[2, FEM] = 1.0
    W1[2, P3] = 1.0
    b1[2] = -1.0

    # ---- Unit 3: young boy -> male with known age, value ~1 at age 0, 0 at ~14 ----
    W1[3, AGEK] = 1.0
    W1[3, FEM] = -1.0
    W1[3, AGE] = -0.7
    b1[3] = 0.0

    # ---- Output layer: logit_died = 0, logit_survived = score ----
    W2[1, 0] = 1.0    # +relu(s)
    W2[1, 1] = -1.0   # -relu(-s)  => together equal s
    W2[1, 2] = -1.5   # 3rd-class women survived less than other women
    W2[1, 3] = 2.5    # boost for young boys ("women and children first")
    b2[:] = 0.0

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
