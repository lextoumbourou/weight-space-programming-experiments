**Step 8: replace the hand-tuned biases with an analytic mean-image calibration.**

Step 7 showed that the hand-tuned offsets are too sensitive. Moving class 9's offset from +0.8 to −0.5 removed nearly all 9 predictions, and moving class 3's from −0.8 to 0 made it absorb about 3,900 images. Small per-class offsets can't be tuned reliably by trial and error.

The fix is to set the biases from a principle rather than by feedback. The average of the ten templates, T̄, is the typical digit. I set each class's bias so that the typical digit produces equal logits for all ten classes. This gives:

- logit_d(f) = s·g·Σ_k α_k·T_dk·(f_k − g·T̄_k)
- Biases are b_d = −s·g²·Σ_k α_k·T_dk·T̄_k.

So each class is scored on how its template differs from the average digit, rather than on its raw overlap with the image. This removes the systematic advantage that large-ink templates (like 2 or 8) get on heavy images, without needing per-class offsets. The templates and per-channel scales are the same as in step 5, so only the calibration changes.

```python
import numpy as np


def build_weights():
    # ---------- conv1: 8 filters, 1x5x5 ----------
    c1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing="ij")

    # f0: vertical stroke detector
    k = np.zeros((5, 5))
    k[c == 2] = 1.0
    k[(c == 0) | (c == 4)] = -0.5
    c1[0, 0] = k

    # f1: horizontal stroke detector
    k = np.zeros((5, 5))
    k[r == 2] = 1.0
    k[(r == 0) | (r == 4)] = -0.5
    c1[1, 0] = k

    # f2: '/' diagonal stroke detector
    k = np.zeros((5, 5))
    k[r + c == 4] = 1.0
    k[np.abs(r + c - 4) == 1] = -0.5
    c1[2, 0] = k

    # f3: '\' diagonal stroke detector
    k = np.zeros((5, 5))
    k[r == c] = 1.0
    k[np.abs(r - c) == 1] = -0.5
    c1[3, 0] = k

    # f4: centre blob detector
    k = np.full((5, 5), -0.5)
    k[1:4, 1:4] = 1.0
    c1[4, 0] = k

    # f5: left-edge detector
    k = np.zeros((5, 5))
    k[c <= 1] = 1.0
    k[c >= 3] = -1.0
    c1[5, 0] = k

    # f6: top-edge detector
    k = np.zeros((5, 5))
    k[r <= 1] = 1.0
    k[r >= 3] = -1.0
    c1[6, 0] = k

    # f7: ink density detector
    c1[7, 0] = np.full((5, 5), 0.2)
    b1[7] = -0.5

    # ---------- conv2: 16 filters, 8x5x5 ----------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros(16, dtype=np.float32)

    # channels 0-7: box average of the matching conv1 channel.
    # channels 0-3 = orientation presence (V, H, /, \), channel 7 = ink density.
    for j in range(8):
        c2[j, j] = 0.05

    # channels 8-15: cross-shaped detectors (not used by the readout)
    for j in range(8, 16):
        k_in = j - 8
        c2[j, k_in] = np.where((r == 2) | (c == 2), 0.1, -0.05)

    # ---------- fc: 256 -> 10 ----------
    # Flatten order is (channel, row, col): index = ch*16 + i*4 + j.

    # Ink-density templates (rows top to bottom, columns left to right).
    D = np.zeros((10, 4, 4))
    D[0] = [[0.0, 0.6, 0.6, 0.0], [0.7, 0.0, 0.0, 0.7], [0.7, 0.0, 0.0, 0.7], [0.0, 0.6, 0.6, 0.0]]
    D[1] = [[0.0, 0.4, 0.6, 0.0], [0.0, 0.3, 0.8, 0.0], [0.0, 0.2, 0.8, 0.0], [0.0, 0.2, 0.8, 0.0]]
    D[2] = [[0.2, 0.6, 0.7, 0.4], [0.0, 0.0, 0.3, 0.8], [0.0, 0.5, 0.6, 0.2], [0.6, 0.9, 0.9, 0.6]]
    D[3] = [[0.3, 0.7, 0.6, 0.3], [0.0, 0.1, 0.5, 0.7], [0.1, 0.4, 0.6, 0.6], [0.2, 0.6, 0.7, 0.4]]
    D[4] = [[0.1, 0.1, 0.4, 0.5], [0.4, 0.1, 0.5, 0.5], [0.7, 0.7, 0.8, 0.6], [0.1, 0.1, 0.7, 0.6]]
    D[5] = [[0.6, 0.7, 0.7, 0.4], [0.6, 0.2, 0.0, 0.0], [0.3, 0.6, 0.6, 0.3], [0.1, 0.5, 0.7, 0.5]]
    D[6] = [[0.1, 0.5, 0.6, 0.2], [0.6, 0.2, 0.0, 0.0], [0.7, 0.4, 0.3, 0.5], [0.3, 0.6, 0.7, 0.4]]
    D[7] = [[0.7, 0.8, 0.8, 0.6], [0.0, 0.0, 0.5, 0.6], [0.0, 0.3, 0.5, 0.1], [0.0, 0.3, 0.5, 0.0]]
    D[8] = [[0.2, 0.6, 0.6, 0.2], [0.6, 0.1, 0.1, 0.6], [0.3, 0.6, 0.6, 0.3], [0.6, 0.2, 0.2, 0.6]]
    D[9] = [[0.2, 0.6, 0.6, 0.3], [0.6, 0.1, 0.1, 0.6], [0.1, 0.2, 0.5, 0.7], [0.1, 0.5, 0.7, 0.4]]

    # Vertical-stroke presence templates (conv2 channel 0).
    V = np.zeros((10, 4, 4))
    V[0] = [[0, .3, .3, 0], [.8, 0, 0, .8], [.8, 0, 0, .8], [0, .3, .3, 0]]
    V[1] = [[0, .3, .7, 0], [0, .3, .8, 0], [0, .2, .8, 0], [0, .2, .8, 0]]
    V[2] = [[0, 0, .4, .4], [0, 0, .4, .5], [0, 0, .2, .1], [0, .1, .1, 0]]
    V[3] = [[0, 0, .4, .3], [0, 0, .5, .6], [0, 0, .5, .6], [0, 0, .3, .3]]
    V[4] = [[0, 0, .5, .1], [0, 0, .7, .1], [0, 0, .7, .2], [0, 0, .7, .2]]
    V[5] = [[.6, 0, 0, .1], [.6, 0, 0, 0], [0, .2, .3, .1], [0, .1, .4, .2]]
    V[6] = [[0, .3, .1, 0], [.7, .1, 0, 0], [.8, .2, .2, .2], [.4, .5, .6, .4]]
    V[7] = [[0, 0, 0, .1], [0, 0, .3, .2], [0, .1, .3, 0], [0, .1, .2, 0]]
    V[8] = [[0, .2, .2, 0], [.6, 0, 0, .6], [.6, 0, 0, .6], [0, .3, .3, 0]]
    V[9] = [[0, .1, .3, .2], [.5, 0, .1, .6], [0, 0, .5, .6], [0, .1, .6, .3]]

    # Horizontal-stroke presence templates (conv2 channel 1).
    H = np.zeros((10, 4, 4))
    H[0] = [[0, .6, .6, 0], [.1, 0, 0, .1], [.1, 0, 0, .1], [0, .6, .6, 0]]
    H[1] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, .2, .2, 0]]
    H[2] = [[.2, .6, .6, .3], [0, 0, 0, 0], [0, .1, .2, 0], [.6, .9, .9, .6]]
    H[3] = [[.3, .7, .6, .3], [0, 0, .2, 0], [0, .3, .4, .1], [.2, .6, .7, .4]]
    H[4] = [[0, 0, 0, 0], [0, 0, 0, 0], [.6, .8, .7, .5], [0, 0, 0, 0]]
    H[5] = [[.7, .8, .7, .3], [0, 0, 0, 0], [.2, .4, .4, .2], [.2, .5, .6, .3]]
    H[6] = [[.1, .5, .5, .2], [0, 0, 0, 0], [.2, .3, .3, .1], [.2, .6, .6, .2]]
    H[7] = [[.8, .8, .8, .6], [0, 0, 0, .1], [0, 0, .1, 0], [0, 0, 0, 0]]
    H[8] = [[.1, .6, .6, .1], [0, .2, .2, 0], [.1, .6, .6, .1], [0, .5, .5, 0]]
    H[9] = [[.2, .6, .6, .2], [0, 0, .1, .1], [0, .2, .3, .1], [.1, .4, .5, .1]]

    # '/' diagonal presence templates (conv2 channel 2).
    S = np.zeros((10, 4, 4))
    S[0] = [[0, .1, .4, .2], [.1, .2, .1, .5], [.5, .1, .2, .1], [.2, .4, .1, 0]]
    S[2] = [[0, 0, 0, .2], [0, 0, .4, .4], [0, .5, .4, 0], [.3, .2, 0, 0]]
    S[3] = [[0, 0, 0, .1], [0, 0, .2, 0], [0, 0, .2, 0], [0, 0, 0, 0]]
    S[4] = [[0, 0, .4, .3], [.3, .5, .1, 0], [.6, .1, 0, 0], [0, 0, 0, 0]]
    S[5] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, .1, 0]]
    S[6] = [[0, 0, .1, 0], [.1, .2, .1, 0], [.3, .2, 0, 0], [.1, .1, 0, 0]]
    S[7] = [[0, 0, 0, .2], [0, 0, .5, .3], [0, .3, .5, 0], [0, .4, .3, 0]]
    S[8] = [[0, 0, .2, 0], [0, .2, 0, .2], [.2, 0, .2, 0], [0, .2, 0, 0]]
    S[9] = [[0, 0, 0, 0], [0, 0, .2, 0], [0, .1, .2, 0], [0, .2, .1, 0]]

    # '\' diagonal presence templates (conv2 channel 3).
    B = np.zeros((10, 4, 4))
    B[0] = [[.2, .4, .1, 0], [.5, .1, .2, .1], [.1, .2, .1, .5], [0, .1, .4, .2]]
    B[3] = [[0, 0, 0, 0], [0, 0, .1, 0], [0, .1, 0, 0], [0, 0, 0, 0]]
    B[5] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, .2, .2, 0], [.2, .4, .4, .1]]
    B[6] = [[0, 0, 0, 0], [0, 0, 0, .1], [0, 0, .2, .3], [0, .2, .3, .2]]
    B[8] = [[0, .2, 0, 0], [.2, 0, .2, 0], [0, .2, 0, .2], [0, 0, .2, 0]]
    B[9] = [[0, 0, 0, 0], [0, 0, .1, 0], [0, .2, 0, 0], [0, .2, 0, 0]]

    # ---- Readout: mean-image calibrated linear classifier ----
    # logit_d(f) = s*g * sum_k alpha_k <T_dk, f_k - g*Tbar_k> (no per-class offsets)
    s = 0.5          # overall logit scale
    g = 1.5          # typical feature value at a fully matched cell
    alpha = {"V": 0.6, "H": 0.6, "S": 1.2, "B": 1.2, "D": 1.0}

    channels = [("V", V, 0), ("H", H, 1), ("S", S, 2), ("B", B, 3), ("D", D, 7)]

    fc_w = np.zeros((10, 16, 4, 4), dtype=np.float64)
    fc_b = np.zeros(10, dtype=np.float64)

    for name, Tk, ch in channels:
        a = alpha[name]
        Tbar_k = Tk.mean(axis=0)                          # typical digit for this channel
        fc_w[:, ch] = s * g * a * Tk                      # matched-filter weights
        # Bias so the typical digit gives equal logits for all classes:
        # b_d = -s * g^2 * sum_cells(alpha * T_dk * Tbar_k)
        fc_b += -s * g * g * a * np.sum(Tk * Tbar_k, axis=(1, 2))

    fc_w = fc_w.reshape(10, 256).astype(np.float32)
    fc_b = fc_b.astype(np.float32)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
