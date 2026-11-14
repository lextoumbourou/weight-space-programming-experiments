import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: same 4 oriented line detectors as before (channels 0..3)
    #   (0 = horizontal, 1 = "/", 2 = vertical, 3 = "\"), channels 4..7 unused
    # ------------------------------------------------------------------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    yy, xx = np.mgrid[-2:3, -2:3].astype(float)   # yy: row offset (down), xx: col offset (right)
    for k in range(4):
        phi = k * math.pi / 4.0
        d = np.abs(xx * math.sin(phi) + yy * math.cos(phi))   # distance from line of direction phi
        g = np.exp(-d ** 2 / 2.0)          # ridge profile (sigma = 1 px)
        g = g - g.mean()                   # zero-sum
        g = g / g[g > 0].sum()             # ideal stroke -> response about 1
        conv1_w[k, 0] = g
        conv1_b[k] = -0.05

    # ------------------------------------------------------------------
    # conv2: single probe channel 0
    #   sums the vertical-stroke map (conv1 channel 2) over the 5 cells of the
    #   middle kernel row -> "vertical stroke energy crossing a 10px wide row band"
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    conv2_w[0, 2, 2, :] = 1.0

    # ------------------------------------------------------------------
    # fc: histogram read-out of s = feature(channel 0, cell row 1, col 1)
    #   (pool1 rows 4-5 = pixel rows ~10-13, columns spanning the image centre)
    #   output k wins when  t_k < s <= t_{k+1}
    # ------------------------------------------------------------------
    thresholds = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.90, 1.10])
    BETA = 10.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    idx = 0 * 16 + 1 * 4 + 1          # (channel 0, row 1, col 1) in flatten order
    for k in range(10):
        fc_w[k, idx] = BETA * k
        fc_b[k] = -BETA * thresholds[:k].sum()

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
