**Step 20 plan: second classifier from measured frequencies.** Step 19 decoded cleanly. Presence of a "\" stroke at the last three cells:

| Digit | (row 2, col 3) | (row 3, col 3) | (row 0, col 0) |
|---|---|---|---|
| 0 | 11% | 0% | 1% |
| 1 | 0% | 2% | 1% |
| 2 | 39% | 60% | 2% |
| 3 | 82% | 23% | 7% |
| 4 | 16% | 14% | 7% |
| 5 | 61% | 17% | 7% |
| 6 | 60% | 7% | 1% |
| 7 | 5% | 2% | 23% |
| 8 | 36% | 25% | 12% |
| 9 | 9% | 8% | 1% |

The tables for horizontal, vertical and "\" strokes are now complete (48 features). For "/" I have two properly measured central cells plus five rough estimates taken from the conditional extras.

This step is the presence/absence vote again, now with all of that:

- **Fully measured features** (the 15 horizontal cells, vertical, "\", and the two central "/" cells) enter at full weight.
- **Rough "/" estimates** enter at half weight, and the rough top-right horizontal cell at 0.7, because they were measured only on sub-groups.
- **Scale** drops slightly from 0.30 to 0.25, since more correlated features are being summed.

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
    # read off the probe steps.  Layout: [digit][cell row][cell column].
    # None = not measured (weight 0).
    # ------------------------------------------------------------------
    N = None
    H_tab = [   # horizontal stroke present  (cell (0,3) is a rough estimate)
        [[7.6, 55, 86, 60], [3.7, 17, 20.8, 11.5], [3.8, 9.4, 14.7, 8.7], [53.5, 96.9, 88.9, 37.2]],   # 0
        [[0.5, 2, 1.7, 2], [0.6, 1, 0.7, 0.2], [0.5, 0.7, 0.5, 0.5], [1.8, 3.9, 3.6, 1.1]],            # 1
        [[41, 83, 81, 25], [21.9, 46, 31.8, 7.2], [47.8, 70.2, 67, 45.6], [74, 94, 89.4, 73.1]],       # 2
        [[61, 97, 94, 36], [44, 91, 90, 23.8], [34.2, 85.2, 81.6, 22.6], [68.8, 96.7, 87, 28.3]],      # 3
        [[1.5, 5, 4.2, 4], [22, 55, 45.5, 18], [73.9, 96, 93, 39], [26.4, 59, 41.6, 14.6]],            # 4
        [[16, 73, 98, 90], [35.7, 89, 93, 55.8], [41.2, 86, 75.6, 22.5], [68.3, 95, 78.5, 21]],        # 5
        [[0.4, 4.4, 20.6, 14], [0.0, 14, 66, 59], [3.1, 45.2, 88.1, 72.5], [23.7, 93.5, 95.6, 53.4]],  # 6
        [[70, 98, 98.6, 70], [63, 92, 89, 41], [8.3, 13.9, 12.6, 8.8], [3.5, 9.1, 7.6, 5]],            # 7
        [[14.6, 73, 93.7, 68], [9.5, 38.8, 54.4, 31.4], [7.1, 33.2, 38.8, 13.9], [18.9, 73.8, 55, 8.8]],  # 8
        [[15.7, 87, 96, 48], [32.8, 88.8, 84.4, 18.3], [51.3, 94, 79, 3.6], [14.8, 42.6, 16, 0.5]],    # 9
    ]
    H_rel = [[1, 1, 1, 0.7], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]

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
    V_rel = [[1, 1, 1, 1]] * 4

    B_tab = [   # "\" stroke present
        [[0.5, 7.3, 68.5, 94.3], [1.1, 4.4, 32.7, 77.5], [31, 15.4, 7.8, 11.4], [93.5, 68.5, 5.1, 0.3]],     # 0
        [[0.8, 14.2, 12.7, 0.2], [0.3, 7.3, 8.2, 0.1], [0.0, 4.9, 7.9, 0.4], [0.4, 7.5, 14.8, 1.9]],         # 1
        [[2.3, 28, 80.5, 71.6], [2.2, 16.6, 40, 27.3], [12.5, 31.6, 50.5, 38.9], [31.4, 39.9, 60, 60.2]],    # 2
        [[7.1, 39.9, 80.5, 48.2], [5.6, 38.1, 93.6, 71.4], [11.3, 36.5, 91.6, 81.7], [61.7, 52.1, 32.3, 22.8]],  # 3
        [[7.3, 5.6, 10, 4.8], [24.5, 37, 19.3, 4.7], [46.8, 69.5, 38.9, 16], [7.5, 25, 23.2, 14.3]],         # 4
        [[6.7, 14.1, 14.1, 13.4], [19.8, 60.1, 75, 46.8], [39.2, 71.4, 90.2, 60.5], [70.5, 62.8, 37, 17]],   # 5
        [[0.6, 1.6, 5.2, 5.2], [3, 19.8, 41.2, 43.8], [41.3, 72.3, 64.7, 60], [61.6, 84.4, 39.7, 7.2]],      # 6
        [[22.8, 24.9, 51.5, 33], [9, 17, 43.6, 28.1], [3.3, 7.2, 5.9, 4.7], [0.3, 1.7, 2.6, 2.1]],           # 7
        [[11.7, 40.2, 71.2, 69.6], [44, 88.8, 85.9, 32.6], [26.1, 86.6, 85.2, 36], [39.3, 81.9, 68.3, 25.1]],  # 8
        [[0.7, 16.5, 78.8, 64.8], [37.3, 66.7, 68.5, 35.8], [64.8, 74.2, 22.1, 8.6], [11.7, 15.9, 11.1, 7.7]],  # 9
    ]
    B_rel = [[1, 1, 1, 1]] * 4

    S_tab = [   # "/" stroke present  (only (1,1),(1,2) measured properly; the rest are rough)
        [[N, 90, 90, N], [N, 95.4, 65.4, N], [N, 95, 95, N], [N, N, N, 95]],   # 0
        [[N, 10, 70, N], [N, 63.3, 68.7, N], [N, 75, 78, N], [N, N, N, 1]],    # 1
        [[N, 75, 60, N], [N, 75.9, 86.8, N], [N, 93, 97, N], [N, N, N, 45]],   # 2
        [[N, 80, 85, N], [N, 93.9, 95, N], [N, 86, 88, N], [N, N, N, 45]],     # 3
        [[N, 75, 83, N], [N, 86.7, 88.7, N], [N, 78, 90, N], [N, N, N, 14]],   # 4
        [[N, 85, 90, N], [N, 86.8, 54.8, N], [N, 65, 60, N], [N, N, N, 25]],   # 5
        [[N, 95, 95, N], [N, 96.8, 93.8, N], [N, 90, 96, N], [N, N, N, 75]],   # 6
        [[N, 50, 67, N], [N, 61.3, 84.1, N], [N, 71, 94, N], [N, N, N, 27]],   # 7
        [[N, 88, 95, N], [N, 96, 97.6, N], [N, 92, 96, N], [N, N, N, 15]],     # 8
        [[N, 95, 87, N], [N, 97.9, 94.8, N], [N, 86, 96, N], [N, N, N, 25]],   # 9
    ]
    S_rel = [[0, 0.5, 0.5, 0], [0, 1, 1, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0.5]]

    # orientation index -> (table, reliability)
    tables = {0: (H_tab, H_rel), 1: (S_tab, S_rel), 2: (V_tab, V_rel), 3: (B_tab, B_rel)}

    class_counts = np.array([991, 1064, 990, 1030, 983, 915, 967, 1090, 1009, 961], dtype=float)

    # ------------------------------------------------------------------
    # fc: presence/absence vote from the measured frequencies
    #   logit_d = s * sum_f r_f [ log q_df + E_f * log((1-q_df)/q_df) ] + log prior_d
    # ------------------------------------------------------------------
    s = 0.25                                # temperature (features are correlated)
    fcw = np.zeros((10, 256))
    fcb = np.zeros(10)
    for d in range(10):
        fcb[d] = math.log(class_counts[d] / class_counts.sum())
        for k, (tab, rel) in tables.items():
            for i in range(4):
                for j in range(4):
                    v = tab[d][i][j]
                    r = rel[i][j]
                    if v is None or r == 0:
                        continue
                    q = min(max(v / 100.0, 0.03), 0.97)
                    idx = (4 + k) * 16 + i * 4 + j          # emptiness channel 4+k, cell (i, j)
                    fcw[d, idx] = s * r * math.log((1.0 - q) / q)
                    fcb[d] += s * r * math.log(q)

    return {
        "conv1.weight": w1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": w2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": fcw.astype(np.float32),
        "fc.bias": fcb.astype(np.float32),
    }
```
