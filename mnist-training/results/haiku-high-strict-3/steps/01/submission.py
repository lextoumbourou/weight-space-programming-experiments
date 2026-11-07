import numpy as np


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters, each 1x5x5. Shape (out=8, in=1, 5, 5).
    # Coordinates: r = row offset inside the 5x5 window, c = column offset.
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)

    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing='ij')

    # Filter 0: vertical stroke detector. Strong on the centre column,
    # mildly positive on the neighbours, negative on the outer columns.
    v = np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.5))
    W1[0, 0] = v

    # Filter 1: horizontal stroke detector (transpose of filter 0).
    W1[1, 0] = v.T

    # Filter 2: '/' diagonal detector. Strong along r + c = 4.
    d = r + c - 4
    W1[2, 0] = np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.5))

    # Filter 3: '\' diagonal detector. Strong along r = c.
    d2 = r - c
    W1[3, 0] = np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.5))

    # Filter 4: centre-surround blob detector (positive 3x3 centre, weak negative ring).
    inner = (np.abs(r - 2) <= 1) & (np.abs(c - 2) <= 1)
    W1[4, 0] = np.where(inner, 0.2, -0.1)

    # Filter 5: upper-half minus lower-half (responds to top-heavy vs bottom-heavy ink).
    W1[5, 0] = np.where(r <= 1, 0.5, np.where(r == 2, 0.0, -0.5))

    # Filter 6: identity. Passes the centre pixel through, keeping raw shape information.
    W1[6, 0] = np.where((r == 2) & (c == 2), 1.0, 0.0)

    # Filter 7: local ink mass with a threshold, so only thick ink activates it.
    W1[7, 0] = 0.2
    b1[7] = -0.3

    # ------------------------------------------------------------------
    # conv2: 16 filters, each 8x5x5. Shape (out=16, in=8, 5, 5).
    # ------------------------------------------------------------------
    # Eight spatial patterns, one per conv2 "type".
    P = []
    # 0: vertical bar
    P.append(np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.3)))
    # 1: horizontal bar
    P.append(np.where(r == 2, 1.0, np.where((r == 1) | (r == 3), 0.3, -0.3)))
    # 2: '/' diagonal
    P.append(np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.3)))
    # 3: '\' diagonal
    P.append(np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.3)))
    # 4: 3x3 blob
    P.append(np.where(inner, 0.2, 0.0))
    # 5: centre point
    P.append(np.where((r == 2) & (c == 2), 1.0, 0.0))
    # 6: top half positive, bottom half negative
    P.append(np.where(r <= 1, 0.5, np.where(r >= 3, -0.5, 0.0)))
    # 7: bottom half positive, top half negative
    P.append(np.where(r >= 3, 0.5, np.where(r <= 1, -0.5, 0.0)))
    P = [p.astype(np.float32) for p in P]

    W2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.1, dtype=np.float32)  # small threshold
    for o in range(16):
        # Main input: channel o%8 with pattern o%8.
        W2[o, o % 8] += P[o % 8]
        # Weaker secondary input: channel (o+3)%8 with a different pattern.
        W2[o, (o + 3) % 8] += 0.5 * P[(o + 4) % 8]

    # ------------------------------------------------------------------
    # fc: 10 x 256. Input index = channel*16 + row*4 + col (4x4 pooled grid).
    # Each class gets a 4x4 "expected ink" template, applied to every channel.
    # ------------------------------------------------------------------
    T = np.array([
        # 0: ring
        [[0, 1, 1, 0], [1, -1, -1, 1], [1, -1, -1, 1], [0, 1, 1, 0]],
        # 1: centre vertical stroke
        [[-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1], [-1, 1, 1, -1]],
        # 2: top arc, diagonal, bottom bar
        [[0, 1, 1, 0], [-1, -1, 1, 0], [-1, 1, 0, -1], [1, 1, 1, 1]],
        # 3: right-side bulges, top and bottom arcs
        [[0, 1, 1, 0], [-1, -1, 1, 1], [-1, -1, 1, 1], [0, 1, 1, 0]],
        # 4: open top-left, cross bar, right stem
        [[-1, 0, 1, -1], [0, 1, 1, 0], [1, 1, 1, 1], [-1, -1, 1, -1]],
        # 5: top bar, left stem, bottom bowl
        [[1, 1, 1, 1], [1, -1, -1, -1], [0, 1, 1, 0], [-1, 1, 1, 0]],
        # 6: left loop from top to bottom
        [[-1, 0, 1, 1], [0, 1, -1, -1], [1, -1, -1, 1], [0, 1, 1, 0]],
        # 7: top bar, diagonal down to the left-centre
        [[1, 1, 1, 1], [-1, -1, 1, 0], [-1, 0, 1, 0], [-1, 0, 1, -1]],
        # 8: two stacked loops
        [[0, 1, 1, 0], [1, -1, -1, 1], [0, 1, 1, 0], [1, -1, -1, 1]],
        # 9: top loop with right stem descending
        [[0, 1, 1, 0], [1, -1, -1, 1], [-1, -1, 1, 1], [-1, 1, 1, 0]],
    ], dtype=np.float32)

    # Remove the per-cell mean across classes so no class is favoured
    # by generic activity. This is a fixed calculation on the templates.
    T = T - T.mean(axis=0, keepdims=True)

    Wfc = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            # Same template is used for every channel, with a global scale.
            Wfc[d_cls, ch * 16:(ch + 1) * 16] = 0.1 * T[d_cls].reshape(16)
    bfc = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc.astype(np.float32),
        "fc.bias": bfc.astype(np.float32),
    }
