import numpy as np

def build_weights():
    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Prior: class-1 logit bias = log(395/605)
    b2[1] = np.log(395.0 / 605.0)

    # ---- Linear score z = w.x (units 0,1 = relu(z), relu(-z)) ----
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

    # Asymmetric slopes: logit1 += a_pos*relu(z) - a_neg*relu(-z)
    a_pos, a_neg = 1.35, 0.75
    W2[1, 0] = a_pos
    W2[1, 1] = -a_neg
    sigma_z = float(np.sqrt(np.sum(w.astype(np.float64) ** 2)))
    b2[1] -= 0.5 * (a_pos - a_neg) * 0.798 * sigma_z   # centre the |z| part

    # ---- |x| terms: units (u,u+1) = relu(x_f), relu(-x_f), both weighted s ----
    def add_abs(u, f, s):
        W1[u, f] = 1.0
        W1[u + 1, f] = -1.0
        W2[1, u] = s
        W2[1, u + 1] = s
        b2[1] -= s * 0.798   # centre using E|x| = 0.798

    add_abs(2, 7, 0.4)     # |x7| positive
    add_abs(4, 1, -0.3)    # |x1| negative
    add_abs(6, 4, -0.3)    # |x4| negative
    add_abs(8, 6, -0.3)    # |x6| negative
    add_abs(10, 11, -0.3)  # |x11| negative

    # ---- Pair interaction probe: logit1 += s * 0.5*(|x7 + x4| - |x7 - x4|) ~ s*x7*x4 ----
    s = -0.6
    a, b = 7, 4
    W1[12, a] = 1.0;  W1[12, b] = 1.0     # relu(x7 + x4)
    W1[13, a] = -1.0; W1[13, b] = -1.0    # relu(-x7 - x4)
    W1[14, a] = 1.0;  W1[14, b] = -1.0    # relu(x7 - x4)
    W1[15, a] = -1.0; W1[15, b] = 1.0     # relu(x4 - x7)
    W2[1, 12] = s / 2
    W2[1, 13] = s / 2
    W2[1, 14] = -s / 2
    W2[1, 15] = -s / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
