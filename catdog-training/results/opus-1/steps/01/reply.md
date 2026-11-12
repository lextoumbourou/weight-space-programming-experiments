## Step 1: build a clean feature pipeline and test one simple cue

**The pipeline.** The idea is to make every stage easy to read, so later steps can change one thing at a time.

- **conv1 (hand-designed detectors):**
  - colour-opponent channels: greenness, red−blue (orange/brown fur), blueness
  - brightness, darkness and whiteness
  - oriented luminance edges in both polarities: horizontal, vertical and the two diagonals
  - a Laplacian "texture" detector in both polarities
- **conv2:** channels 0–15 copy the conv1 maps through a centre tap (identity). Channels 16–31 are 5×5 box-blurred copies of the same maps.
- **conv3:** a pure identity pass-through using centre taps.
- **The final 32×5×5 grid:** each value is roughly the maximum of a feature over a large patch of the image.

**The cue being tested.** Only one cue goes into the classifier: "lots of green, so probably outdoors on grass, so dog." All other fc weights are zero.

- The logits are kept small, so the loss should stay near ln 2 ≈ 0.693.
- If accuracy goes above 50%, the cue points the right way. If it goes below, I will flip it.
- Later steps will test the other channels (edges and texture for fur stripes, orange colour, and so on) in the same way.

```python
import numpy as np

def build_weights():
    W = {}
    # ---------------- conv1: 16 hand-designed detectors on 5x5 RGB patches ----------------
    c1 = np.zeros((16, 3, 5, 5), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    avg = 1.0 / 25.0                      # spatial average weight

    # 0: brightness = mean luminance over patch
    c1[0, :, :, :] = avg / 3.0
    # 1: greenness = G - (R+B)/2
    c1[1, 1] = avg; c1[1, 0] = -avg / 2; c1[1, 2] = -avg / 2
    # 2: red minus blue (orange / brown tones)
    c1[2, 0] = avg; c1[2, 2] = -avg
    # 3: blueness = B - (R+G)/2
    c1[3, 2] = avg; c1[3, 0] = -avg / 2; c1[3, 1] = -avg / 2

    # luminance edge kernels (5x5)
    e = 0.1
    horiz = np.zeros((5, 5)); horiz[0:2, :] = e; horiz[3:5, :] = -e      # top bright vs bottom bright
    vert = horiz.T.copy()
    diag = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            if c - r > 0: diag[r, c] = e
            elif c - r < 0: diag[r, c] = -e
    anti = diag[:, ::-1].copy()
    kernels = [horiz, vert, diag, anti]
    # 4-7: positive polarity edges ; 8-11: negative polarity edges
    for k, ker in enumerate(kernels):
        for ch in range(3):
            c1[4 + k, ch] = ker / 3.0
            c1[8 + k, ch] = -ker / 3.0

    # 12: darkness = 1 - brightness
    c1[12, :, :, :] = -avg / 3.0
    b1[12] = 1.0
    # 13/14: Laplacian (centre vs ring of 3x3) -> fine texture, both polarities
    lap = np.zeros((5, 5))
    lap[1:4, 1:4] = -1.0 / 8.0
    lap[2, 2] = 1.0
    lap *= 0.5
    for ch in range(3):
        c1[13, ch] = lap / 3.0
        c1[14, ch] = -lap / 3.0
    # 15: whiteness: brightness above 0.7
    c1[15, :, :, :] = avg / 3.0
    b1[15] = -0.7

    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ---------------- conv2: identity (0-15) and 5x5 box blur (16-31) ----------------
    c2 = np.zeros((32, 16, 5, 5), dtype=np.float32)
    for c in range(16):
        c2[c, c, 2, 2] = 1.0                  # pass-through
        c2[16 + c, c, :, :] = 1.0 / 25.0      # local average
    W['conv2.weight'] = c2
    W['conv2.bias'] = np.zeros(32, dtype=np.float32)

    # ---------------- conv3: identity pass-through ----------------
    c3 = np.zeros((32, 32, 3, 3), dtype=np.float32)
    for c in range(32):
        c3[c, c, 1, 1] = 1.0
    W['conv3.weight'] = c3
    W['conv3.bias'] = np.zeros(32, dtype=np.float32)

    # ---------------- fc: probe one cue -> greenness (channel 1) votes dog ----------------
    fw = np.zeros((2, 32, 5, 5), dtype=np.float32)
    g = 0.1
    fw[1, 1, :, :] = g      # dog logit up with green
    fw[0, 1, :, :] = -g     # cat logit down with green
    W['fc.weight'] = fw.reshape(2, 800)
    # centre the decision (expected pooled greenness ~0.05)
    W['fc.bias'] = np.array([0.125, -0.125], dtype=np.float32)

    for k in W:
        W[k] = W[k].astype(np.float32)
    return W
```
