## Step 14: start measuring the real class statistics

**What the step 13 probe showed.** Decoding the 3-bit codes:
- The small-loop detector is not discriminative. It fires on about 48% of 3s, 34% of 2s and 32% of 5s, but only 43% of 0s and 58% of 8s.
- It is fooled by two parallel strokes. Its four sides are averaged, so a full top side plus a full bottom side is nearly enough to fire it.
- The horizontal tube fires mostly on 3, 5 and 2.
- The probe mechanism itself works cleanly. Every true "1" landed in the "no feature" column, as it should.

**Why change strategy.** Thirteen steps of guessing templates have plateaued at about 64%. My hand-drawn prototypes don't match real MNIST statistics, and the feedback cannot tell me where they are wrong. Instead I will measure the class-conditional statistics directly.

**The plan.** Measure, for each digit, the probability that each orientation (horizontal, vertical, \, /) is present in each of the 4×4 cells. That is 64 binary features, measured 3 per step. I will then build a classifier from the measured probabilities, with naive-Bayes log-odds weights. Probe steps have huge losses, but only the lowest-loss step is scored, so they cost nothing.

**Probe features.**
- conv1 uses the step-9 line detectors on channels 1–4.
- conv2 passes each one through with only its centre tap, so a feature is the max-pooled line response over an 8-px image window.
- A feature is "present" if it exceeds 0.35. An aligned stroke gives about 0.8; a stroke 45° off gives about 0.3.

**This step** tests horizontal-stroke presence in grid cells (0,0), (0,1) and (0,2). Output class c (0–7) encodes the three yes/no answers, as in step 13: bit i of c is test i.

```python
import numpy as np
import math

def build_weights():
    W1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    W2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    Wf = np.zeros((10, 256), np.float32)
    bf = np.zeros(10, np.float32)

    # ---------------- conv1 ----------------
    # ch0: ink (Gaussian blur)
    G = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            G[i, j] = math.exp(-((i - 2) ** 2 + (j - 2) ** 2) / 2.0)
    W1[0, 0] = G / G.sum()
    b1[0] = -0.05
    # ch1..4: oriented line detectors (1=horiz, 2=vert, 3="\", 4="/")
    thetas = [0.0, math.pi / 2, math.pi / 4, 3 * math.pi / 4]
    for k, th in enumerate(thetas):
        K = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                r, c = i - 2, j - 2
                d = r * math.cos(th) - c * math.sin(th)
                l = r * math.sin(th) + c * math.cos(th)
                K[i, j] = (1 - d * d / 2.0) * math.exp(-d * d / 4.0) * math.exp(-l * l / 12.0)
        K -= K.mean()
        K /= K[K > 0].sum()
        W1[1 + k, 0] = K
        b1[1 + k] = -0.1

    # ---------------- conv2: pass-through (centre tap) of conv1 ch0..4 ----------------
    # final feature (ch, cell) = max of conv1 ch over an ~8px image window
    for k in range(5):
        W2[k, k, 2, 2] = 1.0

    # ---------------- fc: PROBE ----------------
    # tests: (conv2 channel, cell index = row*4+col); test true if feature > thr
    tests = [(1, 0), (1, 1), (1, 2)]   # horizontal presence in top-row cells 0,1,2
    thr = 0.35
    Kbig = 100.0
    for c in range(8):
        for i, (ch, cell) in enumerate(tests):
            s = 1.0 if (c >> i) & 1 else -1.0
            Wf[c, ch * 16 + cell] += Kbig * s
            bf[c] += -Kbig * s * thr
    bf[8] = -1e4
    bf[9] = -1e4

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
