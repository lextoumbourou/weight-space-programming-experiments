import numpy as np

def build_weights():
    PRIOR = np.log(395.0 / 605.0)  # class-1 log-odds
    GAIN = 1.0                     # overall scale on the linear direction

    # Estimated per-feature logistic coefficients from single-feature probes
    beta = np.array([
        0.0,    # x0  none
        0.63,   # x1  strong +
        0.10,   # x2  weak +
        0.0,    # x3  none
        -0.49,  # x4  strong -
        0.10,   # x5  weak +
        -0.24,  # x6  moderate -
        0.63,   # x7  strong +
        0.0,    # x8  none
        -0.52,  # x9  strong -
        0.0,    # x10 none
        0.44,   # x11 moderate +
    ], dtype=np.float32) * GAIN

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden 0 = relu(beta.x), hidden 1 = relu(-beta.x)
    W1[0] = beta
    W1[1] = -beta

    # logit1 - logit0 = h0 - h1 = beta.x
    W2[1, 0], W2[1, 1] = 0.5, -0.5
    W2[0, 0], W2[0, 1] = -0.5, 0.5

    # Class prior in output bias
    b2[1] = PRIOR / 2
    b2[0] = -PRIOR / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
