Looking at the confusion matrix, class 8 is now massively over-predicted (2450 times, bias was too high at +1.0). Class 3 and 7 also over-predicted. Key confusions: 4→8 (648), 9→8 (645), 6→8 (450), 7→3 (415), 1→7 (413).

**Step 4 fixes:**
1. **Recalibrated biases** using log(target/predicted) from step 3
2. **Increased scale** to 0.4 for sharper discrimination
3. **More discriminative templates**: horizontal stroke (ch 8) and vertical stroke (ch 9) templates for ALL digits, with explicit negative weights where features should NOT appear
4. **Strengthened hole templates** for better 0/6/8/9 discrimination

```python
import numpy as np

def build_weights():
    # ===== CONV1 (unchanged) =====
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)
    for r in range(5):
        for c in range(5):
            conv1_w[0, 0, r, c] = np.exp(-((r-2)**2 + (c-2)**2) / 2.0)
    conv1_w[0, 0] /= conv1_w[0, 0].sum()
    conv1_w[0, 0] *= 1.5
    conv1_b[0] = -0.15
    e = np.array([[2,2,2,2,2],[1,1,1,1,1],[0,0,0,0,0],
                   [-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2]], dtype=np.float32)*0.04
    conv1_w[1,0]=e; conv1_w[2,0]=-e; conv1_w[3,0]=e.T; conv1_w[4,0]=-e.T
    d = np.array([[2,1,0,-1,-2],[1,2,0,-2,-1],[0,0,0,0,0],
                   [-1,-2,0,2,1],[-2,-1,0,1,2]], dtype=np.float32)*0.04
    conv1_w[5,0]=d; conv1_w[6,0]=np.fliplr(d)
    conv1_w[7,0]=np.array([[1,2,2,2,1],[2,0,-2,0,2],[2,-2,-4,-2,2],
                            [2,0,-2,0,2],[1,2,2,2,1]], dtype=np.float32)*0.04

    # ===== CONV2 (unchanged) =====
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    ck = np.zeros((5,5), dtype=np.float32)
    ck[1:4,1:4] = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32)
    ck /= ck.sum()
    for i in range(8): conv2_w[i,i] = ck*4.0
    conv2_w[8,1]=ck*2.5;  conv2_w[8,2]=ck*2.5
    conv2_w[9,3]=ck*2.5;  conv2_w[9,4]=ck*2.5
    conv2_w[10,1]=ck*2; conv2_w[10,3]=ck*2
    conv2_w[11,1]=ck*2; conv2_w[11,4]=ck*2
    conv2_w[12,2]=ck*2; conv2_w[12,3]=ck*2
    conv2_w[13,2]=ck*2; conv2_w[13,4]=ck*2
    conv2_w[14,5]=ck*3; conv2_w[14,0]=ck*1.5
    conv2_w[15,6]=ck*3; conv2_w[15,0]=ck*1.5

    # ===== FC LAYER =====
    fc_w = np.zeros((10, 256), dtype=np.float32)
    # Recalibrated biases from step 3 prediction counts
    fc_b = np.array([0.3, -1.1, 0.7, 0.6, 0.4, 0.7, 0.6, -0.5, 0.35, 0.9],
                    dtype=np.float32)

    def idx(ch, r, c):
        return ch * 16 + r * 4 + c
    def T(d, ch, t, sc):
        arr = np.array(t, dtype=np.float32)
        arr -= arr.mean()
        for r in range(4):
            for c in range(4):
                fc_w[d, idx(ch, r, c)] += arr[r, c] * sc

    s = 0.4  # increased from 0.3

    # == INK DENSITY (ch 0) ==
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

    # == HOLES (ch 7) — strengthened ==
    T(0,7,[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]], s*1.0)   # center hole
    T(1,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*0.5) # no holes
    T(2,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*0.3)
    T(3,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*0.2)
    T(4,7,[[0,1,0,0],[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0]], s*0.3)
    T(5,7,[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*0.2)
    T(6,7,[[0,-1,-1,0],[0,-1,-1,0],[0,1,1,0],[0,1,1,0]], s*0.7)  # bottom hole only
    T(7,7,[[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0]], s*0.4) # no holes
    T(8,7,[[0,1,1,0],[0,.5,.5,0],[0,.5,.5,0],[0,1,1,0]], s*0.7)  # holes everywhere
    T(9,7,[[0,1,1,0],[0,1,1,0],[0,-1,-1,0],[0,-1,-1,0]], s*0.7)  # top hole only

    # == HORIZONTAL STROKE (ch 8) — with negative where NOT expected ==
    T(0,8,[[0,1,1,0],[0,-1,-1,0],[0,-1,-1,0],[0,1,1,0]], s*0.3)  # top+bottom oval
    T(1,8,[[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0],[0,-1,-1,0]], s*0.4) # NO horiz
    T(2,8,[[0,-1,-1,0],[0,0,0,0],[0,0,0,0],[0,1,1,1]], s*0.4)   # bottom bar only
    T(3,8,[[0,.5,.5,0],[0,0,0,0],[0,.5,.5,0],[0,.5,.5,0]], s*0.2)
    T(4,8,[[0,-1,-1,0],[0,0,0,0],[0,1,1,1],[0,-1,-1,0]], s*0.4) # crossbar row2
    T(5,8,[[0,1,1,0],[0,0,0,0],[0,-1,-1,0],[0,0,0,0]], s*0.3)   # top bar only
    T(6,8,[[0,-1,-1,0],[0,0,0,0],[0,.5,.5,0],[0,.5,.5,0]], s*0.2)
    T(7,8,[[0,1,1,1],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]], s*0.5) # strong top bar
    T(8,8,[[0,.5,.5,0],[0,.5,.5,0],[0,.5,.5,0],[0,.5,.5,0]], s*0.2)
    T(9,8,[[0,1,1,0],[0,0,0,0],[0,-1,-1,0],[0,0,0,0]], s*0.3)

    # == VERTICAL STROKE (ch 9) ==
    T(0,9,[[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1]], s*0.3)   # both sides
    T(1,9,[[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1],[-1,0,1,-1]], s*0.4) # center only
    T(4,9,[[-1,0,0,1],[-1,0,0,1],[-1,0,0,1],[-1,0,0,1]], s*0.4) # right only
    T(6,9,[[1,0,0,-1],[1,0,0,-1],[1,0,0,-1],[1,0,0,-1]], s*0.2) # left only
    T(8,9,[[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1]], s*0.2)   # both sides
    T(9,9,[[-1,0,0,1],[-1,0,0,1],[-1,0,0,1],[-1,0,0,1]], s*0.3) # right only

    # == EDGE TEMPLATES for key pairs ==
    T(7,1,[[0,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*0.3) # 7: bottom-of-ink at top
    T(2,2,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,.5]], s*0.3) # 2: top-of-ink at bottom
    T(5,1,[[0,1,1,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], s*0.2)
    T(3,3,[[0,0,1,0],[0,0,0,1],[0,0,0,1],[0,0,1,0]], s*0.3) # 3: right boundary
    T(0,3,[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,1]], s*0.2)
    T(0,4,[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], s*0.2) # 0: left boundary
    T(6,4,[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], s*0.2)

    return {
        'conv1.weight': conv1_w, 'conv1.bias': conv1_b,
        'conv2.weight': conv2_w, 'conv2.bias': conv2_b,
        'fc.weight': fc_w, 'fc.bias': fc_b,
    }
```
