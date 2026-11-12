## Step 12: back to step 9's weights, probe whiteness as cat evidence

**What step 11 showed.** Doubling blueness made the loss worse (0.6574 against 0.6486 at step 9). Accuracy changed little, so the stronger weight mostly made confident predictions wrong more often. I revert to the step 9 weights, which are the best so far.

**New probe: whiteness votes cat.** This is conv1 channel 15, which fires on regions brighter than 0.7. It follows from the pattern seen so far: colourful or textured images lean dog, so neutral images may lean cat. White or pale-grey fur, white walls, bedding and window light should all show up in this channel.

**Calibration.** I use a modest weight of 0.05 per pooled cell. I expect the typical pooled whiteness to be about 0.1. That would push the logit difference about 0.25 towards cat on average, so I move the bias 0.25 towards dog to compensate. The cat-minus-dog bias difference becomes 1.55.

```python
import numpy as np

def build_weights():
    W = {}
    # ---------------- conv1: 16 hand-designed detectors ----------------
    c1 = np.zeros((16, 3, 5, 5), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    avg = 1.0 / 25.0

    c1[0, :, :, :] = avg / 3.0                                       # 0 brightness
    c1[1, 1] = avg; c1[1, 0] = -avg / 2; c1[1, 2] = -avg / 2         # 1 greenness
    c1[2, 0] = avg; c1[2, 2] = -avg                                  # 2 red - blue (warm)
    c1[3, 2] = avg; c1[3, 0] = -avg / 2; c1[3, 1] = -avg / 2         # 3 blueness

    e = 0.1
    horiz = np.zeros((5, 5)); horiz[0:2, :] = e; horiz[3:5, :] = -e
    vert = horiz.T.copy()
    diag = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            if c - r > 0: diag[r, c] = e
            elif c - r < 0: diag[r, c] = -e
    anti = diag[:, ::-1].copy()
    for k, ker in enumerate([horiz, vert, diag, anti]):              # 4-7 / 8-11 edges
        for ch in range(3):
            c1[4 + k, ch] = ker / 3.0
            c1[8 + k, ch] = -ker / 3.0

    c1[12, :, :, :] = -avg / 3.0; b1[12] = 1.0                       # 12 darkness
    lap = np.zeros((5, 5)); lap[1:4, 1:4] = -1.0 / 8.0; lap[2, 2] = 1.0; lap *= 0.5
    for ch in range(3):                                              # 13/14 Laplacian texture
        c1[13, ch] = lap / 3.0
        c1[14, ch] = -lap / 3.0
    c1[15, :, :, :] = avg / 3.0; b1[15] = -0.7                       # 15 whiteness

    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ---------------- conv2: identity (0-15) + blur (16-31) ----------------
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

    # ---------------- fc ----------------
    fw = np.zeros((2, 32, 5, 5), dtype=np.float32)
    # greenness -> dog
    fw[1, 1, :, :] = 0.2
    fw[0, 1, :, :] = -0.2
    # blueness -> dog
    fw[1, 3, :, :] = 0.2
    fw[0, 3, :, :] = -0.2
    # warm (R-B) -> dog
    fw[1, 2, :, :] = 0.05
    fw[0, 2, :, :] = -0.05
    # fine texture -> dog
    for ch in (13, 14):
        fw[1, ch, :, :] = 0.1
        fw[0, ch, :, :] = -0.1
    # oriented edges -> dog
    for ch in range(4, 12):
        fw[1, ch, :, :] = 0.01
        fw[0, ch, :, :] = -0.01
    # PROBE: whiteness -> cat
    fw[0, 15, :, :] = 0.05
    fw[1, 15, :, :] = -0.05
    W['fc.weight'] = fw.reshape(2, 800)
    # step 9 bias 1.8 - 0.25 (whiteness shift toward cat)
    W['fc.bias'] = np.array([0.775, -0.775], dtype=np.float32)

    for k in W:
        W[k] = W[k].astype(np.float32)
    return W
```
