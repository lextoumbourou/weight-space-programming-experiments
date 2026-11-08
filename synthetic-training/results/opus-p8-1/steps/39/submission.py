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
    add_abs(4, 6, -0.3)    # |x6| negative
    add_abs(6, 11, -0.3)   # |x11| negative

    # ---- Product term via 4 units: logit1 += s * 0.5*(|u+v| - |u-v|) ~ s*u*v ----
    def add_product(unit, uvec, vvec, s):
        W1[unit, :] = uvec + vvec
        W1[unit + 1, :] = -(uvec + vvec)
        W1[unit + 2, :] = uvec - vvec
        W1[unit + 3, :] = -(uvec - vvec)
        W2[1, unit] = s / 2
        W2[1, unit + 1] = s / 2
        W2[1, unit + 2] = -s / 2
        W2[1, unit + 3] = -s / 2

    def e(f):
        v = np.zeros(12, dtype=np.float32)
        v[f] = 1.0
        return v

    # Confirmed interaction: x7 * x4 (negative)
    add_product(8, e(7), e(4), -0.8)

    # Probe: x9 * g, g over subgroup {6, 8, 10, 11}, negative sign
    group = [6, 8, 10, 11]
    g = np.zeros(12, dtype=np.float32)
    for f in group:
        g[f] = 1.0 / np.sqrt(len(group))
    add_product(12, e(9), g, -0.6)

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
