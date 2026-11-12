import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 polarity edge detectors (unchanged) ----------------
    alphas = [k * 45.0 for k in range(8)]
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float64)
    b1 = np.zeros(8, dtype=np.float64)
    for k, al in enumerate(alphas):
        a = math.radians(al)
        gx, gy = math.cos(a), math.sin(a)
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                dx, dy = c - 2, r - 2
                t = dx * gx + dy * gy
                s = -dx * gy + dy * gx
                w[r, c] = t * math.exp(-t * t / 2.0) * math.exp(-s * s / (2 * 1.5 ** 2))
        w /= w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15

    # ---------------- conv2: two grids of the 8 edge maps (unchanged) ----------------
    W2 = np.zeros((16, 8, 5, 5), dtype=np.float64)
    b2 = np.zeros(16, dtype=np.float64)
    k1 = np.array([0.5, 1.0, 0.5])
    K = np.outer(k1, k1)
    for j in range(8):
        W2[j, j, 1:4, 1:4] = K
        W2[8 + j, j, 2:5, 2:5] = K

    # ---------------- fc: PROBE - histogram of total feature mass S = sum(f) ----------------
    # logit_k = a*(k*S - sum_{j<=k} t_j)  ->  argmax = number of thresholds below S
    thr = np.array([20, 30, 40, 50, 60, 70, 85, 100, 120], dtype=np.float64)
    a = 5.0
    Wfc = np.zeros((10, 256), dtype=np.float64)
    bfc = np.zeros(10, dtype=np.float64)
    for k in range(10):
        Wfc[k, :] = a * k
        bfc[k] = -a * thr[:k].sum()

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
