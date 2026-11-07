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
            c1w[4, 0, r, c] = 0.1 if (abs(r - 2) <= 1 and abs(c - 2) <= 1) else -0.02  # ch4 blob
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
    # conv2: 16 filters of size 8x5x5 (unchanged from step 2)
    # ------------------------------------------------------------------
    c2w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    c2b = np.zeros(16, dtype=np.float64)

    for k in range(8):
        # out k: 3x3 box blur of conv1 channel k
        c2w[k, k, 1:4, 1:4] = 1.0 / 9.0
    for k in range(8):
        # out 8+k: 5x5 box blur of conv1 channel k (not used by fc)
        c2w[8 + k, k, :, :] = 1.0 / 25.0

    # ------------------------------------------------------------------
    # fc: 256 -> 10. Flatten index = channel*16 + row*4 + col.
    # ------------------------------------------------------------------
    fcw = np.zeros((10, 256), dtype=np.float64)

    INK_CH = 5    # conv2 channel: blurred ink presence
    HORIZ_CH = 1  # conv2 channel: blurred horizontal-stroke response

    # Hand-drawn 4x4 ink-occupancy templates (rows top->bottom, cols left->right).
    ink_templates = {
        0: [[-0.5, 0.5, 0.5, -0.5], [0.5, -1.0, -1.0, 0.5],
            [0.5, -1.0, -1.0, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        1: [[-1.0, 0.5, 0.5, -1.0]] * 4,
        2: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, -0.5], [0.5, 1.0, 1.0, 0.5]],
        3: [[-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5, 0.5], [-0.5, 0.5, 0.5, -0.5]],
        4: [[-0.5, -0.5, 0.5, -0.5], [-0.5, 0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5, 0.5], [-0.5, -0.5, 0.5, -0.5]],
        5: [[0.5, 1.0, 1.0, 0.5], [0.5, 0.5, -0.5, -0.5],
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

    # Horizontal-stroke evidence per row.
    horiz_rows = {
        1: {0: -0.3, 1: -0.3, 2: -0.3, 3: -0.3},
        2: {0: 0.3, 3: 0.3},
        3: {0: 0.3, 3: 0.3},
        4: {2: 0.3},
        5: {0: 0.3, 2: 0.3, 3: 0.3},
        7: {0: 0.3},
    }

    for d in range(10):
        # Zero-mean ink template so total ink does not favour a class.
        T = np.array(ink_templates[d], dtype=np.float64)
        T = T - T.mean()
        for i in range(4):
            for j in range(4):
                fcw[d, INK_CH * 16 + i * 4 + j] = T[i, j]
        for i, w in horiz_rows.get(d, {}).items():
            for j in range(4):
                fcw[d, HORIZ_CH * 16 + i * 4 + j] = w

    # Per-class offsets, adjusted by hand from the step-13 confusion matrix.
    # Step-13 predicted counts: 0:728, 1:1157, 2:1220, 3:988, 4:679,
    #                           5:1015, 6:542, 7:877, 8:1366, 9:1428.
    # 8 and 9 are over-predicted, so they come down. 0, 4, 6 and 7 are under-predicted,
    # so they go up. 2 is slightly over-predicted and is lowered.
    fcb = np.array([0.7, 0.0, -0.3, -0.22, 0.05, -0.28, 0.7, 0.0, 0.4, 0.4],
                   dtype=np.float64)

    return {
        "conv1.weight": c1w.astype(np.float32),
        "conv1.bias": c1b.astype(np.float32),
        "conv2.weight": c2w.astype(np.float32),
        "conv2.bias": c2b.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
