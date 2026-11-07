**Step 1: baseline from hand-drawn filters.**

- **Conv1 (8 filters):** Oriented stroke detectors (vertical, horizontal, two diagonals), a centre-blob detector, left-edge and top-edge detectors, and an ink-density detector. Each is zero-sum or near zero-sum, so a blank background gives no response. The density detector has a negative bias so it stays silent on empty pixels.
- **Conv2 (16 filters):** Channels 0-7 are box averages of the matching conv1 map, which measure how much of each stroke type is present in a region. Channels 8-15 are cross-shaped detectors on the same maps, which add some spatial structure.
- **FC readout:** Each digit gets a hand-written prototype. It rewards the stroke types and regions where that digit usually has ink, and penalises stroke types where it usually doesn't. The spatial masks are coarse 4x4 region templates.

I expect this to be a rough baseline. The confusion matrix should show which digits are being mixed up, and I'll adjust the prototypes from there.

```python
import numpy as np


def build_weights():
    # ---------- conv1: 8 filters, 1x5x5 ----------
    c1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)
    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing="ij")

    # f0: vertical stroke detector (centre column positive, sides negative)
    k = np.zeros((5, 5))
    k[c == 2] = 1.0
    k[(c == 0) | (c == 4)] = -0.5
    c1[0, 0] = k

    # f1: horizontal stroke detector (centre row positive, top/bottom negative)
    k = np.zeros((5, 5))
    k[r == 2] = 1.0
    k[(r == 0) | (r == 4)] = -0.5
    c1[1, 0] = k

    # f2: '/' diagonal stroke detector (anti-diagonal r+c=4 positive)
    k = np.zeros((5, 5))
    k[r + c == 4] = 1.0
    k[np.abs(r + c - 4) == 1] = -0.5
    c1[2, 0] = k

    # f3: '\' diagonal stroke detector (main diagonal r=c positive)
    k = np.zeros((5, 5))
    k[r == c] = 1.0
    k[np.abs(r - c) == 1] = -0.5
    c1[3, 0] = k

    # f4: centre blob detector (inner 3x3 positive, outer ring negative)
    k = np.full((5, 5), -0.5)
    k[1:4, 1:4] = 1.0
    c1[4, 0] = k

    # f5: left-edge detector (ink on the left, background on the right)
    k = np.zeros((5, 5))
    k[c <= 1] = 1.0
    k[c >= 3] = -1.0
    c1[5, 0] = k

    # f6: top-edge detector (ink above, background below)
    k = np.zeros((5, 5))
    k[r <= 1] = 1.0
    k[r >= 3] = -1.0
    c1[6, 0] = k

    # f7: ink density detector (small positive weight everywhere, negative bias)
    c1[7, 0] = np.full((5, 5), 0.2)
    b1[7] = -0.5

    # ---------- conv2: 16 filters, 8x5x5 ----------
    c2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.zeros(16, dtype=np.float32)

    # channels 0-7: box average of the matching conv1 channel (stroke density in a region)
    for j in range(8):
        c2[j, j] = 0.05

    # channels 8-15: cross-shaped detector on conv1 channel (j-8)
    for j in range(8, 16):
        k_in = j - 8
        pattern = np.where((r == 2) | (c == 2), 0.1, -0.05)
        c2[j, k_in] = pattern

    # ---------- fc: 256 -> 10 ----------
    # Flatten order is (channel, row, col), so index = ch*16 + i*4 + j.
    # fc_w[d, ch, i, j] is the weight from feature (ch, i, j) to digit d.
    fi, fj = np.meshgrid(np.arange(4), np.arange(4), indexing="ij")

    def mask(name):
        # coarse 4x4 spatial templates; +1 where the digit usually has ink, negative elsewhere
        if name == "all":
            return np.ones((4, 4))
        if name == "ring":
            return np.where((fi == 0) | (fi == 3) | (fj == 0) | (fj == 3), 1.0, -1.0)
        if name == "center":
            return np.where((fj == 1) | (fj == 2), 1.0, -0.5)
        if name == "top":
            return np.where(fi <= 1, 1.0, -0.5)
        if name == "bottom":
            return np.where(fi >= 2, 1.0, -0.5)
        if name == "left":
            return np.where(fj <= 1, 1.0, -0.5)
        if name == "right":
            return np.where(fj >= 2, 1.0, -0.5)
        if name == "top_row":
            return np.where(fi == 0, 1.0, -0.3)
        if name == "bottom_row":
            return np.where(fi == 3, 1.0, -0.3)
        if name == "mid":
            return np.where((fi == 1) | (fi == 2), 1.0, -0.5)
        raise ValueError(name)

    # Each digit: list of (feature channel, spatial mask, weight)
    prototypes = {
        0: [(7, "ring", 1.0), (0, "center", -0.5)],
        1: [(0, "center", 1.0), (1, "all", -0.5), (7, "center", 0.3)],
        2: [(1, "top", 0.5), (1, "bottom_row", 1.0), (2, "all", 0.8), (0, "center", -0.5)],
        3: [(1, "top", 0.5), (1, "mid", 0.5), (1, "bottom_row", 0.5),
            (0, "right", 0.6), (0, "left", -0.8)],
        4: [(0, "right", 0.8), (1, "mid", 0.8), (0, "left", -0.8), (3, "left", 0.5)],
        5: [(1, "top_row", 1.0), (5, "left", 0.8), (0, "right", -0.5), (1, "bottom_row", -0.8)],
        6: [(5, "left", 0.8), (4, "bottom", 0.8), (0, "left", 0.5), (1, "top_row", -0.5)],
        7: [(1, "top_row", 1.0), (3, "right", 0.6), (0, "left", -0.5), (7, "bottom", -0.3)],
        8: [(4, "all", 0.8), (7, "ring", 0.6)],
        9: [(4, "top", 0.8), (0, "right", 0.8), (1, "top_row", 0.6),
            (0, "left", -0.5), (1, "bottom_row", -0.8)],
    }

    fc_w = np.zeros((10, 16, 4, 4), dtype=np.float32)
    for d, terms in prototypes.items():
        for ch, name, w in terms:
            fc_w[d, ch] += (w * mask(name)).astype(np.float32)

    fc_w = fc_w.reshape(10, 256) * 0.1  # scale logits to a moderate range
    fc_b = np.zeros(10, dtype=np.float32)

    return {
        "conv1.weight": c1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": c2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
