import numpy as np
import math

def build_weights():
    # ---- linear part (units 0/1 carry w.x through ReLU pair) ----
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.6    # dominant positive feature (raised: interaction unit handles x10&x4 case)
    w[4]  = -0.3   # negative binary feature
    w[1]  = 0.3    # positive
    w[5]  = 0.25   # positive
    w[9]  = 0.2    # positive
    w[2]  = 0.1    # weak positive
    w[0]  = -0.15  # weak negative (binary)
    w[3]  = -0.15  # weak negative, skewed tail
    w[8]  = -0.1   # weak negative

    b = -0.7       # bias for class-1 logit

    fc1_w = np.zeros((16, 13), dtype=np.float32)
    fc1_b = np.zeros(16, dtype=np.float32)
    fc1_w[0] = w        # h0 = relu(w.x)
    fc1_w[1] = -w       # h1 = relu(-w.x)

    # ---- interaction unit: fires only when x10 high AND x4 high ----
    fc1_w[2, 10] = 1.0
    fc1_w[2, 4]  = 1.0
    fc1_b[2] = -1.5

    fc2_w = np.zeros((2, 16), dtype=np.float32)
    fc2_b = np.zeros(2, dtype=np.float32)
    # class-1 logit = w.x + b + v*h2 ; class-0 logit = 0
    fc2_w[1, 0] = 1.0
    fc2_w[1, 1] = -1.0
    fc2_w[1, 2] = -1.5    # penalty when both x10 and x4 are high
    fc2_b[1] = b

    return {
        "fc1.weight": fc1_w,
        "fc1.bias": fc1_b,
        "fc2.weight": fc2_w,
        "fc2.bias": fc2_b,
    }
