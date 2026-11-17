**Step 13 plan.** Step 12 was slightly worse than step 9 (0.6579 against 0.6561). The re-weighting alone cannot cost that much, so the Λ/V corner term adds more noise than signal on top of the other features and I remove it again. The single-feature probes show that orientation statistics are what carries information here, so I build the same vertical-versus-horizontal measurement at coarser scales, where it should reflect body pose and scene structure rather than fur:

- **Mid scale (conv2):** four new channels take rectified x and y derivatives of the pooled brightness map, about 2.5 px scale.
- **Coarse scale (conv3):** four channels take Sobel derivatives of the pooled brightness map on 4 px cells.

This step is a clean probe of the mid-scale contrast alone: the logit is `2.5 * (V_mid − H_mid)`.

```python
import numpy as np


def build_weights():
    LUM = np.array([0.299, 0.587, 0.114])

    def gauss(size, sigma):
        ax = np.arange(size) - (size - 1) / 2.0
        g = np.exp(-(ax[:, None] ** 2 + ax[None, :] ** 2) / (2 * sigma ** 2))
        return g / g.sum()

    # ------------------------------------------------------------------
    # conv1: 16 channels
    #  0..7  : directional luminance gradients, direction d*45deg
    #          (d=0 brighter to the right, d=2 brighter below, d=1 brighter lower-right ...)
    #  8 green, 9 warm (R-B), 10 cool (B-R), 11 brightness, 12 darkness,
    #  13 small dark spot (DoG), 14 small bright spot (DoG), 15 pink/magenta
    # ------------------------------------------------------------------
    W1 = np.zeros((16, 3, 5, 5))
    b1 = np.zeros(16)
    ax = np.arange(5) - 2.0
    Y, X = np.meshgrid(ax, ax, indexing="ij")  # Y = row offset (down), X = column offset (right)
    G = np.exp(-(X ** 2 + Y ** 2) / 2.0)
    for d in range(8):
        th = d * np.pi / 4
        k = (np.cos(th) * X + np.sin(th) * Y) * G
        k = k / k[k > 0].sum() * 2.0
        for c in range(3):
            W1[d, c] = k * LUM[c]
        b1[d] = -0.02  # small noise threshold

    B5 = gauss(5, 1.2)

    def setcol(ch, rgb, gain, bias=0.0):
        for c in range(3):
            W1[ch, c] = gain * rgb[c] * B5
        b1[ch] = bias

    setcol(8, (-0.5, 1.0, -0.5), 4.0)      # green  (grass)
    setcol(9, (1.0, 0.0, -1.0), 2.5)       # warm
    setcol(10, (-1.0, 0.0, 1.0), 4.0)      # cool
    setcol(11, LUM, 1.0)                   # brightness
    setcol(12, -LUM, 2.5, 1.0)             # darkness = 2.5*(0.4 - Y)
    setcol(15, (0.5, -1.0, 0.5), 4.0)      # pink / magenta
    dog = gauss(5, 1.6) - gauss(5, 0.7)    # surround minus centre
    for c in range(3):
        W1[13, c] = 3.0 * dog * LUM[c]     # small dark spot / thin dark line
        W1[14, c] = -3.0 * dog * LUM[c]    # small bright spot / thin bright line
    b1[13] = b1[14] = -0.02

    # ------------------------------------------------------------------
    # conv2: 32 channels on the 30x30 pooled maps (1 cell = 2 px)
    #  0 Lambda (bright inside)   1 Lambda (dark inside)
    #  2 V (bright inside)        3 V (dark inside)
    #  4..7 pooled diagonal edges E1,E3,E5,E7 ; 24..27 pooled E2,E6,E0,E4
    #  8 larger dark blob (nose) ; 16 small dark blob (eye) ; 17 small bright blob
    #  10..15 pooled green, warm, cool, pink, bright, dark
    #  18,19 pooled fine dark / bright spots ; 20 texture energy ; 21 smoothness
    #  22 vertical thin line ; 23 horizontal thin line
    #  28,29 mid-scale brightness gradient to the right / to the left  (vertical structures)
    #  30,31 mid-scale brightness gradient downwards / upwards         (horizontal structures)
    # ------------------------------------------------------------------
    W2 = np.zeros((32, 16, 5, 5))
    b2 = np.zeros(32)

    def arm(p0, p1, sigma=0.6):
        # soft line segment drawn in a 5x5 kernel, (row, col) coordinates
        p0 = np.array(p0, float)
        p1 = np.array(p1, float)
        v = p1 - p0
        L2 = (v ** 2).sum()
        w = np.zeros((5, 5))
        for r in range(5):
            for c in range(5):
                p = np.array([r, c], float)
                t = np.clip(((p - p0) * v).sum() / L2, 0, 1)
                dd = ((p - (p0 + t * v)) ** 2).sum()
                w[r, c] = np.exp(-dd / (2 * sigma ** 2))
        return w / w.sum()

    LamL = arm((4.3, 0.0), (0.3, 2.0))   # left arm "/" of the Lambda
    LamR = arm((4.3, 4.0), (0.3, 2.0))   # right arm "\" of the Lambda
    VL = LamL[::-1].copy()               # left arm "\" of the V
    VR = LamR[::-1].copy()               # right arm "/" of the V

    def shape2(ch, armA, posA, armB, posB, inhA, inhB, bias):
        for e, w in posA:
            W2[ch, e] += 0.5 * w * armA
        for e, w in posB:
            W2[ch, e] += 0.5 * w * armB
        for e in inhA:                      # wrong diagonal orientation on that arm -> inhibit
            W2[ch, e] -= 0.25 * armA
        for e in inhB:
            W2[ch, e] -= 0.25 * armB
        b2[ch] = bias

    shape2(0, LamL, [(1, .6), (0, .4)], LamR, [(3, .6), (4, .4)], [3, 7], [1, 5], -0.08)
    shape2(1, LamL, [(5, .6), (4, .4)], LamR, [(7, .6), (0, .4)], [3, 7], [1, 5], -0.08)
    shape2(2, VL, [(7, .6), (0, .4)], VR, [(5, .6), (4, .4)], [1, 5], [3, 7], -0.08)
    shape2(3, VL, [(3, .6), (4, .4)], VR, [(1, .6), (0, .4)], [1, 5], [3, 7], -0.08)

    P5 = gauss(5, 1.3)
    for ch, src in [(4, 1), (5, 3), (6, 5), (7, 7), (24, 2), (25, 6), (26, 0), (27, 4),
                    (10, 8), (11, 9), (12, 10), (13, 15), (14, 11), (15, 12),
                    (18, 13), (19, 14)]:
        W2[ch, src] = P5                    # plain local pooling

    Gc = gauss(5, 0.8)
    ring = np.ones((5, 5)); ring[1:4, 1:4] = 0; ring /= ring.sum()
    C3 = np.zeros((5, 5)); C3[1:4, 1:4] = 1 / 9.0
    W2[16, 12] = 1.2 * (Gc - ring); W2[16, 11] = 1.0 * (ring - Gc); b2[16] = -0.15  # small dark blob
    W2[17, 11] = 1.0 * (Gc - ring); b2[17] = -0.15                                   # small bright blob
    W2[8, 12] = 1.2 * (C3 - ring); W2[8, 11] = 1.0 * (ring - C3); b2[8] = -0.15      # larger dark blob
    for d in range(8):
        W2[20, d] = P5                      # texture energy = sum of all edge channels
        W2[21, d] = -P5                     # smoothness = relu(0.3 - texture)
    b2[21] = 0.3
    vl = np.zeros((5, 5)); vl[:, 2] = 0.2; vl[:, 0] = -0.1; vl[:, 4] = -0.1
    W2[22, 13] = vl; W2[22, 14] = vl; b2[22] = -0.03        # vertical thin line (cage bars)
    W2[23, 13] = vl.T; W2[23, 14] = vl.T; b2[23] = -0.03    # horizontal thin line

    # mid-scale derivative-of-Gaussian on the pooled brightness map (sigma = 1.3 cells = 2.6 px)
    Gm = np.exp(-(X ** 2 + Y ** 2) / (2 * 1.3 ** 2))
    kx = X * Gm
    kx = kx / kx[kx > 0].sum() * 2.0        # unit step edge -> 2.0 (same gain as the fine edges)
    ky = kx.T
    W2[28, 11] = kx;  b2[28] = -0.02        # brighter to the right
    W2[29, 11] = -kx; b2[29] = -0.02        # brighter to the left
    W2[30, 11] = ky;  b2[30] = -0.02        # brighter below
    W2[31, 11] = -ky; b2[31] = -0.02        # brighter above

    # ------------------------------------------------------------------
    # conv3: 32 channels on 13x13 maps (1 cell = 4 px)
    #  0..3 small Lambda/V passed on ; 4..7 large Lambda/V from pooled edges
    #  8,9   coarse brightness gradient right / left   (Sobel on 4px cells)
    #  29,30 coarse brightness gradient down / up
    #  10..15 colour means ; 16,17 blobs ; 18,19 fine spots ; 20 texture ; 21 smooth ; 22,23 lines
    #  24,25,26 fine horizontal / vertical / diagonal edge energy ; 27 grass (green AND texture)
    #  28 mid-scale vertical-structure energy ; 31 mid-scale horizontal-structure energy
    # ------------------------------------------------------------------
    W3 = np.zeros((32, 32, 3, 3))
    b3 = np.zeros(32)
    M3 = np.outer([0.6, 1, 0.6], [0.6, 1, 0.6]); M3 /= M3.sum()   # local mean
    S3 = 3.0 * M3                                                # local (soft) sum for sparse detectors
    for ch in (0, 1, 2, 3):
        W3[ch, ch] = S3

    LA = np.array([[0, 0.8, 0], [0.9, 0.3, 0], [1.0, 0, 0]]); LA /= LA.sum()  # left arm of big Lambda
    RA = LA[:, ::-1].copy()
    VLA = LA[::-1].copy()
    VRA = RA[::-1].copy()

    def shape3(ch, armA, posA, armB, posB, inhA, inhB, bias, gain=3.0):
        for e, w in posA:
            W3[ch, e] += gain * 0.5 * w * armA
        for e, w in posB:
            W3[ch, e] += gain * 0.5 * w * armB
        for e in inhA:
            W3[ch, e] -= gain * 0.25 * armA
        for e in inhB:
            W3[ch, e] -= gain * 0.25 * armB
        b3[ch] = bias

    # conv2 pooled edge channels: E1->4, E3->5, E5->6, E7->7, E2->24, E6->25, E0->26, E4->27
    shape3(4, LA, [(4, .6), (26, .4)], RA, [(5, .6), (27, .4)], [5, 7], [4, 6], -0.08)   # big Lambda bright
    shape3(5, LA, [(6, .6), (27, .4)], RA, [(7, .6), (26, .4)], [5, 7], [4, 6], -0.08)   # big Lambda dark
    shape3(6, VLA, [(7, .6), (26, .4)], VRA, [(6, .6), (27, .4)], [4, 6], [5, 7], -0.08) # big V bright
    shape3(7, VLA, [(5, .6), (27, .4)], VRA, [(4, .6), (26, .4)], [4, 6], [5, 7], -0.08) # big V dark

    # coarse Sobel gradients of the pooled brightness map (conv2 channel 14)
    sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float) / 4.0 * 2.0   # unit step -> 2.0
    sy = sx.T
    W3[8, 14] = sx;   b3[8] = -0.02       # brighter to the right
    W3[9, 14] = -sx;  b3[9] = -0.02       # brighter to the left
    W3[29, 14] = sy;  b3[29] = -0.02      # brighter below
    W3[30, 14] = -sy; b3[30] = -0.02      # brighter above

    for ch in (10, 11, 12, 13, 14, 15, 18, 19, 20, 21):
        W3[ch, ch] = M3
    for ch in (16, 17, 22, 23):
        W3[ch, ch] = S3
    W3[24, 24] = M3; W3[24, 25] = M3                       # fine horizontal edge energy
    W3[25, 26] = M3; W3[25, 27] = M3                       # fine vertical edge energy
    for src in (4, 5, 6, 7):
        W3[26, src] = 0.5 * M3                             # fine diagonal edge energy
    W3[27, 10] = M3; W3[27, 20] = 0.8 * M3; b3[27] = -0.8  # grass = green AND textured
    W3[28, 28] = M3; W3[28, 29] = M3                       # mid-scale vertical structures   (x-gradients)
    W3[31, 30] = M3; W3[31, 31] = M3                       # mid-scale horizontal structures (y-gradients)

    # ------------------------------------------------------------------
    # fc: logit difference (dog - cat) = sum_k w_k * (<profile_k, map_k> - centre_k)
    # ------------------------------------------------------------------
    UNI = np.ones((5, 5)) / 25.0

    # Probe of this step (alone): z = 2.5 * (V_mid - H_mid)
    terms = [
        (28, +2.5, UNI, 0.0),
        (31, -2.5, UNI, 0.0),
    ]
    extra_bias = 0.0

    Wf = np.zeros((2, 800))
    bf = np.zeros(2)
    bias_diff = extra_bias
    for ch, w, prof, centre in terms:
        Wf[1, ch * 25:(ch + 1) * 25] += 0.5 * w * prof.reshape(-1)
        Wf[0, ch * 25:(ch + 1) * 25] += -0.5 * w * prof.reshape(-1)
        bias_diff -= w * centre
    bf[1] = 0.5 * bias_diff
    bf[0] = -0.5 * bias_diff

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "conv3.weight": W3.astype(np.float32),
        "conv3.bias": b3.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
```
