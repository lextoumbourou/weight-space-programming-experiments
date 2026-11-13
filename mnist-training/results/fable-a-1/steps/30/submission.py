import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # DIAGNOSTIC STEP: three binary facts read out jointly; predicted class =
    # 3-bit number:
    #   bit 0 (value 1): "\" presence in cell (row 3, col 1) above 0.5
    #   bit 1 (value 2): "\" presence in cell (row 3, col 3) above 0.5
    #   bit 2 (value 4): loop detector (4 sizes) fires in the upper half
    # Classes 8, 9 are unused.
    # ------------------------------------------------------------------
    ORI_FEATS = [(3, 3, 1), (3, 3, 3)]   # (orientation k, row a, col b)
    HOLE_TAU = 0.05                      # loop evidence threshold
    K = 40.0                             # sharpness of the readout

    T0 = 0.25
    CLIP = 1.2
    C1_BIAS = -0.1
    CORNER_BIAS = -1.05
    BLANK_W = -0.5
    THETA = 0.9
    CC = 0.25

    # conv1, filters 0..3: oriented line detectors
    def line_filter(theta_deg):
        th = math.radians(theta_deg)
        f = np.zeros((5, 5), dtype=np.float64)
        for r in range(5):
            for c in range(5):
                y = r - 2
                x = c - 2
                u = abs(x * math.sin(th) + y * math.cos(th))
                f[r, c] = np.interp(u, [0.0, 1.0, 2.0, 3.0], [2.0, 0.0, -1.0, -1.0])
        pos = f[f > 0].sum()
        neg = -f[f < 0].sum()
        f[f < 0] *= pos / neg
        return f / pos

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS

    # conv1, filters 4..7: inner-corner detectors
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0
    TL[2:5, 0:2] = 1.0 / 6.0
    TL[2:4, 2:4] = BLANK_W
    conv1_w[4, 0] = TL
    conv1_w[5, 0] = TL[:, ::-1]
    conv1_w[6, 0] = TL[::-1, :]
    conv1_w[7, 0] = TL[::-1, ::-1]
    conv1_b[4:8] = CORNER_BIAS

    # conv2, channels 0..7: clipped orientation presence
    #   channel k   = relu(boxsum3x3(orientation k) - T0)
    #   channel k+4 = relu(boxsum3x3(orientation k) - T0 - CLIP)
    #   presence y  = (channel k - channel k+4) / CLIP   in [0, 1]
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # conv2, channels 8..11: loop detectors for 4 loop sizes
    sizes = [(1, 1), (2, 2), (2, 1), (1, 2)]
    for i, (sy, sx) in enumerate(sizes):
        ch = 8 + i
        r0 = (4 - sy) // 2
        c0 = (4 - sx) // 2
        conv2_w[ch, 4, r0, c0] += 1.0
        conv2_w[ch, 5, r0, c0 + sx] += 1.0
        conv2_w[ch, 6, r0 + sy, c0] += 1.0
        conv2_w[ch, 7, r0 + sy, c0 + sx] += 1.0
        conv2_b[ch] = -THETA

    # conv2, channels 12..15: absence-coded saturating corner features (kept, unused here)
    for t in range(4):
        conv2_w[12 + t, 4 + t, 1:4, 1:4] = -1.0
        conv2_b[12 + t] = CC

    # fc: joint readout of the three binary facts.
    # logit(outcome o) = K * sum_i sign(o, i) * (value_i - threshold_i)
    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)
    for o in range(8):
        # bits 0, 1: orientation presence features
        for i, (k, a, b) in enumerate(ORI_FEATS):
            sgn = 1.0 if (o >> i) & 1 else -1.0
            fc_w[o, k * 16 + a * 4 + b] += K * sgn / CLIP
            fc_w[o, (k + 4) * 16 + a * 4 + b] += -K * sgn / CLIP
            fc_b[o] += -K * sgn * 0.5
        # bit 2: loop evidence in the upper half (final rows 0, 1 of channels 8..11)
        sgn = 1.0 if (o >> 2) & 1 else -1.0
        for ch in range(8, 12):
            for a in (0, 1):
                for b in range(4):
                    fc_w[o, ch * 16 + a * 4 + b] += K * sgn
        fc_b[o] += -K * sgn * HOLE_TAU
    fc_b[8] = -1000.0
    fc_b[9] = -1000.0

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
