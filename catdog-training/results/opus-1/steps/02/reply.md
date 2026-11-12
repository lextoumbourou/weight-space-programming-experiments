## Step 2: recalibrate the greenness cue

**What step 1 showed.** Greenness pointing to "dog" is a real signal, since accuracy reached 54.5%. The decision threshold was badly placed, though: 89% of all images were predicted cat. So the typical pooled greenness is well below the 0.05 I assumed.

**What I change.**
- I double the greenness weight.
- I lower the threshold to a pooled greenness of about 0.02, so the predictions should split roughly evenly between the two classes.

This gives a calibrated baseline for the single cue. Next I will test other channels against it one at a time.

```python
import numpy as np

def build_weights():
    W = {}
    # ---------------- conv1: 16 hand-designed detectors on 5x5 RGB patches ----------------
    c1 = np.zeros((16, 3, 5, 5), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    avg = 1.0 / 25.0

    # 0: brightness
    c1[0, :, :, :] = avg / 3.0
    # 1: greenness = G - (R+B)/2
    c1[1, 1] = avg; c1[1, 0] = -avg / 2; c1[1, 2] = -avg / 2
    # 2: red minus blue
    c1[2, 0] = avg; c1[2, 2] = -avg
    # 3: blueness
    c1[3, 2] = avg; c1[3, 0] = -avg / 2; c1[3, 1] = -avg / 2

    e = 0.1
    horiz = np.zeros((5, 5)); horiz[0:2, :] = e; horiz[3:5, :] = -e
    vert = horiz.T.copy()
    diag = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            if c - r > 0: diag[r, c] = e
            elif c - r < 0: diag[r, c] = -e
    anti = diag[:, ::-1].copy()
    kernels = [horiz, vert, diag, anti]
    # 4-7 positive edges, 8-11 negative edges
    for k, ker in enumerate(kernels):
        for ch in range(3):
            c1[4 + k, ch] = ker / 3.0
            c1[8 + k, ch] = -ker / 3.0

    # 12: darkness
    c1[12, :, :, :] = -avg / 3.0
    b1[12] = 1.0
    # 13/14: Laplacian texture, both polarities
    lap = np.zeros((5, 5))
    lap[1:4, 1:4] = -1.0 / 8.0
    lap[2, 2] = 1.0
    lap *= 0.5
    for ch in range(3):
        c1[13, ch] = lap / 3.0
        c1[14, ch] = -lap / 3.0
    # 15: whiteness above 0.7
    c1[15, :, :, :] = avg / 3.0
    b1[15] = -0.7

    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ---------------- conv2: identity (0-15) and 5x5 blur (16-31) ----------------
    c2 = np.zeros((32, 16, 5, 5), dtype=np.float32)
    for c in range(16):
        c2[c, c, 2, 2] = 1.0
        c2[16 + c, c, :, :] = 1.0 / 25.0
    W['conv2.weight'] = c2
    W['conv2.bias'] = np.zeros(32, dtype=np.float32)

    # ---------------- conv3: identity ----------------
    c3 = np.zeros((32, 32, 3, 3), dtype=np.float32)
    for c in range(32):
        c3[c, c, 1, 1] = 1.0
    W['conv3.weight'] = c3
    W['conv3.bias'] = np.zeros(32, dtype=np.float32)

    # ---------------- fc: greenness -> dog, recalibrated ----------------
    fw = np.zeros((2, 32, 5, 5), dtype=np.float32)
    g = 0.2
    fw[1, 1, :, :] = g
    fw[0, 1, :, :] = -g
    W['fc.weight'] = fw.reshape(2, 800)
    # logit diff = 10 * mean_pooled_green - 0.2  -> threshold at 0.02
    W['fc.bias'] = np.array([0.1, -0.1], dtype=np.float32)

    for k in W:
        W[k] = W[k].astype(np.float32)
    return W
```
