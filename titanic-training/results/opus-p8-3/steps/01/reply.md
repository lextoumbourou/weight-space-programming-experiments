## Step 1: a hand-built logistic score plus a few interaction units

I am starting from a logistic-regression-style log-odds score built from what I know about Titanic survival:

- Women survived far more often than men.
- First class did better than second, and second better than third.
- Survival odds fall with age, and children did well.
- Large families did worse.
- Cherbourg passengers and passengers with a recorded cabin did somewhat better.

How the hidden units are used:

- **Units 0 and 1** pass that linear score through unchanged. Unit 0 is ReLU(s) and unit 1 is ReLU(−s), and the survival logit is h0 − h1, which equals s exactly.
- **Unit 2** fires for female passengers in third class. It applies a penalty, because only about half of them survived, which a purely additive model overestimates.
- **Unit 3** fires for males in second class. It applies a penalty, because adult men in second class fared almost as badly as men in third.
- **Unit 4** is a "child" unit, ReLU(1.5·age_known − age_decades). It is positive only for passengers with a known age under 15 and gives them a survival bonus. It stays at 0 when age is missing.

The died logit is held at 0, so the survived logit carries the whole decision. Units 5 to 15 are unused for now.

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
    s[AGEK] = 1.0    # offsets the age term so a ~30-year-old matches unknown age
    s[SIB]  = -0.3   # siblings/spouses
    s[PAR]  = -0.1   # parents/children
    s[FARE] = 0.1    # log fare
    s[EC]   = 0.3    # Cherbourg
    s[ES]   = -0.1   # Southampton
    s[CAB]  = 0.5    # cabin recorded
    s_bias = -0.1

    # Unit 0 = ReLU(s), unit 1 = ReLU(-s); h0 - h1 = s exactly
    W1[0] = s;  b1[0] = s_bias
    W1[1] = -s; b1[1] = -s_bias
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0

    # Unit 2: female AND third class -> ReLU(F + P3 - 1) is 1 only if both
    W1[2, F] = 1.0; W1[2, P3] = 1.0; b1[2] = -1.0
    W2[1, 2] = -0.6

    # Unit 3: male AND second class -> ReLU(P2 - F) is 1 only for males in 2nd
    W1[3, P2] = 1.0; W1[3, F] = -1.0
    W2[1, 3] = -1.0

    # Unit 4: child bonus -> ReLU(1.5*age_known - age_decades)
    # positive only for known age < 15; 0 when age unknown
    W1[4, AGEK] = 1.5; W1[4, AGE] = -1.0
    W2[1, 4] = 1.5

    # Died logit stays 0 (b2[0] = 0); all decision mass on survived logit
    return {
        "fc1.weight": W1.astype(np.float32),
        "fc1.bias": b1.astype(np.float32),
        "fc2.weight": W2.astype(np.float32),
        "fc2.bias": b2.astype(np.float32),
    }
```
