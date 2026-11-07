import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 3: where do LOOP_s (ch5) and LOOP_l (ch6) fire?
    # conv1/conv2 identical to step 16.
    # ==================================================================
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))
        w = w - w.mean()
        w = w / w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()
    W1[4, 0] = g;        b1[4] = -0.1
    W1[5, 0] = -2.5 * g; b1[5] = 1.0
    W1[6, 0] = 3.0 * g;  b1[6] = -0.3
    W1[7, 0] = 3.0 * g;  b1[7] = -1.3

    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def sat(ch, r, c, w):
        W2[ch, 6, r, c] += w
        W2[ch, 7, r, c] -= w

    near = {'U': (1, 2), 'D': (3, 2), 'L': (2, 1), 'R': (2, 3)}
    far = {'U': (0, 2), 'D': (4, 2), 'L': (2, 0), 'R': (2, 4)}

    def detector(ch, taps, sides_req, sides_forbid=()):
        W2[ch, 5, 2, 2] = 1.0
        for sd in sides_req:
            sat(ch, *taps[sd], 1.0)
        for sd in sides_forbid:
            sat(ch, *taps[sd], -1.0)
        b2[ch] = -(len(sides_req) + 1 - 0.6)

    detector(5, near, 'UDLR')
    detector(6, far, 'UDLR')
    detector(7, near, 'LR')
    detector(8, near, 'UD')
    detector(9, far, 'LR')
    detector(10, far, 'UD')
    detector(11, far, 'UDR', 'L')
    detector(12, far, 'UDL', 'R')
    detector(13, far, 'LRD', 'U')
    detector(14, far, 'LRU', 'D')

    # fc probe
    beta = 10.0
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    idx = lambda c, i, j: c * 16 + i * 4 + j
    for r in range(4):
        for j in range(4):
            Wf[r, idx(5, r, j)] = beta / 0.1         # LOOP_s in row r
            Wf[4 + r, idx(6, r, j)] = beta / 0.1     # LOOP_l in row r
    bf[8] = beta * 1.0                               # no loop
    bf[9] = -100.0

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
