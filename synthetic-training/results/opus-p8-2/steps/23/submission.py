import numpy as np

def build_weights():
    # Logit gap d = logit1 - logit0
    #   d = bias + sum_i lin[i]*x_i + sum_i absc[i]*|x_i|
    #         + sum_(i,j,g) g * (|x_i + x_j| - |x_i - x_j|) / 2
    lin  = np.zeros(12, dtype=np.float32)
    absc = np.zeros(12, dtype=np.float32)
    bias = float(np.log(395.0 / 605.0))   # class prior

    lin[1] =  1.0    # x1 positive   <-- probe: raised from 0.7
    lin[4] = -0.7    # x4 negative
    lin[7] =  0.7    # x7 positive
    lin[9] = -0.7    # x9 negative

    inter = []       # no interaction terms (x1*x7 did not help)

    bias -= 0.798 * float(np.sum(absc))   # centring for |x| terms (none now)

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    def add_out(unit, coef):
        W2[1, unit] += 0.5 * coef
        W2[0, unit] -= 0.5 * coef

    # Units 0..7: per-feature pairs relu(x_f), relu(-x_f)
    feats = [i for i in range(12) if lin[i] != 0 or absc[i] != 0][:4]
    for k, f in enumerate(feats):
        u, v = 2 * k, 2 * k + 1
        W1[u, f] = 1.0
        W1[v, f] = -1.0
        add_out(u, lin[f] + absc[f])
        add_out(v, -lin[f] + absc[f])

    # Units 8..15: interaction terms, 4 units each
    for n, (i, j, g) in enumerate(inter[:2]):
        base = 8 + 4 * n
        W1[base + 0, i] = 1.0;  W1[base + 0, j] = 1.0
        W1[base + 1, i] = -1.0; W1[base + 1, j] = -1.0
        W1[base + 2, i] = 1.0;  W1[base + 2, j] = -1.0
        W1[base + 3, i] = -1.0; W1[base + 3, j] = 1.0
        add_out(base + 0, 0.5 * g)
        add_out(base + 1, 0.5 * g)
        add_out(base + 2, -0.5 * g)
        add_out(base + 3, -0.5 * g)

    b2[1] = 0.5 * bias
    b2[0] = -0.5 * bias

    return {"fc1.weight": W1, "fc1.bias": b1, "fc2.weight": W2, "fc2.bias": b2}
