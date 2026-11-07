Looking at the confusion matrix, almost everything is predicted as class 8. The root cause: class 8's FC template has the highest sum of positive weights (all positive, no negative values), so it dominates for any input. 

**Key fix for step 2:** Make all FC templates zero-mean by subtracting each template's mean before applying. This prevents any class from being favored simply because its template has more positive weight. I also reduce conv1 bias[0] from -0.3 to -0.15 to let more activations through, and increase FC scale from 0.2 to 0.3.

```python
import numpy as np

def build_weights():
    # ===== CONV1: 8 feature detectors (same as step 1, reduced bias) =====
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    # 0: Gaussian ink detector
    for r in range(5):
        for c in range(5):
            conv1_w[0, 0, r, c] = np.exp(-((r - 2)**2 + (c - 2)**2) / 2.0)
    conv1_w[0, 0] = conv1_w[0, 0] / conv1_w[0, 0].sum() * 1.5
    conv1_b[0] = -0.15  # lowered to let more ink signal through

    # 1-4: oriented edge detectors
    conv1_w[1, 0] = np.array([
        [ 2, 2, 2, 2, 2],[ 1, 1, 1, 1, 1],[ 0, 0, 0, 0, 0],
        [-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2]], dtype=np.float32) * 0.04
    conv1_w[2, 0] = -conv1_w[1, 0]           # bottom edge
    conv1_w[3, 0] = conv1_w[1, 0].T           # left edge
    conv1_w[4, 0] = -conv1_w[3, 0]            # right edge

    # 5-6: diagonal edge detectors
    conv1_w[5, 0] = np.array([
        [ 2, 1, 0,-1,-2],[ 1, 2, 0,-2,-1],[ 0, 0, 0, 0, 0],
        [-1,-2, 0, 2, 1],[-2,-1, 0, 1, 2]], dtype=np.float32) * 0.04
    conv1_w[6, 0] = np.fliplr(conv1_w[5, 0])  # / diagonal

    # 7: hole/ring detector (bright surround, dark center)
    conv1_w[7, 0] = np.array([
        [ 1, 2, 2, 2, 1],[ 2, 0,-2, 0, 2],[ 2,-2,-4,-2, 2],
        [ 2, 0,-2, 0, 2],[ 1, 2, 2, 2, 1]], dtype=np.float32) * 0.04

    # ===== CONV2: 16 higher-level features (unchanged) =====
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    ck = np.zeros((5, 5), dtype=np.float32)
    ck[1:4, 1:4] = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32)
    ck /= ck.sum()
    for i in range(8):                                       # pass-through
        conv2_w[i, i] = ck * 4.0
    conv2_w[8, 1] = ck*2.5;  conv2_w[8, 2] = ck*2.5        # horiz stroke
    conv2_w[9, 3] = ck*2.5;  conv2_w[9, 4] = ck*2.5        # vert stroke
    conv2_w[10,1] = ck*2.0;  conv2_w[10,3] = ck*2.0        # TL corner
    conv2_w[11,1] = ck*2.0;  conv2_w[11,4] = ck*2.0        # TR corner
    conv2_w[12,2] = ck*2.0;  conv2_w[12,3] = ck*2.0        # BL corner
    conv2_w[13,2] = ck*2.0;  conv2_w[13,4] = ck*2.0        # BR corner
    conv2_w[14,5] = ck*3.0;  conv2_w[14,0] = ck*1.5        # \ diag+ink
    conv2_w[15,6] = ck*3.0;  conv2_w[15,0] = ck*1.5        # / diag+ink

    # ===== FC LAYER: zero-mean templates =====
    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)

    def idx(ch, r, c):
        return ch * 16 + r * 4 + c

    def T(d, ch, t, sc):
        """Add a 4x4 template to fc_w for digit d on channel ch.
           Template is zero-mean centered before scaling."""
        arr = np.array(t, dtype=np.float32)
        arr -= arr.mean()          # KEY FIX: zero-mean centering
        for r in range(4):
            for c in range(4):
                fc_w[d, idx(ch, r, c)] += arr[r, c] * sc

    s = 0.3  # increased scale for sharper logit differences

    # -- Ink density templates (channel 0): where is ink on 4x4 grid? --
    # 0: circle – ink on perimeter, empty center
    T(0, 0, [[ 0, 1, 1, 0],[ 1,-1,-1, 1],[ 1,-1,-1, 1],[ 0, 1, 1, 0]], s)
    # 1: thin vertical stroke in center
    T(1, 0, [[-1, 0, 1,-1],[-1, 0, 1,-1],[-1, 0, 1,-1],[-1, 0, 1,-1]], s)
    # 2: top-right curve, diagonal, bottom bar
    T(2, 0, [[ 0,.5, 1, 0],[-1, 0, 0, 1],[ 0, 1, 0,-1],[ 0, 1, 1,.5]], s)
    # 3: right-side arcs
    T(3, 0, [[ 0,.5, 1, 0],[-1, 0, 0, 1],[-1, 0, 0, 1],[ 0,.5, 1, 0]], s)
    # 4: left diagonal + crossbar + right vertical
    T(4, 0, [[.5, 0,-1, 1],[.5,.5, 0, 1],[ 0, 1, 1, 1],[-1,-1,-1, 1]], s)
    # 5: top bar, left descender, bottom-right curve
    T(5, 0, [[ 0, 1, 1,.5],[ 0, 1,-1,-1],[-1, 0,.5, 1],[ 0, 1, 1, 0]], s)
    # 6: top arc, bottom loop
    T(6, 0, [[ 0,.5, 1, 0],[ 0, 1,-1,-1],[ 0, 1, 0, 1],[ 0,.5, 1, 0]], s)
    # 7: top bar, diagonal going down
    T(7, 0, [[-1,.5, 1, 1],[-1, 0, 1, 0],[-1,.5, 0, 0],[-1, 1,-1,-1]], s)
    # 8: figure-eight – ink on perimeter AND some in center
    T(8, 0, [[ 0, 1, 1, 0],[ 1,.5,.5, 1],[ 1,.5,.5, 1],[ 0, 1, 1, 0]], s)
    # 9: top loop, right stroke going down
    T(9, 0, [[ 0, 1, 1, 0],[ 0,.5, 0, 1],[-1, 0, 0, 1],[ 0,.5, 1, 0]], s)

    # -- Hole detector templates (channel 7) --
    # 0: big hole in center
    T(0, 7, [[ 0, 0, 0, 0],[ 0, 1, 1, 0],[ 0, 1, 1, 0],[ 0, 0, 0, 0]], s*0.7)
    # 1: no holes expected (penalise holes)
    T(1, 7, [[ 0, 0, 0, 0],[ 0,-1,-1, 0],[ 0,-1,-1, 0],[ 0, 0, 0, 0]], s*0.5)
    # 6: hole only in bottom half
    T(6, 7, [[ 0,-1,-1, 0],[ 0,-1,-1, 0],[ 0, 1, 1, 0],[ 0, 1, 1, 0]], s*0.5)
    # 7: no holes expected
    T(7, 7, [[ 0, 0, 0, 0],[ 0,-1,-1, 0],[ 0,-1,-1, 0],[ 0, 0, 0, 0]], s*0.3)
    # 8: holes everywhere (two loops)
    T(8, 7, [[ 0, 1, 1, 0],[ 0,.5,.5, 0],[ 0,.5,.5, 0],[ 0, 1, 1, 0]], s*0.5)
    # 9: hole only in top half
    T(9, 7, [[ 0, 1, 1, 0],[ 0, 1, 1, 0],[ 0,-1,-1, 0],[ 0,-1,-1, 0]], s*0.5)

    # -- Edge feature templates for extra discrimination --
    # 7: strong top edge at top row (horizontal bar of 7)
    T(7, 1, [[ 0,.5, 1, 1],[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0]], s*0.4)
    # 5: top edge at top (top bar of 5)
    T(5, 1, [[ 0, 1, 1,.5],[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0]], s*0.3)
    # 2: bottom edge at bottom (base bar of 2)
    T(2, 2, [[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 0, 0, 0],[ 0, 1, 1,.5]], s*0.4)
    # 3: right edges throughout
    T(3, 4, [[ 0, 0, 0, 1],[ 0, 0, 0, 1],[ 0, 0, 0, 1],[ 0, 0, 0, 1]], s*0.3)
    # 1: strong vertical stroke in center columns
    T(1, 9, [[-1, 0, 1,-1],[-1, 0, 1,-1],[-1, 0, 1,-1],[-1, 0, 1,-1]], s*0.3)

    return {
        'conv1.weight': conv1_w,
        'conv1.bias':   conv1_b,
        'conv2.weight': conv2_w,
        'conv2.bias':   conv2_b,
        'fc.weight':    fc_w,
        'fc.bias':      fc_b,
    }
```
