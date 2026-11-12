import numpy as np
import math

def build_weights():
    thetas = [k * math.pi / 4 for k in range(4)]  # 0: horizontal, 45: "\", 90: vertical, 135: "/"
    off = np.arange(-2, 3)
    V, U = np.meshgrid(off, off, indexing='ij')

    # ================= conv1: identical to step 9 =================
    W1 = np.zeros((8, 1, 5, 5)); b1 = np.zeros(8)
    g1 = 3.0
    for k, th in enumerate(thetas):
        par = U * math.cos(th) + V * math.sin(th)
        perp = -U * math.sin(th) + V * math.cos(th)
        K = np.exp(-par**2 / 8.0) * np.exp(-perp**2 / (2 * 0.9**2))
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[k, 0] = g1 * K;     b1[k] = -0.6
        W1[k + 4, 0] = g1 * K; b1[k + 4] = -1.6

    # ================= conv2: identical to step 9 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)

    def set_pair(m, Z, g, t):
        for k in range(4):
            W2[2 * m, k] = g * Z[k];      W2[2 * m, k + 4] = -g * Z[k]
            W2[2 * m + 1, k] = g * Z[k];  W2[2 * m + 1, k + 4] = -g * Z[k]
        b2[2 * m] = -g * t
        b2[2 * m + 1] = -g * t - 1.0

    nb = np.zeros((5, 5))
    nb[1:4, 1:4] = [[0.4, 0.6, 0.4], [0.6, 1.0, 0.6], [0.4, 0.6, 0.4]]
    for k in range(4):
        Z = np.zeros((4, 5, 5)); Z[k] = nb
        set_pair(k, Z, 1.0, 0.6)

    rho = np.sqrt(U**2 + V**2)
    phi = np.arctan2(V, U)
    tang = phi + math.pi / 2
    ring = np.exp(-(rho - 2.0)**2 / (2 * 0.6**2)); ring[2, 2] = 0.0

    def ring_kernel(gate):
        Z = np.zeros((4, 5, 5))
        for k, th in enumerate(thetas):
            Z[k] = ring * np.cos(tang - th)**4 * gate
        Z /= np.sum(ring * np.maximum(gate, 0))
        for k in range(4):
            Z[k, 2, 2] -= 0.3
        return Z

    def arc_gate(phic):
        cs = np.cos(phi - phic)
        return np.maximum(0, cs) - 0.6 * np.maximum(0, -cs)**2

    set_pair(4, ring_kernel(np.ones((5, 5))), 4.0, 0.45)          # loop
    set_pair(5, ring_kernel(arc_gate(0.0)), 4.0, 0.45)
    set_pair(6, ring_kernel(arc_gate(-math.pi / 2)), 4.0, 0.45)
    set_pair(7, ring_kernel(arc_gate(math.pi / 2)), 4.0, 0.45)

    # ================= fc: PROBE of loop feature (m=4) =================
    # f_loop(r,c) = pool2[8,r,c] - pool2[9,r,c]
    A_top = np.zeros((16, 4, 4)); A_top[8, 0:2, :] = 1.0; A_top[9, 0:2, :] = -1.0
    A_bot = np.zeros((16, 4, 4)); A_bot[8, 2:4, :] = 1.0; A_bot[9, 2:4, :] = -1.0
    A_top = A_top.reshape(256); A_bot = A_bot.reshape(256)
    lev = [0.0, 0.5, 1.5]       # bin boundaries at 0.25 and 1.0
    M = 40.0
    Wfc = np.zeros((10, 256)); bfc = np.zeros(10)
    for i in range(3):          # top-half bin
        for j in range(3):      # bottom-half bin
            cls = 3 * i + j
            Wfc[cls] = M * (lev[i] * A_top + lev[j] * A_bot)
            bfc[cls] = -M * 0.5 * (lev[i]**2 + lev[j]**2)
    bfc[9] = -1e4               # unused

    return {
        'conv1.weight': W1.astype(np.float32),
        'conv1.bias': b1.astype(np.float32),
        'conv2.weight': W2.astype(np.float32),
        'conv2.bias': b2.astype(np.float32),
        'fc.weight': Wfc.astype(np.float32),
        'fc.bias': bfc.astype(np.float32),
    }
