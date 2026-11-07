import numpy as np
import math

def build_weights():
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)

    # ---------------- conv1 ----------------
    # ch0: ink (Gaussian blur)
    G = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            G[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / 2.0)
    W1[0, 0] = G / G.sum()
    b1[0] = -0.05
    # ch1..4: oriented line detectors (1=horiz, 2=vert, 3="\", 4="/")
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

    # ---------------- conv2: pass-through (centre tap) of conv1 ch0..4 ----------------
    # final feature (ch, cell) = max of conv1 ch over an ~8px image window
    for k in range(5):
        W2[k, k, 2, 2] = 1.0

    # ---------------- fc: PROBE ----------------
    # tests: (conv2 channel, cell index = row*4+col); test true if feature > thr
    tests = [(1, 0), (1, 1), (1, 2)]   # horizontal presence in top-row cells 0,1,2
    thr = 0.35
    Kbig = 100.0
    for c in range(8):
        for i, (ch, cell) in enumerate(tests):
            s = 1.0 if (c >> i) & 1 else -1.0
            Wf[c, ch * 16 + cell] += Kbig * s
            bf[c] += -Kbig * s * thr
    bf[8] = -1e4
    bf[9] = -1e4

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
