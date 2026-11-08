import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear part (units 0,1): logit1 += scale * w.x ----
    w = np.zeros(12, dtype=np.float32)
    w[1] = 0.5    # x1 positive
    w[4] = -0.5   # x4 negative
    w[6] = -0.5   # x6 negative
    w[7] = 0.5    # x7 positive (strong)
    w[9] = -0.5   # x9 negative (strong)
    w[11] = 0.5   # x11 positive (mild)
    scale = 1.0
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = scale
    W2[1, 1] = -scale

    # ---- Group |x| probe (units 2..13) ----
    # For each feature f: units relu(x_f), relu(-x_f), both weighted +s
    # -> logit1 += s*|x_f|; subtract s*E|x| (=0.798) in the bias to keep it centred.
    s = 0.3
    group = [0, 2, 3, 5, 8, 10]
    u = 2
    for f in group:
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798
        u += 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
