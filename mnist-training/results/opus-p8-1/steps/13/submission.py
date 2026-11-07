import numpy as np
import math

def build_weights():
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)

    # ---------------- conv1 (same as step 12) ----------------
    def gauss(sig):
        G = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                G[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / (2 * sig * sig))
        return G / G.sum()
    W1[0, 0] = gauss(1.0)
    b1[0] = -0.05
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                r, c = i - 2, j - 2
                d = r * math.cos(th) - c * math.sin(th)
                l = r * math.sin(th) + c * math.cos(th)
                K[i, j] = (1 - d * d / 2.0) * math.exp(-d * d / 4.0) * math.exp(-l * l / 12.0)
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[1 + k, 0] = K
        b1[1 + k] = -0.1
    W1[5, 0] = 1.3 * gauss(0.8)      # thresholded ink presence
    b1[5] = -0.3

    # ---------------- conv2 (same as step 12) ----------------
    for k in range(5):
        W2[k, k, 1:4, 1:4] = 1.0
    KL = np.zeros((5, 5))
    for t in (1, 2, 3):
        KL[0, t] += 1 / 3.0; KL[4, t] += 1 / 3.0
        KL[t, 0] += 1 / 3.0; KL[t, 4] += 1 / 3.0
    KL[2, 2] = -3.0
    KV = np.zeros((5, 5))
    for t in (1, 2, 3):
        KV[t, 0] = 1 / 3.0; KV[t, 4] = 1 / 3.0; KV[t, 2] = -1.0
    KH = KV.T.copy()
    W2[5, 5] = KL; b2[5] = -2.4     # small loop
    W2[6, 5] = KV; b2[6] = -1.2     # vertical tube
    W2[7, 5] = KH; b2[7] = -1.2     # horizontal tube

    # ---------------- fc: PROBE ----------------
    # x_i = total activity of conv2 channel (5,6,7) over the 4x4 grid
    # class c in 0..7 encodes bits (x_0>t, x_1>t, x_2>t); classes 8,9 disabled
    Kbig = 100.0
    t = 0.05
    probe_ch = [5, 6, 7]
    for c in range(8):
        for i, ch in enumerate(probe_ch):
            s = 1.0 if (c >> i) & 1 else -1.0
            Wf[c, ch * 16:(ch + 1) * 16] += Kbig * s
            bf[c] += -Kbig * s * t
    bf[8] = -1000.0
    bf[9] = -1000.0

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
