**Step 13 plan: first classifier built on measured frequencies.** Step 12 decoded cleanly. Presence of a vertical stroke in cell column 3 (around x ≈ 19.5), by row 0–3:

| Digit | Row 0 | Row 1 | Row 2 | Row 3 |
|---|---|---|---|---|
| 0 | 71% | 97% | 94% | 44% |
| 1 | 57% | 20% | 3% | 2% |
| 2 | 83% | 86% | 55% | 17% |
| 3 | 64% | 73% | 93% | 82% |
| 4 | 89% | 92% | 70% | 46% |
| 5 | 1% | 13% | 72% | 61% |
| 6 | 3% | 29% | 80% | 36% |
| 7 | 59% | 91% | 73% | 28% |
| 8 | 59% | 53% | 55% | 50% |
| 9 | 56% | 93% | 80% | 51% |

I now have measured presence frequencies for 31 features: 15 horizontal (the top-right cell is still unmeasured) and all 16 vertical. Before spending more steps on the two diagonal orientations, I want to check that the approach pays off.

This step is a pure presence/absence vote using only those 31 measured features, with the frequencies typed in as a table:

- weight on "stroke missing" = log((1−q)/q), where q is the measured frequency for that digit;
- bias = Σ log q plus the log of the class frequency;
- everything scaled by 0.3, because neighbouring cells are correlated and the raw vote would be overconfident.

The hand-drawn templates are switched off for this step so the result is a clean read on the measured table alone.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 4 oriented line detectors x 2 thresholds  (unchanged)
    #   channel k   (k=0..3): orientation k, bias -t0
    #   channel k+4         : same filter,  bias -t1
    #   orientation 0: horizontal stroke, 1: "/" , 2: vertical, 3: "\"
    #   pooled(k) - pooled(k+4) = clip(resp - t0, 0, t1 - t0)  -> saturated map M_k
    # ------------------------------------------------------------------
    prof = np.array([-0.75, 0.25, 1.0, 0.25, -0.75])   # across-stroke profile (zero sum)
    Hf = np.tile(prof[:, None], (1, 5))                # horizontal stroke detector
    Vf = Hf.T.copy()                                   # vertical stroke detector
    dv = [1.0, 0.4, -0.45, -0.9, -0.95]                # diagonal profile by |offset| (zero sum)
    D1 = np.zeros((5, 5))
    D2 = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            D1[r, c] = dv[abs((r - 2) + (c - 2))]      # "/" : ridge on r + c = 4
            D2[r, c] = dv[abs((r - 2) - (c - 2))]      # "\" : ridge on r = c
    filts = [Hf, D1, Vf, D2]
    t0, t1 = 0.45, 0.75
    w1 = np.zeros((8, 1, 5, 5))
    b1 = np.zeros(8)
    for k in range(4):
        w1[k, 0] = filts[k] / 5.0
        b1[k] = -t0
        w1[k + 4, 0] = filts[k] / 5.0
        b1[k + 4] = -t1

    # ------------------------------------------------------------------
    # conv2 (unchanged):
    #   channels 0..3  : C_k  = stroke amount of orientation k in a tapered 5x5 window
    #   channels 4..7  : E_k  = ReLU(1 - amount/tau)   ("stroke k missing here"; 0 = present)
    #   channels 8..11 : C'_k = ReLU(amount - tau_l)
    #   channels 12..15: unused
    # ------------------------------------------------------------------
    k1 = np.array([0.5, 1.0, 1.0, 1.0, 0.5])
    K2 = np.outer(k1, k1)
    tau = 1.6
    tau_l = 1.5
    w2 = np.zeros((16, 8, 5, 5))
    b2 = np.zeros(16)
    for k in range(4):
        w2[k, k] = K2 / (t1 - t0)
        w2[k, k + 4] = -K2 / (t1 - t0)
        w2[4 + k, k] = -K2 / ((t1 - t0) * tau)
        w2[4 + k, k + 4] = K2 / ((t1 - t0) * tau)
        b2[4 + k] = 1.0
        w2[8 + k, k] = K2 / (t1 - t0)
        w2[8 + k, k + 4] = -K2 / (t1 - t0)
        b2[8 + k] = -tau_l

    # ------------------------------------------------------------------
    # Measured presence frequencies (percent) of the E-channel features,
    # read off the probe steps 5-12.  Layout: [digit][cell row][cell column].
    # None = not measured yet (gets weight 0).
    # ------------------------------------------------------------------
    N = None
    H_tab = [   # horizontal stroke present
        [[7.6, 55, 86, N], [3.7, 17, 20.8, 11.5], [3.8, 9.4, 14.7, 8.7], [53.5, 96.9, 88.9, 37.2]],   # 0
        [[0.5, 2, 1.7, N], [0.6, 1, 0.7, 0.2], [0.5, 0.7, 0.5, 0.5], [1.8, 3.9, 3.6, 1.1]],           # 1
        [[41, 83, 81, N], [21.9, 46, 31.8, 7.2], [47.8, 70.2, 67, 45.6], [74, 94, 89.4, 73.1]],       # 2
        [[61, 97, 94, N], [44, 91, 90, 23.8], [34.2, 85.2, 81.6, 22.6], [68.8, 96.7, 87, 28.3]],      # 3
        [[1.5, 5, 4.2, N], [22, 55, 45.5, 18], [73.9, 96, 93, 39], [26.4, 59, 41.6, 14.6]],           # 4
        [[16, 73, 98, N], [35.7, 89, 93, 55.8], [41.2, 86, 75.6, 22.5], [68.3, 95, 78.5, 21]],        # 5
        [[0.4, 4.4, 20.6, N], [0.0, 14, 66, 59], [3.1, 45.2, 88.1, 72.5], [23.7, 93.5, 95.6, 53.4]],  # 6
        [[70, 98, 98.6, N], [63, 92, 89, 41], [8.3, 13.9, 12.6, 8.8], [3.5, 9.1, 7.6, 5]],            # 7
        [[14.6, 73, 93.7, N], [9.5, 38.8, 54.4, 31.4], [7.1, 33.2, 38.8, 13.9], [18.9, 73.8, 55, 8.8]],  # 8
        [[15.7, 87, 96, N], [32.8, 88.8, 84.4, 18.3], [51.3, 94, 79, 3.6], [14.8, 42.6, 16, 0.5]],    # 9
    ]
    V_tab = [   # vertical stroke present
        [[24.9, 35.8, 32.7, 70.9], [78.5, 59.6, 42.7, 97], [98.2, 53.3, 33.6, 94.2], [92.7, 39.9, 16.5, 44.4]],  # 0
        [[0.6, 52.9, 94.9, 56.8], [0.3, 86.7, 97.6, 19.8], [8.7, 95.8, 95.7, 2.8], [8.6, 94.6, 78.9, 1.8]],      # 1
        [[11.5, 19.8, 72.1, 82.9], [9.4, 26.5, 82.1, 86], [39, 28.4, 60.8, 55.1], [37.3, 27.4, 17.4, 16.6]],     # 2
        [[6.8, 16.4, 69.4, 63.8], [5.3, 20.5, 79.5, 72.5], [14.4, 10.9, 74.5, 93.3], [13.6, 15.2, 60.9, 82.2]],  # 3
        [[50.3, 70.6, 79.3, 89], [76.6, 82.2, 92.1, 92.4], [63.3, 75.1, 92.6, 70.2], [10, 64, 89.4, 45.9]],      # 4
        [[29, 43.1, 12.9, 1.4], [52.7, 67.7, 32.1, 12.9], [43.7, 47.3, 70.7, 71.6], [23, 24.2, 64.9, 60.9]],     # 5
        [[27.3, 72.8, 48.3, 3.3], [70.8, 87.4, 59.5, 28.7], [95, 91.5, 64.9, 80.1], [58.5, 66.6, 40.4, 35.9]],   # 6
        [[11.5, 11.7, 40.3, 59.2], [23.6, 25, 81.7, 90.7], [13.5, 42.7, 90.1, 72.8], [2.2, 70.5, 85.2, 27.9]],   # 7
        [[30.4, 66.8, 56.5, 58.7], [55.5, 87.3, 74, 53.1], [69.6, 90.8, 87.9, 55.4], [65.2, 91.8, 89.7, 50.2]],  # 8
        [[18.1, 23.8, 49.9, 56.4], [88.1, 78.8, 87.5, 92.5], [62, 77.4, 92.3, 80.4], [2.6, 58.9, 89.8, 51.1]],   # 9
    ]
    tables = {0: H_tab, 2: V_tab}          # orientation index -> table

    class_counts = np.array([991, 1064, 990, 1030, 983, 915, 967, 1090, 1009, 961], dtype=float)

    # ------------------------------------------------------------------
    # fc: presence/absence vote from the measured frequencies
    #   logit_d = s * sum_f [ log q_df + E_f * log((1-q_df)/q_df) ] + log prior_d
    # ------------------------------------------------------------------
    s = 0.3                                 # temperature (features are correlated)
    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for d in range(10):
        fcb[d] = math.log(class_counts[d] / class_counts.sum())
        for k, tab in tables.items():
            for i in range(4):
                for j in range(4):
                    v = tab[d][i][j]
                    if v is None:
                        continue
                    q = min(max(v / 100.0, 0.03), 0.97)
                    idx = (4 + k) * 16 + i * 4 + j          # emptiness channel 4+k, cell (i, j)
                    fcw[d, idx] = s * math.log((1.0 - q) / q)
                    fcb[d] += s * math.log(q)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
