import numpy as np

def build_weights():
    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Feature indices
    P1, P2, P3, FEM, AGE, AGEK, SIB, PAR, FARE, EC, EQ, ES, CAB = range(13)

    # ---- Linear survival score z (log-odds of survival) ----
    # Reference: male, 1st class, adult ~30 (or unknown age), embarked S, no cabin.
    w = np.zeros(13, dtype=np.float32)
    w[P2] = -1.1          # 2nd class vs 1st
    w[P3] = -1.3          # 3rd class vs 1st (for men; women in 3rd handled by h2)
    w[FEM] = 3.4          # being female
    w[AGE] = -0.2         # older -> slightly worse (per decade)
    w[AGEK] = 0.6         # centres age term at 30 yrs: -0.2*(age-3) when known, 0 when unknown
    w[SIB] = -0.35        # siblings/spouses aboard
    w[PAR] = -0.1         # parents/children aboard
    w[FARE] = 0.1         # higher fare slightly better
    w[EC] = 0.35          # Cherbourg
    w[EQ] = 0.0           # Queenstown
    w[CAB] = 0.5          # cabin recorded
    bz = -0.6             # base log-odds for reference passenger (~35%)

    # h0 = relu(z), h1 = relu(-z); output uses h0 - h1 = z
    W1[0] = w
    b1[0] = bz
    W1[1] = -w
    b1[1] = -bz

    # h2: female AND 3rd class -> relu(female + p3 - 1) is 1 only when both
    W1[2, FEM] = 1.0
    W1[2, P3] = 1.0
    b1[2] = -1.0

    # h3: child bonus -> relu(1.5*age_known - age_decades), positive only for known age < 15
    W1[3, AGEK] = 1.5
    W1[3, AGE] = -1.0

    # h4: large family -> relu(sibsp + parch - 3)
    W1[4, SIB] = 1.0
    W1[4, PAR] = 1.0
    b1[4] = -3.0

    # ---- Output layer: logit[0] (died) = 0, logit[1] (survived) = score ----
    W2[1, 0] = 1.0     # +z positive part
    W2[1, 1] = -1.0    # -(negative part) -> together gives z
    W2[1, 2] = -1.7    # 3rd-class women survived much less than the linear score implies
    W2[1, 3] = 1.2     # children: up to +1.8 for infants
    W2[1, 4] = -0.8    # extra penalty per family member beyond 3

    return {
        "fc1.weight": W1.astype(np.float32),
        "fc1.bias": b1.astype(np.float32),
        "fc2.weight": W2.astype(np.float32),
        "fc2.bias": b2.astype(np.float32),
    }
