import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear part (units 0,1): logit1 += w.x ----
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.68    # x1
    w[2] = 0.10    # x2 (weak)
    w[4] = -0.60   # x4
    w[5] = 0.10    # x5 (weak)
    w[6] = -0.34   # x6
    w[7] = 0.78    # x7 (strongest)
    w[9] = -0.67   # x9
    w[11] = 0.21   # x11
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = 1.0
    W2[1, 1] = -1.0

    # ---- Kept: |x7| term (units 2,3): logit1 += 0.4*(|x7| - 0.798) ----
    W1[2, 7] = 1.0
    W1[3, 7] = -1.0
    W2[1, 2] = 0.4
    W2[1, 3] = 0.4
    b2[1] -= 0.4 * 0.798

    # ---- Interaction probes: logit1 += s * 0.5*(|a+b| - |a-b|)  (~ product a*b) ----
    def add_pair(u, a, b, s):
        # units u,u+1: relu(a+b), relu(-a-b)  -> +s/2 each  (= s/2*|a+b|)
        W1[u, a] = 1.0;  W1[u, b] = 1.0
        W1[u + 1, a] = -1.0; W1[u + 1, b] = -1.0
        W2[1, u] = s / 2;  W2[1, u + 1] = s / 2
        # units u+2,u+3: relu(a-b), relu(b-a) -> -s/2 each (= -s/2*|a-b|)
        W1[u + 2, a] = 1.0;  W1[u + 2, b] = -1.0
        W1[u + 3, a] = -1.0; W1[u + 3, b] = 1.0
        W2[1, u + 2] = -s / 2; W2[1, u + 3] = -s / 2

    add_pair(4, 1, 7, 0.4)    # probe x1*x7
    add_pair(8, 7, 9, 0.4)    # probe x7*x9
    add_pair(12, 1, 9, 0.4)   # probe x1*x9

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
