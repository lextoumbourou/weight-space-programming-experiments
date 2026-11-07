Looking at the confusion matrix, class 1 is massively over-predicted (4701 times, should be ~1135) and class 7 is also over-predicted (1667 times). Classes 2, 3, 5, 8, 9 are severely under-predicted.

**Key fixes for step 3:**
1. **FC bias corrections** based on prediction imbalances — this should have the biggest impact
2. **More edge/stroke templates** to improve discrimination (horizontal strokes for 7/5/2/4, vertical for 1/4)
3. **Penalizing templates** (e.g., digit 1 should NOT have horizontal strokes; digits 2,3,5 should NOT have holes)

```python
import numpy as np

def build_weights():
    # ===== CONV1 (same as step 2) =====
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    for r in range(5):
        for c in range(5):
            conv1_w[0, 0, r, c] = np.exp(-((r-2)**2 + (c-2)**2) / 2.0)
    conv1_w[0, 0] /= conv1_w[0, 0].sum()
    conv1_w[0, 0] *= 1.5
    conv1_b[0] = -0.15

    conv1_w[1, 0] = np.array([
        [2,2,2,2,2],[1,1,1,1,1],[0,0,0,0,0],
        [-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2]], dtype=np.float32) * 0.04
    conv1_w[2, 0] = -conv1_w[1, 0]
    conv1_w[3, 0] = conv1_w[1, 0].T
    conv1_w[4, 0] = -conv1_w[3, 0]
    conv1_w[5, 0] = np.array([
        [2,1,0,-1,-2],[1,2,0,-2,-1],[0,0,0,0,0],
        [-1,-2,0,2,1],[-2,-1,0,1,2]], dtype=np.float32) * 0.04
    conv1_w[6, 0] = np.fliplr(conv1_w[5, 0])
    conv1_w[7, 0] = np.array([
        [1,2,2,2,1],[2,0,-2,0,2],[2,-2,-4,-2,2],
        [2,0,-2,0,2],[1,2,2,2,1]], dtype=np.float32) * 0.04

    # ===== CONV2 (same as step 2) =====
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    ck = np.zeros((5,5), dtype=np.float32)
    ck[1:4,1:4] = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32)
    ck /= ck.sum()
    for i in range(8):
        conv2_w[i, i] = ck * 4.0
    conv2_w[8,1]=ck*2.5;  conv2_w[8,2]=ck*2.5   # horiz stroke
    conv2_w[9,3]=ck*2.5;  conv2_w[9,4]=ck*2.5   # vert stroke
    conv2_w[10,1]=ck*2;   conv2_w[10,3]=ck*2     # TL corner
    conv2_w[11,1]=ck*2;   conv2_w[11,4]=ck*2     # TR corner
    conv2_w[12,2]=ck*2;   conv2_w[12,3]=ck*2     # BL corner
    conv2_w[13,2]=ck*2;   conv2_w[13,4]=ck*2     # BR corner
    conv2_w[14,5]=ck*3;   conv2_w[14,0]=ck*1.5   # \ diag+ink
    conv2_w[15,6]=ck*3;   conv2_w[15,0]=ck*1.5   # / diag+ink

    # ===== FC LAYER =====
    fc_w = np.zeros((10, 256), dtype=np.float32)
    # Bias corrections from step 2 prediction imbalance
    fc_b = np.array([0, -1.2, 0.8, 0.8, 0, 0.6, 0.3, -0.3, 1.0, 0.5],
                    dtype=np.float32)

    def idx(ch, r, c):
        return ch * 16 + r * 4 + c

    def T(d, ch, t, sc):
        arr = np.array(t, dtype=np.float32)
        arr -= arr.mean()  # zero-mean centering
        for r in range(4):
            for c in range(4):
                fc_w[d, idx(ch, r, c)] += arr[r, c] * sc

    s = 0.3

    # ---- Ink density (ch 0) ----
    T(0,0,[[0,1,1,0],[1,-1,-1,1],[1,-1,-1,1],[0,1,1,0]], s)
    T(1,0,[[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1]], s)
    T(2,0,[[0,.5,1,0],[-1,0,0,1],[0,1,0,-1],[0,1,1,.5]], s)
    T(3,0,[[0,.5,1,0],[-1,0,0,1],[-1,0,0,1],[0,.5,1,0]], s)
    T(4,0,[[.5,0,-1,1],[.5,.5,0,1],[0,1,1,1],[-1,-1,-1,1]], s)
    T(5,0,[[0,1,1,.5],[0,1,-1,-1],[-1,0,.5,1],[0,1,1,0]], s)
    T(6,0,[[0,.5,1,0],[0,1,-1,-1],[0,1,0,1],[0,.5,1,0]], s)
    T(7,0,[[-1,.5,1,1],[-1,0,1,0],[-1,.5,0,0],[-1,1,-1,-1]], s)
    T(8,0,[[0,1,1,0],[1,.5,.5,1],[1,.5,.5,1],[0,1,1,0]], s)
    T(9,0,[[0,1,1,0],[0,.5,0,1],[-1,0,0,1],[0,.5,1,0]], s)

    # ---- Hole detector (ch 7) ----
    T(0,7,[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]], s*.7)   # center hole
    T(1,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*.5) # no holes
    T(2,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*.3) # no holes
    T(3,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*.2) # no holes
    T(5,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*.2) # no holes
    T(6,7,[[0,-1,-1,0],[0,-1,-1,0],[0,1,1,0],[0,1,1,0]], s*.5) # bottom hole
    T(7,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*.3) # no holes
    T(8,7,[[0,1,1,0],[0,.5,.5,0],[0,.5,.5,0],[0,1,1,0]], s*.5) # holes everywhere
    T(9,7,[[0,1,1,0],[0,1,1,0],[0,-1,-1,0],[0,-1,-1,0]], s*.5) # top hole only

    # ---- Horizontal stroke (ch 8) ----
    T(7,8,[[0,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*.4)  # top bar of 7
    T(5,8,[[0,1,1,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*.3)  # top bar of 5
    T(2,8,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,1]], s*.4)  # bottom bar of 2
    T(4,8,[[0,0,0,0],[0,0,0,0],[0,1,1,1],[0,0,0,0]], s*.3)  # crossbar of 4
    T(1,8,[[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0]], s*.3)  # 1 has NO horiz

    # ---- Vertical stroke (ch 9) ----
    T(1,9,[[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1]], s*.3) # center vert
    T(4,9,[[-1,0,0,1],[-1,0,0,1],[-1,0,0,1],[-1,0,0,1]], s*.2)    # right vert

    # ---- Lower ink boundary (ch 1) ----
    T(7,1,[[0,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*.3)  # bottom of 7's top bar
    T(5,1,[[0,1,1,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*.2)  # bottom of 5's top bar

    # ---- Upper ink boundary (ch 2) ----
    T(2,2,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,.5]], s*.3) # top of 2's bottom bar

    # ---- Right ink boundary (ch 3) ----
    T(3,3,[[0,0,1,0],[0,0,0,1],[0,0,0,1],[0,0,1,0]], s*.3)  # right arcs of 3
    T(0,3,[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,1]], s*.2)  # right side of 0

    # ---- Left ink boundary (ch 4) ----
    T(0,4,[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], s*.2)  # left side of 0
    T(6,4,[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], s*.2)  # left side of 6

    return {
        'conv1.weight': conv1_w, 'conv1.bias': conv1_b,
        'conv2.weight': conv2_w, 'conv2.bias': conv2_b,
        'fc.weight': fc_w, 'fc.bias': fc_b,
    }
```
