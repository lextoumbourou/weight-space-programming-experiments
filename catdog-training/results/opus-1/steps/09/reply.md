## Step 9: reverse the warm-colour cue

**What step 8 showed.** Making warm colour (R − B) a cat cue badly hurt the model: accuracy fell to 55.8% and the loss rose to 0.689. Miscalibration explains only part of this. The model predicted dog for 62% of images, yet in step 6 an even worse skew (74% dog) still gave 57%. So warm colour most likely points the other way. Brown, golden and tan fur is very common in dogs, while cats are more often grey, black or white.

The 62% dog skew also shows the warm term's average push towards cat was smaller than the 0.5 I assumed, more like 0.35.

**What I change.**
- Warm colour now votes dog, with the same weight of 0.05 per pooled cell.
- I start from the step 7 bias, which was the best calibrated so far.
- I nudge it 0.1 towards dog for the remaining cat lean.
- I move it about 0.35 towards cat to absorb the warm term's average push towards dog.
- The result is a cat-minus-dog bias difference of 1.8.

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
    # warm (R-B) -> DOG (flipped after step 8)
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
    W['fc.weight'] = fw.reshape(2, 800)
    # 1.55 - 0.1 + 0.35 = 1.8
    W['fc.bias'] = np.array([0.9, -0.9], dtype=np.float32)

    for k in W:
        W[k] = W[k].astype(np.float32)
    return W
```
