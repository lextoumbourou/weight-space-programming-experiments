**Step 5 plan: switch the fc layer to nearest-prototype matching.**

The last several steps have all had the same problem. A linear template score mixes "does this digit's pattern match" with "how much ink is there", and the second term keeps favouring whichever class has a dense or centred template. Zero-centering fixed one bias and created another.

For Gaussian-like matching, the logit for class d is -½‖a − μ_d‖² = a·μ_d − ½‖μ_d‖² + const. This is an exact linear function of the features. Weights are μ_d, and the bias −½‖μ_d‖² removes the dependence on each prototype's overall ink level. Each class prototype is a hand-drawn expected-activity map. It is built from the step-4 stroke maps, mapped to [0, 1] as occupancy, so no template is zero-centred. I'm keeping the conv layers unchanged.

```python
import numpy as np


def _m(rows):
    return np.array(rows, dtype=np.float32)


def build_weights():
    # ------------------------------------------------------------------
    # conv1: 8 filters, each 1x5x5. Shape (out=8, in=1, 5, 5).
    # ------------------------------------------------------------------
    W1 = np.zeros((8, 1, 5, 5), dtype=np.float32)
    b1 = np.zeros(8, dtype=np.float32)

    r, c = np.meshgrid(np.arange(5), np.arange(5), indexing='ij')

    v = np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.5))
    W1[0, 0] = v                                   # vertical stroke
    W1[1, 0] = v.T                                 # horizontal stroke
    d = r + c - 4
    W1[2, 0] = np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.5))  # '/'
    d2 = r - c
    W1[3, 0] = np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.5))  # '\'
    inner = (np.abs(r - 2) <= 1) & (np.abs(c - 2) <= 1)
    W1[4, 0] = np.where(inner, 0.2, -0.1)          # centre-surround blob
    W1[5, 0] = np.where(r <= 1, 0.5, np.where(r == 2, 0.0, -0.5))  # top vs bottom
    W1[6, 0] = np.where((r == 2) & (c == 2), 1.0, 0.0)            # identity
    W1[7, 0] = 0.2                                 # local ink mass
    b1[7] = -0.3

    # ------------------------------------------------------------------
    # conv2: 16 filters, each 8x5x5. Output o uses conv1 channel o%8 with
    # spatial pattern P[o%8], plus a weaker input from channel (o+3)%8.
    # ------------------------------------------------------------------
    P = []
    P.append(np.where(c == 2, 1.0, np.where((c == 1) | (c == 3), 0.3, -0.3)))
    P.append(np.where(r == 2, 1.0, np.where((r == 1) | (r == 3), 0.3, -0.3)))
    P.append(np.where(d == 0, 1.0, np.where(np.abs(d) == 1, 0.3, -0.3)))
    P.append(np.where(d2 == 0, 1.0, np.where(np.abs(d2) == 1, 0.3, -0.3)))
    P.append(np.where(inner, 0.2, 0.0))
    P.append(np.where((r == 2) & (c == 2), 1.0, 0.0))
    P.append(np.where(r <= 1, 0.5, np.where(r >= 3, -0.5, 0.0)))
    P.append(np.where(r >= 3, 0.5, np.where(r <= 1, -0.5, 0.0)))
    P = [p.astype(np.float32) for p in P]

    W2 = np.zeros((16, 8, 5, 5), dtype=np.float32)
    b2 = np.full(16, -0.1, dtype=np.float32)
    for o in range(16):
        W2[o, o % 8] += P[o % 8]
        W2[o, (o + 3) % 8] += 0.5 * P[(o + 4) % 8]

    # ------------------------------------------------------------------
    # Hand-drawn stroke maps per class. Groups: V, H, '/', '\', blob/other.
    # Values: +1 strong expected stroke, 0 neutral, -1 expected empty.
    # ------------------------------------------------------------------
    Z = np.zeros((4, 4), dtype=np.float32)
    S = np.zeros((10, 5, 4, 4), dtype=np.float32)

    S[0] = [  # ring
        _m([[0, -0.5, -0.5, 0], [1, -0.5, -0.5, 1], [1, -0.5, -0.5, 1], [0, -0.5, -0.5, 0]]),
        _m([[0, 1, 1, 0], [-0.5, -0.5, -0.5, -0.5], [-0.5, -0.5, -0.5, -0.5], [0, 1, 1, 0]]),
        _m([[0.5, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0.5]]),
        _m([[0, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, -1, -1, 0], [0, -1, -1, 0], [0, 0, 0, 0]]),
    ]
    S[1] = [  # centre vertical stroke
        _m([[-0.5, 1, 1, -0.5]] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
        _m([[-0.3] * 4] * 4),
    ]
    S[2] = [  # top arc, '/' diagonal, bottom bar
        _m([[0, 0, 0, 0], [0, 0, 0.5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        _m([[0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]),
        _m([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0.5, 0, 0, 0]]),
        Z.copy(),
        Z.copy(),
    ]
    S[3] = [  # right-side bulges, top and bottom arcs
        _m([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]),
        _m([[0, 1, 1, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]
    S[4] = [  # right stem, crossbar, '/' upper-left diagonal
        _m([[0.5, 0, 1, 0], [0.5, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 1, 0, 0], [0.5, 0, 0, 0], [0, 0, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [-0.5, -0.5, 0, 0]]),
    ]
    S[5] = [  # top bar, left stem, bowl at bottom
        _m([[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0.5], [0, 0, 0, 0]]),
        _m([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, -0.5, -0.5, -0.5], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ]
    S[6] = [  # left stroke running down into a lower loop
        _m([[0.5, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]),
        _m([[0, 1, 0, 0], [0.5, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, -0.5], [0, 0, 0, -0.5], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ]
    S[7] = [  # top bar, '/' stem down the centre-left
        _m([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0.5, 0, 0], [0, 0.5, 0, 0]]),
        _m([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        _m([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0.5, 0, 0]]),
        Z.copy(),
        _m([[0, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]
    S[8] = [  # two stacked loops
        _m([[0.5, 0, 0, 0.5], [1, 0, 0, 1], [1, 0, 0, 1], [0.5, 0, 0, 0.5]]),
        _m([[0, 1, 1, 0], [0, 0.5, 0.5, 0], [0, 0.5, 0.5, 0], [0, 1, 1, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, 0.5, 0.5, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0]]),
    ]
    S[9] = [  # closed top loop, right stem descending
        _m([[0, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0.5, 1], [0, 0, 0.5, 1]]),
        _m([[0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.5, 0, 0]]),
        Z.copy(),
        Z.copy(),
        _m([[0, 0, 0, 0], [0, -0.5, -0.5, 0], [-0.5, 0, 0, 0], [-0.5, 0, 0, 0]]),
    ]

    # Convert to expected occupancy in [0, 1]: 0.5 + 0.5*S (S=+1 -> 1, S=-1 -> 0).
    occ = np.clip(0.5 + 0.5 * S, 0.0, 1.0)

    # Prototype for class d, conv2 channel ch, cell k: mu[d, ch, k].
    pattern_group = [0, 1, 2, 3, 4, 4, 4, 4]
    ALPHA = 1.0    # assumed scale of pooled conv2 activity
    BETA = 0.03    # logit scale
    mu = np.zeros((10, 256), dtype=np.float32)
    for d_cls in range(10):
        for ch in range(16):
            g = pattern_group[ch % 8]
            mu[d_cls, ch * 16:(ch + 1) * 16] = ALPHA * occ[d_cls, g].reshape(16)

    # Gaussian-matching form: logit_d = BETA * (a . mu_d - 0.5 * ||mu_d||^2).
    Wfc = (BETA * mu).astype(np.float32)
    bfc = (-0.5 * BETA * np.sum(mu * mu, axis=1)).astype(np.float32)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wfc,
        "fc.bias": bfc,
    }
```
