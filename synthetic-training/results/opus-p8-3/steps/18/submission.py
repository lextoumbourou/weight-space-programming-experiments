import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds
    GAIN = 1.0                     # overall scale on the linear direction

    # Linear direction from single-feature probes
    beta = np.array([
        0.0, 0.63, 0.10, 0.0, -0.49, 0.10,
        -0.24, 0.63, 0.0, -0.52, 0.0, 0.44,
    ], dtype=np.float32) * GAIN

    # Interaction probe between features A and B
    A, B = 1, 7
    INT_COEF = 0.5

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Units 0/1: linear part, relu(beta.x) - relu(-beta.x) = beta.x
    W1[0] = beta
    W1[1] = -beta
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Units 2/3: relu(xA+xB), relu(-(xA+xB))  -> sum = |xA+xB|
    W1[2, A], W1[2, B] = 1.0, 1.0
    W1[3, A], W1[3, B] = -1.0, -1.0
    # Units 4/5: relu(xA-xB), relu(-(xA-xB))  -> sum = |xA-xB|
    W1[4, A], W1[4, B] = 1.0, -1.0
    W1[5, A], W1[5, B] = -1.0, 1.0

    # logit diff += INT_COEF * (|xA+xB| - |xA-xB|) / 2
    c = INT_COEF / 2
    for u, s in [(2, 1.0), (3, 1.0), (4, -1.0), (5, -1.0)]:
        W2[1, u] = s * c / 2
        W2[0, u] = -s * c / 2

    # Output bias: class prior
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
