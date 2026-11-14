import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1 (unchanged)
    #   channels 0..3: oriented line detectors (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\")
    #   channels 4..7: polarity edge detectors
    #       4: ink to the RIGHT   5: ink to the LEFT   6: ink BELOW   7: ink ABOVE
    # ------------------------------------------------------------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    yy, xx = np.mgrid[-2:3, -2:3].astype(float)
    for k in range(4):
        phi = k * math.pi / 4.0
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))
        g = np.exp(-d ** 2 / 2.0)
        g = g - g.mean()
        g = g / g[g > 0].sum()
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05
    c = np.array([-0.5, -1.0, 0.0, 1.0, 0.5])   # derivative profile across the edge
    r = np.array([0.5, 1.0, 1.0, 1.0, 0.5])     # smoothing along the edge
    conv1_w[4, 0] = np.outer(r, c) / 6.0        # ink right
    conv1_w[5, 0] = -np.outer(r, c) / 6.0       # ink left
    conv1_w[6, 0] = np.outer(c, r) / 6.0        # ink below
    conv1_w[7, 0] = -np.outer(c, r) / 6.0       # ink above
    conv1_b[4:8] = -0.1

    # ------------------------------------------------------------------
    # conv2 channels 0..7: smoothed orientation maps on two staggered grids
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    t = np.array([0.5, 1.0, 0.5])
    k3 = np.outer(t, t) / 2.0
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = k3
        conv2_w[4 + k, k, 2:5, 2:5] = k3

    # ------------------------------------------------------------------
    # conv2 channels 8..13: loci features of the background point at the kernel centre
    #   8 : wall on the right, left ray open        9 : wall on the left, right ray open
    #   10: floor below, ray upwards open           11: ceiling above, ray downwards open
    #   12: walls left AND right                    13: walls above AND below
    # Walls = inward-facing polarity edges in the centre cell or up to 2 cells out.
    # Open ray = no stroke crossing the ray (perpendicular line / edges along the ray).
    # ------------------------------------------------------------------
    lat = (0.25, 0.5, 0.25)     # lateral smoothing across the ray
    KINH = 1.5                  # veto strength

    def block_R(ch):
        for a, wl in zip((1, 2, 3), lat):
            for b in (2, 3, 4):
                conv2_w[ch, 4, a, b] += wl

    def block_L(ch):
        for a, wl in zip((1, 2, 3), lat):
            for b in (0, 1, 2):
                conv2_w[ch, 5, a, b] += wl

    def block_D(ch):
        for b, wl in zip((1, 2, 3), lat):
            for a in (2, 3, 4):
                conv2_w[ch, 6, a, b] += wl

    def block_U(ch):
        for b, wl in zip((1, 2, 3), lat):
            for a in (0, 1, 2):
                conv2_w[ch, 7, a, b] += wl

    def veto(ch, cells, chans, strength=1.0):
        for (a, b) in cells:
            for cc in chans:
                conv2_w[ch, cc, a, b] -= KINH * strength

    LINES = (0, 1, 2, 3)
    # 8: wall right / left open
    block_R(8)
    veto(8, [(2, 0), (2, 1)], (2, 4, 5)); veto(8, [(2, 0), (2, 1)], (1, 3), 0.5)
    veto(8, [(2, 2)], LINES); veto(8, [(2, 2)], (5,))
    # 9: wall left / right open
    block_L(9)
    veto(9, [(2, 3), (2, 4)], (2, 4, 5)); veto(9, [(2, 3), (2, 4)], (1, 3), 0.5)
    veto(9, [(2, 2)], LINES); veto(9, [(2, 2)], (4,))
    # 10: floor below / open above
    block_D(10)
    veto(10, [(0, 2), (1, 2)], (0, 6, 7)); veto(10, [(0, 2), (1, 2)], (1, 3), 0.5)
    veto(10, [(2, 2)], LINES); veto(10, [(2, 2)], (7,))
    # 11: ceiling above / open below
    block_U(11)
    veto(11, [(3, 2), (4, 2)], (0, 6, 7)); veto(11, [(3, 2), (4, 2)], (1, 3), 0.5)
    veto(11, [(2, 2)], LINES); veto(11, [(2, 2)], (6,))
    conv2_b[8:12] = -0.4
    # 12: walls left and right; 13: walls above and below
    block_L(12); block_R(12); veto(12, [(2, 2)], LINES)
    block_U(13); block_D(13); veto(13, [(2, 2)], LINES)
    conv2_b[12:14] = -1.9       # one wall alone must not be enough

    # ------------------------------------------------------------------
    # fc: joint 3x3 histogram probe of two scalars (same as step 6)
    #   s1 = sum of channel 10 (floor / open above) over rows 0-1, cols 1-2
    #   s2 = sum of channel 13 (walls above+below)  over rows 0-1, cols 1-2
    #   predicted index = 3 * bin(s1) + bin(s2)
    # ------------------------------------------------------------------
    def region_vec(ch, rows, cols):
        v = np.zeros((16, 4, 4))
        for i in rows:
            for j in cols:
                v[ch, i, j] = 1.0
        return v.reshape(-1)

    v1 = region_vec(10, (0, 1), (1, 2))
    v2 = region_vec(13, (0, 1), (1, 2))
    th1 = (0.15, 1.0)     # bin edges for s1
    th2 = (0.15, 0.8)     # bin edges for s2
    cum1 = (0.0, th1[0], th1[0] + th1[1])
    cum2 = (0.0, th2[0], th2[0] + th2[1])
    BETA = 10.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for b1 in range(3):
        for b2 in range(3):
            k = 3 * b1 + b2
            fc_w[k] = (BETA * (b1 * v1 + b2 * v2)).astype(np.float32)
            fc_b[k] = -BETA * (cum1[b1] + cum2[b2])
    fc_b[9] = -1000.0     # unused output

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
