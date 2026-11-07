## Step 15: second probe, with a lowered loop threshold and the narrow-gap detector

**Probe results from step 14.**
- **LOOP never fired** in any digit, so its threshold was unreachable. By my estimate, a real hole gives about 0.8 from the background tap plus 4 × 0.6 × 0.5 from the ink taps, roughly 2.0. That is below the bias of 2.2.
- **HB2 (wide gap) works and is informative.** The counts below say where it fired most. Each row also contains ~280–1,060 images in the "nothing" column, not shown.

| Digit | Where HB2 fired (grid row: count) |
|---|---|
| 0 | spread over all rows (117 / 191 / 215 / 187) |
| 4 | row 1 (429) |
| 9 | row 1 (420) |
| 6 | rows 1–2 (168 / 216) |
| 7 | row 1 (261), unexpectedly |
| 8 | rows 1 and 3 |
| 2 | rows 0 and 3 |
| 3, 5 | rows 2–3 |
| 1 | never |

This tells me the real locations, which were off from my guessed tables.

**What this probe measures.** conv1 and the rest of conv2 are unchanged. The LOOP bias goes from −2.2 to −1.7.

| Output | Meaning |
|---|---|
| 0–3 | LOOP (ch9) at grid rows 0–3, central columns, measured relative to 0.1 |
| 4–7 | HB1 narrow gap (ch7) at rows 0–3, measured relative to 0.15 |
| 8 | "nothing" |

Afterwards I will rebuild the topology templates from the measured per-class distributions.

```python
import numpy as np
import math

def build_weights():
    # ==================================================================
    # DIAGNOSTIC PROBE 2: LOOP (threshold lowered) and HB1 locations.
    # ==================================================================
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    thetas = [0.0, 45.0, 90.0, 135.0]
    ys, xs = np.mgrid[-2:3, -2:3].astype(np.float64)
    s = 1.5
    for k, th in enumerate(thetas):
        t = math.radians(th)
        d = -math.sin(t) * xs + math.cos(t) * ys
        w = (1 - d**2 / s**2) * np.exp(-d**2 / (2 * s**2))
        w = w - w.mean()
        w = w / w[w > 0].sum()
        W1[k, 0] = w
        b1[k] = -0.15
    g = np.exp(-(xs**2 + ys**2) / 2.0); g /= g.sum()
    W1[4, 0] = g
    b1[4] = -0.1
    W1[5, 0] = -1.5 * g
    b1[5] = 1.0

    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    blur3 = np.array([[0.125, 0.25, 0.125],
                      [0.25,  0.5,  0.25],
                      [0.125, 0.25, 0.125]])
    for c in range(5):
        W2[c, c, 1:4, 1:4] = blur3

    def pair_detector(ch, taps):
        W2[ch, 5, 2, 2] = 1.0
        for (r, c) in taps:
            W2[ch, 4, r, c] = 1.0
        b2[ch] = -1.8

    pair_detector(5, [(2, 0), (2, 4)])   # HB2
    pair_detector(6, [(0, 2), (4, 2)])   # VB2
    pair_detector(7, [(2, 1), (2, 3)])   # HB1
    pair_detector(8, [(1, 2), (3, 2)])   # VB1
    W2[9, 5, 2, 2] = 1.0                 # LOOP, threshold lowered 2.2 -> 1.7
    for (r, c) in [(1, 2), (3, 2), (2, 1), (2, 3)]:
        W2[9, 4, r, c] = 0.6
    b2[9] = -1.7

    # fc probe
    beta = 10.0
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)
    idx = lambda c, i, j: c * 16 + i * 4 + j
    for r in range(4):
        for j in (1, 2):
            Wf[r, idx(9, r, j)] = beta * 0.5 / 0.1        # LOOP row r
            Wf[4 + r, idx(7, r, j)] = beta * 0.5 / 0.15   # HB1 row r
    bf[8] = beta * 1.0        # nothing over threshold
    bf[9] = -100.0

    return {
        "conv1.weight": W1, "conv1.bias": b1,
        "conv2.weight": W2, "conv2.bias": b2,
        "fc.weight": Wf, "fc.bias": bf,
    }
```
