import numpy as np

def build_weights():
    # Probe settings: which feature to test and how strongly
    FEAT = 0      # feature index being probed
    SCALE = 0.5   # logit-difference slope applied to that feature

    W1 = np.zeros((16, 12), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # Hidden unit 0 = relu(x_FEAT), hidden unit 1 = relu(-x_FEAT)
    W1[0, FEAT] = 1.0
    W1[1, FEAT] = -1.0

    # Class-1 logit gets +SCALE/2 * x, class-0 logit gets -SCALE/2 * x,
    # so logit1 - logit0 = SCALE * (relu(x) - relu(-x)) = SCALE * x
    W2[1, 0] = SCALE / 2
    W2[1, 1] = -SCALE / 2
    W2[0, 0] = -SCALE / 2
    W2[0, 1] = SCALE / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
