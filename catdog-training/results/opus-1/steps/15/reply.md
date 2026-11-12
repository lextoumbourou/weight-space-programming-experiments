## Step 15: test whether warm colour matters more on the animal than on the background

**Where things stand.** Step 14's 1.3× scale-up was about neutral: loss 0.6454 against 0.6456, accuracy 63.4%. The logit scale is roughly right, so further gains must come from better features, not from rescaling.

**Using spatial position.** So far each cue is pooled over the whole 5×5 output grid. In most pet photos the animal sits near the centre, so the grid's centre 3×3 mostly shows the animal and the outer ring mostly shows the background. Warm colour (R − B) probably helps because of golden, brown or tan fur. If so, it should be much more informative in the centre than at the edges.

**This probe.**
- Move all the warm-colour weight onto the centre 3×3 cells.
- Multiply the per-cell weight by 25/9, so the total weight and the average push stay about the same. The bias is left unchanged.

Nothing else changes, so the result shows directly whether centre-only warm colour beats warm colour everywhere.

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

    # ---------------- fc: per-channel "dog evidence" weights ----------------
    S = 1.3
    fw = np.zeros((2, 32, 5, 5), dtype=np.float32)
    dogw = {1: 0.2,    # greenness
            3: 0.2,    # blueness
            13: 0.1, 14: 0.1,   # fine texture
            15: -0.05}          # whiteness (votes cat)
    for ch in range(4, 12):
        dogw[ch] = 0.01         # oriented edges
    for ch, w in dogw.items():
        fw[1, ch, :, :] = S * w
        fw[0, ch, :, :] = -S * w
    # warm (R-B): centre 3x3 only, same total weight
    wc = S * 0.05 * 25.0 / 9.0
    fw[1, 2, 1:4, 1:4] = wc
    fw[0, 2, 1:4, 1:4] = -wc
    W['fc.weight'] = fw.reshape(2, 800)
    W['fc.bias'] = np.array([1.105, -1.105], dtype=np.float32)

    for k in W:
        W[k] = W[k].astype(np.float32)
    return W
```
