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

    # ---- Kept: |x7| term (units 2,3) ----
    W1[2, 7] = 1.0
    W1[3, 7] = -1.0
    W2[1, 2] = 0.4
    W2[1, 3] = 0.4
    b2[1] -= 0.4 * 0.798

    # ---- Group interaction probe (units 4,5) ----
    # z = sum_i c_i x_i / sqrt(6) over the 'null' features; logit1 += s*(|z| - 0.798)
    group = [0, 2, 3, 5, 8, 10]
    c = [1, 1, 1, 1, 1, 1]          # sign pattern A (all +)
    s = 0.7
    for f, ci in zip(group, c):
        W1[4, f] = ci / np.sqrt(6.0)
        W1[5, f] = -ci / np.sqrt(6.0)
    W2[1, 4] = s
    W2[1, 5] = s
    b2[1] -= s * 0.798

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
