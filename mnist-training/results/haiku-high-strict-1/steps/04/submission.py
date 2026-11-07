import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters of size 1x5x5 (input is 1 channel)
    # ------------------------------------------------------------------
    c1w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    c1b = np.zeros(8, dtype=np.float64)

    def line_profile(dist):
        # Weight as a function of distance (pixels) from a stroke centreline.
        if dist == 0:
            return 0.125
        if dist == 1:
            return 0.0625
        if dist == 2:
            return -0.0625
        return 0.0

    for r in range(5):
        for c in range(5):
            c1w[0, 0, r, c] = line_profile(abs(c - 2))          # ch0 vertical stroke
            c1w[1, 0, r, c] = line_profile(abs(r - 2))          # ch1 horizontal stroke
            c1w[2, 0, r, c] = line_profile(abs(r + c - 4))      # ch2 '/' diagonal
            c1w[3, 0, r, c] = line_profile(abs(r - c))          # ch3 '\' diagonal
            c1w[4, 0, r, c] = 0.1 if (abs(r - 2) <= 1 and abs(c - 2) <= 1) else -0.02  # ch4 centre blob
            c1w[5, 0, r, c] = 0.04                              # ch5 local ink average
            if c >= 3:                                          # ch6 bright right / dark left
                c1w[6, 0, r, c] = 0.1
            elif c <= 1:
                c1w[6, 0, r, c] = -0.1
            if r <= 1:                                          # ch7 bright above / dark below
                c1w[7, 0, r, c] = 0.1
            elif r >= 3:
                c1w[7, 0, r, c] = -0.1

    # Thresholds so background (0) gives 0 after ReLU.
    c1b[:] = [-0.25, -0.25, -0.25, -0.25, -0.2, 0.0, -0.2, -0.2]

    # ------------------------------------------------------------------
    # conv2: 16 filters of size 8x5x5
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    # out 0..3: 3x3 blur of the oriented stroke channels
    for k in range(4):
        c2w[k, k, 1:4, 1:4] = 1.0 / 9.0
    # out 4: hole detector on the ink channel (ring mean minus centre mean)
    for r in range(5):
        for c in range(5):
            centre = (1 <= r <= 3) and (1 <= c <= 3)
            c2w[4, 5, r, c] = -1.0 / 9.0 if centre else 1.0 / 16.0
    # out 5: 3x3 blur of ink presence
    c2w[5, 5, 1:4, 1:4] = 1.0 / 9.0
    # out 6, 7: blur of the edge channels (unused by fc)
    c2w[6, 6, 1:4, 1:4] = 1.0 / 9.0
    c2w[7, 7, 1:4, 1:4] = 1.0 / 9.0
    # out 8..15: 5x5 box blur of conv1 channels 0..7 (unused by fc)
    for k in range(8):
        c2w[8 + k, k, :, :] = 1.0 / 25.0

    # ------------------------------------------------------------------
    # fc: 256 -> 10. Flatten index = channel*16 + row*4 + col.
    # Channels used: 5 = ink, 4 = hole, 0 = vertical, 1 = horizontal, 2 = '/'.
    # ------------------------------------------------------------------
    fcw = np.zeros((10, 256), dtype=np.float64)
    fcb = np.zeros(10, dtype=np.float64)

    INK_CH, HOLE_CH, VERT_CH, HORIZ_CH, SLASH_CH = 5, 4, 0, 1, 2

    # Raw shape templates (rows top->bottom, cols left->right).
    # Value scale: +1 = feature expected strongly, -1 = expected strongly absent.

    ink_raw = {
        0: [[-0.5, 0.5, 0.5, -0.5], [0.5, -1.0, -1.0, 0.5],
            [0.5, -1.0, -1.0, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        1: [[-1.0, 0.5, 0.5, -1.0]] * 4,
        2: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5], [0.5, 1.0, 1.0, 0.5]],
        3: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        4: [[-0.5, -0.5, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5, 0.5], [-0.5, -0.5, 0.5, -0.5]],
        5: [[0.5, 0.5, 0.5, 0.5], [0.5, 0.5, -0.5, -0.5],
            [0.5, 1.0, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5]],
        6: [[-0.5, 0.5, 0.5, -0.5], [0.5, 0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5, 0.5], [-0.5, 0.5, 0.5, 0.5]],
        7: [[0.5, 1.0, 1.0, 0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.0, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5]],
        8: [[-0.5, 0.5, 0.5, -0.5], [0.5, -0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        9: [[-0.5, 0.5, 0.5, -0.5], [0.5, -0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5], [-0.5, -0.5, 0.5, -0.5]],
    }

    def grid(cells, default=0.0):
        g = np.full((4, 4), default, dtype=np.float64)
        for (i, j), v in cells.items():
            g[i, j] = v
        return g

    no_hole = {(1, 1): -0.5, (1, 2): -0.5, (2, 1): -0.5, (2, 2): -0.5}
    hole_raw = {
        0: grid({(1, 1): 1.0, (1, 2): 1.0, (2, 1): 1.0, (2, 2): 1.0}),
        1: grid(no_hole), 2: grid(no_hole), 3: grid(no_hole),
        4: grid({(1, 1): 0.5}),
        5: grid(no_hole),
        6: grid({(2, 1): 1.0, (2, 2): 1.0}),
        7: grid(no_hole),
        8: grid({(1, 1): 0.6, (1, 2): 0.6, (2, 1): 0.6, (2, 2): 0.6}),
        9: grid({(1, 1): 1.0, (1, 2): 1.0}),
    }

    vert_raw = {d: grid({}) for d in range(10)}
    vert_raw[1] = grid({(i, j): 1.0 for i in range(4) for j in (1, 2)})
    vert_raw[4] = grid({(0, 2): 0.5, (1, 2): 0.5, (2, 2): 0.5, (3, 2): 0.5})
    vert_raw[7] = grid({(1, 2): 0.5, (2, 2): 0.5, (3, 2): 0.5})
    vert_raw[9] = grid({(2, 2): 0.5, (2, 3): 0.5, (3, 2): 0.5})
    for d in (0, 6, 8):
        vert_raw[d] = grid({(1, 0): 0.5, (2, 0): 0.5, (1, 3): 0.5, (2, 3): 0.5})
    vert_raw[5] = grid({(1, 0): 0.5})

    horiz_raw = {d: grid({}) for d in range(10)}
    horiz_raw[1] = grid({(i, j): -0.3 for i in range(4) for j in range(4)})
    bars_top_bottom = {(0, j): 0.3 for j in range(4)}
    bars_top_bottom.update({(3, j): 0.3 for j in range(4)})
    horiz_raw[2] = grid(bars_top_bottom)
    horiz_raw[3] = grid(bars_top_bottom)
    horiz_raw[4] = grid({(2, j): 0.3 for j in range(4)})
    horiz_raw[5] = grid({**{(0, j): 0.3 for j in range(4)},
                         **{(2, j): 0.3 for j in range(4)},
                         **{(3, j): 0.3 for j in range(4)}})
    horiz_raw[7] = grid({(0, j): 0.3 for j in range(4)})

    slash_raw = {d: grid({}) for d in range(10)}
    slash_raw[2] = grid({(1, 2): 0.5, (2, 1): 0.5})
    slash_raw[4] = grid({(0, 2): 0.5, (1, 1): 0.5, (2, 0): 0.5})
    slash_raw[6] = grid({(0, 2): 0.5, (1, 1): 0.5})
    slash_raw[7] = grid({(1, 2): 0.5, (2, 1): 0.5})

    # Map raw values to expected feature levels mu (prototype per cell).
    def ink_mu(v):
        return float(np.clip(0.45 + 0.4 * v, 0.02, 0.95))

    def feat_mu(v):
        # For hole / orientation channels, absence is the default (low level).
        return float(np.clip(0.05 + 0.55 * v, 0.02, 0.95))

    SIGMA2 = 0.2
    # Channel weights: how strongly each channel contributes to the distance.
    chan_weight = {INK_CH: 1.0, HOLE_CH: 1.0, VERT_CH: 0.7, HORIZ_CH: 0.5, SLASH_CH: 0.7}

    for d in range(10):
        blocks = [
            (INK_CH, np.vectorize(ink_mu)(np.array(ink_raw[d], dtype=np.float64))),
            (HOLE_CH, np.vectorize(feat_mu)(hole_raw[d])),
            (VERT_CH, np.vectorize(feat_mu)(vert_raw[d])),
            (HORIZ_CH, np.vectorize(feat_mu)(horiz_raw[d])),
            (SLASH_CH, np.vectorize(feat_mu)(slash_raw[d])),
        ]
        bias = 0.0
        for ch, mu in blocks:
            a = chan_weight[ch]
            mu = np.asarray(mu, dtype=np.float64)
            # Squared-distance score: linear part f*mu/sigma^2, constant part -mu^2/(2 sigma^2).
            fcw[d, ch * 16:(ch + 1) * 16] = (a * mu / SIGMA2).reshape(16)
            bias -= a * np.sum(mu ** 2) / (2.0 * SIGMA2)
        fcb[d] = bias

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
