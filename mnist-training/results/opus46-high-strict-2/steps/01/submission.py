import numpy as np

def build_weights():
    # ===== CONV1: 8 basic feature detectors (1 input ch, 5x5 kernels) =====
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    # Filter 0: Gaussian ink/brightness detector
    for r in range(5):
        for c in range(5):
            conv1_w[0, 0, r, c] = np.exp(-((r - 2)**2 + (c - 2)**2) / 2.0)
    conv1_w[0, 0] = conv1_w[0, 0] / conv1_w[0, 0].sum() * 1.5  # sum=1.5
    conv1_b[0] = -0.3  # suppress background regions

    # Filter 1: Top edge  (ink above, background below)
    conv1_w[1, 0] = np.array([
        [ 2, 2, 2, 2, 2], [ 1, 1, 1, 1, 1], [ 0, 0, 0, 0, 0],
        [-1,-1,-1,-1,-1], [-2,-2,-2,-2,-2]], dtype=np.float32) * 0.04

    # Filter 2: Bottom edge (background above, ink below)
    conv1_w[2, 0] = -conv1_w[1, 0]

    # Filter 3: Left edge  (ink left, background right)
    conv1_w[3, 0] = conv1_w[1, 0].T

    # Filter 4: Right edge (background left, ink right)
    conv1_w[4, 0] = -conv1_w[3, 0]

    # Filter 5: Diagonal \ edge
    conv1_w[5, 0] = np.array([
        [ 2, 1, 0,-1,-2], [ 1, 2, 0,-2,-1], [ 0, 0, 0, 0, 0],
        [-1,-2, 0, 2, 1], [-2,-1, 0, 1, 2]], dtype=np.float32) * 0.04

    # Filter 6: Diagonal / edge
    conv1_w[6, 0] = np.fliplr(conv1_w[5, 0])

    # Filter 7: Hole/ring detector (bright surround, dark center)
    conv1_w[7, 0] = np.array([
        [ 1, 2, 2, 2, 1], [ 2, 0,-2, 0, 2], [ 2,-2,-4,-2, 2],
        [ 2, 0,-2, 0, 2], [ 1, 2, 2, 2, 1]], dtype=np.float32) * 0.04

    # ===== CONV2: 16 higher-level features (8 input ch, 5x5 kernels) =====
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)

    # Center-weighted smoothing kernel (3x3 core in 5x5, sums to 1)
    ck = np.zeros((5, 5), dtype=np.float32)
    ck[1:4, 1:4] = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32)
    ck /= ck.sum()

    # Ch 0-7: pass-through of each conv1 feature with spatial smoothing
    for i in range(8):
        conv2_w[i, i] = ck * 4.0

    # Ch 8: horizontal stroke detector (top edge + bottom edge)
    conv2_w[8, 1] = ck * 2.5;  conv2_w[8, 2] = ck * 2.5

    # Ch 9: vertical stroke detector (left edge + right edge)
    conv2_w[9, 3] = ck * 2.5;  conv2_w[9, 4] = ck * 2.5

    # Ch 10-13: four corner types
    conv2_w[10, 1] = ck * 2.0; conv2_w[10, 3] = ck * 2.0  # top-left
    conv2_w[11, 1] = ck * 2.0; conv2_w[11, 4] = ck * 2.0  # top-right
    conv2_w[12, 2] = ck * 2.0; conv2_w[12, 3] = ck * 2.0  # bottom-left
    conv2_w[13, 2] = ck * 2.0; conv2_w[13, 4] = ck * 2.0  # bottom-right

    # Ch 14-15: diagonal features combined with ink
    conv2_w[14, 5] = ck * 3.0; conv2_w[14, 0] = ck * 1.5  # \ diagonal
    conv2_w[15, 6] = ck * 3.0; conv2_w[15, 0] = ck * 1.5  # / diagonal

    # ===== FC LAYER: 10 x 256  (16 channels x 4 rows x 4 cols) =====
    # Flat index = channel*16 + row*4 + col
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    def idx(ch, r, c):
        return ch * 16 + r * 4 + c

    def T(digit, ch, template, sc):
        """Set FC weights: 4x4 spatial template on one feature channel."""
        for r in range(4):
            for c in range(4):
                fc_w[digit, idx(ch, r, c)] += template[r][c] * sc

    s = 0.2  # base weight scale

    # ---- Ink density templates (channel 0) ----
    # Each row: [col0, col1, col2, col3] for grid rows 0-3
    # Positive = expect ink, negative = expect no ink

    # Digit 0: oval/circle – ink on perimeter, empty center
    T(0, 0, [[ 0, .8, .8, 0],[.8,-.5,-.5,.8],[.8,-.5,-.5,.8],[ 0, .8, .8, 0]], s)
    # Digit 1: thin vertical stroke, center-ish
    T(1, 0, [[-.5,.3, .5,-.5],[-.5,.3, .5,-.5],[-.5,.3, .5,-.5],[-.5,.3, .5,-.5]], s)
    # Digit 2: top-right curve, diagonal, bottom bar
    T(2, 0, [[ 0, .5, .8, .3],[-.2, 0, .3, .8],[ 0, .8, .3,-.2],[ 0, .8, .8, .5]], s)
    # Digit 3: arcs on right side
    T(3, 0, [[ 0, .5, .8, .3],[-.3, 0, .3, .8],[-.3, 0, .3, .8],[ 0, .5, .8, .3]], s)
    # Digit 4: left diagonal + horizontal bar + right vertical
    T(4, 0, [[ .3, .3, 0, .8],[ .3, .5, .3, .8],[ .3, .8, .8, .8],[-.3,-.3, 0, .8]], s)
    # Digit 5: top bar, left descender, bottom-right curve
    T(5, 0, [[ 0, .8, .8, .5],[ 0, .8,-.2,-.3],[-.3, 0, .5, .8],[ 0, .8, .8, .3]], s)
    # Digit 6: top arc, bottom loop
    T(6, 0, [[ 0, .5, .8, .3],[ 0, .8, 0,-.3],[ 0, .8, .3, .8],[ 0, .5, .8, .3]], s)
    # Digit 7: top horizontal bar, diagonal down
    T(7, 0, [[ 0, .5, .8, .8],[-.3, 0, .5, .5],[-.3, .3, .5,-.2],[-.3, .5,-.2,-.3]], s)
    # Digit 8: two stacked loops, wider
    T(8, 0, [[ 0, .8, .8, 0],[ .3, .5, .5, .3],[ .3, .5, .5, .3],[ 0, .8, .8, 0]], s)
    # Digit 9: top loop, stroke going down-right
    T(9, 0, [[ 0, .8, .8, .3],[ 0, .5, .3, .8],[-.3, 0, .3, .8],[ 0, .5, .8, .3]], s)

    # ---- Hole/ring detector templates (channel 7) ----
    # 0: big central hole
    T(0, 7, [[ 0, 0, 0, 0],[ 0, .6, .6, 0],[ 0, .6, .6, 0],[ 0, 0, 0, 0]], s)
    # 1: no holes (penalise)
    T(1, 7, [[ 0,-.3,-.3, 0],[ 0,-.3,-.3, 0],[ 0,-.3,-.3, 0],[ 0,-.3,-.3, 0]], s)
    # 6: hole in bottom half only
    T(6, 7, [[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, .4, .4, 0],[ 0, .4, .4, 0]], s)
    # 7: no holes (penalise)
    T(7, 7, [[ 0,-.2,-.2, 0],[ 0,-.2,-.2, 0],[ 0,-.2,-.2, 0],[ 0,-.2,-.2, 0]], s)
    # 8: holes everywhere (two loops)
    T(8, 7, [[ 0, .3, .3, 0],[ 0, .5, .5, 0],[ 0, .5, .5, 0],[ 0, .3, .3, 0]], s)
    # 9: hole in top half only
    T(9, 7, [[ 0, .3, .3, 0],[ 0, .5, .5, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0]], s)

    # ---- A few edge-based cues ----
    # 7: strong top-edge at top row (the horizontal bar of 7)
    T(7, 1, [[ 0, .3, .5, .5],[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0]], s * 0.5)
    # 2: bottom-edge at bottom row (the horizontal bar of 2)
    T(2, 2, [[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, .5, .5, .3]], s * 0.5)

    return {
        'conv1.weight': conv1_w,
        'conv1.bias':   conv1_b,
        'conv2.weight': conv2_w,
        'conv2.bias':   conv2_b,
        'fc.weight':    fc_w,
        'fc.bias':      fc_b,
    }
