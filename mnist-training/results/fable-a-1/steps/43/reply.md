**Step 43 approach:** continue the temperature line search, with a second round of bias nudges.

- **Temperature:** scaling the logits by 0.85 lowered the loss from 0.335 to 0.318 with predictions essentially unchanged, so the model was overconfident. This step goes to 0.70.
- **Class biases:** the same imbalances remain, slightly reduced: 2 at 1060 predictions against 990 true, 8 and 1 a little high, 0, 4, 7 and 9 a little low. The biases move further in the same direction.

```python
import numpy as np
import math


def build_weights():
    # ------------------------------------------------------------------
    # Knobs
    # ------------------------------------------------------------------
    T0 = 0.25         # conv2 noise threshold on summed orientation response
    CLIP = 1.2        # conv2 saturation level (feature = min(relu(S-T0),CLIP)/CLIP)
    C1_BIAS = -0.1    # conv1 bias of line filters
    CORNER_BIAS = -1.05  # conv1 bias of inner-corner filters
    BLANK_W = -0.5       # "must be blank" weight inside a corner filter
    THETA = 0.9          # conv2 threshold of the loop detector
    GAMMA = 0.5          # trust factor for the loop evidence
    CC = 0.25            # saturation level of the corner cell feature
    NBAR = 1.5           # typical number of cells lit by one corner in a zone
    GAMMA_C = 0.33       # trust factor for the corner-zone evidence
    ZP_LO, ZP_HI = 0.03, 0.97   # clip for measured corner-zone rates
    G_HV = 0.45          # trust factor for horizontal / vertical cells (dense grid)
    G_D = 0.62           # trust factor for diagonal cells (checkerboard)
    OP_LO, OP_HI = 0.02, 0.98   # clip for measured orientation rates
    SCALE = 0.70         # overall temperature applied to all evidence (was 0.85)
    # per-class offsets from the prediction-count imbalance (steps 31, 41, 42)
    BIAS_ADJ = np.array([0.2, -0.2, -0.5, 0.0, 0.35, -0.05, -0.1, 0.25, -0.2, 0.35])

    # Loop evidence, from the measured firing rates of the loop detector
    # (upper half: step 30, lower half: step 15): slope per unit of loop response
    # and log-probability that the detector stays silent, per digit 0..9.
    HOLE_UP = np.array([0.06, -3.4, 0.6, 1.5, 1.9, 1.25, -2.1, 0.0, 3.2, 2.9])
    HOLE_LO = np.array([-0.94, -3.4, 1.06, -0.68, 0.26, -0.29, 3.0, -2.6, 3.4, -0.8])
    HOLE_NONE = np.array([-0.146, 0.0, -0.362, -0.346, -0.50, -0.319, -0.773,
                          -0.107, -1.753, -0.768])

    # Measured rate (steps 13-15) at which each corner type fires in the upper /
    # lower half of the 4x4 grid, per true digit 0..9.
    # index: [corner type 0..3 = TL, TR, BL, BR][zone 0 = upper, 1 = lower]
    ZONE_P = {
        (0, 0): [.95, .16, .39, .59, .34, .93, .62, .38, .94, .93],     # TL upper
        (0, 1): [.44, .20, .79, .15, .65, .14, .79, .38, .945, .25],    # TL lower
        (1, 0): [.97, .05, .97, .98, .16, .14, .22, .985, .86, .90],    # TR upper
        (1, 1): [.09, .02, .51, .94, .99, .91, .76, .145, .92, .95],    # TR lower
        (2, 0): [.15, .02, .10, .63, .71, .80, .575, .15, .915, .745],  # BL upper
        (2, 1): [.99, .06, .94, .49, .67, .47, .98, .08, .88, .47],     # BL lower
        (3, 0): [.40, .20, .66, .91, .73, .24, .22, .30, .86, .74],     # BR upper
        (3, 1): [.97, .18, .805, .96, .64, .93, .88, .42, .91, .44],    # BR lower
    }

    # Measured rate (steps 19-30 and 36-40) at which the clipped orientation feature
    # of a cell is "on", per true digit 0..9. Key = (orientation k, row a, col b);
    # k: 0 = horizontal, 1 = "/", 2 = vertical, 3 = "\".
    ORI_P = {
        # horizontal (all 16 cells)
        (0, 0, 0): [.217, .011, .623, .76, .045, .286, .013, .828, .312, .358],
        (0, 0, 1): [.863, .042, .936, .989, .153, .902, .169, .998, .911, .96],
        (0, 0, 2): [.986, .072, .954, .985, .122, .995, .389, .996, .99, .992],
        (0, 0, 3): [.882, .102, .557, .607, .119, .969, .301, .85, .876, .694],
        (0, 1, 0): [.206, .015, .373, .636, .516, .638, .016, .855, .248, .635],
        (0, 1, 1): [.436, .026, .485, .963, .691, .952, .363, .958, .674, .899],
        (0, 1, 2): [.42, .022, .398, .967, .658, .957, .82, .947, .809, .864],
        (0, 1, 3): [.258, .008, .128, .531, .346, .722, .81, .757, .568, .502],
        (0, 2, 0): [.098, .014, .628, .543, .895, .637, .182, .183, .213, .76],
        (0, 2, 1): [.14, .024, .82, .924, .99, .903, .766, .172, .779, .977],
        (0, 2, 2): [.255, .021, .846, .928, .984, .86, .956, .17, .805, .938],
        (0, 2, 3): [.253, .007, .634, .463, .554, .44, .888, .124, .316, .21],
        (0, 3, 0): [.862, .104, .904, .853, .542, .842, .484, .083, .517, .349],
        (0, 3, 1): [.998, .154, .994, .971, .68, .951, .993, .154, .90, .494],
        (0, 3, 2): [.991, .086, .98, .968, .619, .915, .995, .142, .798, .352],
        (0, 3, 3): [.685, .027, .88, .517, .28, .42, .78, .074, .27, .029],
        # vertical (15 of 16 cells)
        (2, 0, 0): [.466, .016, .275, .178, .659, .471, .456, .259, .631, .484],
        (2, 0, 1): [.677, .691, .439, .35, .831, .683, .90, .262, .877, .544],
        (2, 0, 2): [.515, .984, .841, .867, .834, .313, .746, .671, .726, .796],
        (2, 0, 3): [.928, .641, .921, .812, .964, .069, .144, .874, .822, .873],
        (2, 1, 0): [.941, .01, .179, .125, .89, .743, .874, .37, .698, .965],
        (2, 1, 1): [.804, .97, .312, .404, .89, .879, .957, .367, .948, .849],
        (2, 1, 2): [.425, .995, .889, .907, .946, .466, .624, .935, .854, .944],
        (2, 1, 3): [.998, .525, .924, .799, .983, .28, .532, .985, .743, .993],
        (2, 2, 0): [.999, .04, .447, .20, .884, .656, .991, .209, .619, .848],
        (2, 2, 1): [.666, .995, .461, .298, .782, .635, .977, .572, .966, .785],
        (2, 2, 2): [.397, .992, .844, .818, .975, .798, .708, .972, .936, .98],
        (2, 2, 3): [.995, .055, .705, .951, .926, .788, .929, .912, .579, .939],
        (2, 3, 0): [.99, .436, .723, .405, .228, .445, .891, .109, .872, .088],
        (2, 3, 1): [.508, .991, .474, .26, .705, .38, .921, .86, .957, .667],
        (2, 3, 3): [.796, .074, .359, .964, .535, .798, .653, .458, .679, .65],
        # "/" diagonal (checkerboard)
        (1, 0, 0): [.73, .012, .657, .616, .544, .442, .481, .554, .529, .844],
        (1, 0, 2): [.852, .727, .625, .909, .723, .882, .891, .523, .912, .846],
        (1, 1, 1): [.98, .682, .625, .955, .856, .908, .956, .618, .916, .985],
        (1, 1, 3): [.455, .376, .803, .691, .838, .217, .586, .835, .931, .817],
        (1, 2, 0): [.849, .129, .703, .535, .728, .637, .567, .263, .686, .445],
        (1, 2, 2): [.736, .719, .989, .783, .926, .525, .957, .96, .965, .966],
        (1, 3, 1): [.674, .73, .941, .669, .603, .671, .763, .816, .93, .669],
        (1, 3, 3): [.992, .009, .454, .937, .232, .75, .943, .452, .467, .359],
        # "\" diagonal (checkerboard)
        (3, 0, 0): [.032, .014, .053, .14, .108, .162, .01, .327, .345, .047],
        (3, 0, 2): [.79, .208, .915, .882, .217, .188, .18, .61, .79, .88],
        (3, 1, 1): [.049, .11, .275, .567, .567, .744, .432, .307, .917, .755],
        (3, 1, 3): [.892, .001, .314, .812, .089, .511, .554, .469, .483, .625],
        (3, 2, 0): [.42, .002, .263, .148, .574, .425, .565, .055, .404, .721],
        (3, 2, 2): [.119, .086, .604, .966, .522, .933, .683, .107, .90, .319],
        (3, 3, 1): [.854, .112, .467, .569, .357, .651, .906, .046, .83, .299],
        (3, 3, 3): [.015, .042, .679, .478, .228, .393, .259, .03, .414, .092],
    }

    # ------------------------------------------------------------------
    # conv1, filters 0..3: oriented line detectors
    # (0=horizontal, 45="/", 90=vertical, 135="\"), zero-sum, max response 1.
    # Profile across the stroke: +2 on the centre line, 0 at distance 1, -1 beyond.
    # ------------------------------------------------------------------
    def line_filter(theta_deg):
        th = math.radians(theta_deg)
        f = np.zeros((5, 5), dtype=np.float64)
        for r in range(5):
            for c in range(5):
                y = r - 2
                x = c - 2
                u = abs(x * math.sin(th) + y * math.cos(th))  # distance to the line
                f[r, c] = np.interp(u, [0.0, 1.0, 2.0, 3.0], [2.0, 0.0, -1.0, -1.0])
        pos = f[f > 0].sum()
        neg = -f[f < 0].sum()
        f[f < 0] *= pos / neg
        return f / pos

    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    conv1_b = np.zeros((8,), dtype=np.float64)
    for k in range(4):
        conv1_w[k, 0] = line_filter(45.0 * k)
        conv1_b[k] = C1_BIAS

    # ------------------------------------------------------------------
    # conv1, filters 4..7: inner-corner detectors, types 0..3 = TL, TR, BL, BR.
    # TL = ink along the top AND along the left, blank just below-right of centre.
    # Each arm alone sums to 1.0 (cancelled by the bias); both arms give 2.0.
    # ------------------------------------------------------------------
    TL = np.zeros((5, 5), dtype=np.float64)
    TL[0:2, 2:5] = 1.0 / 6.0    # top arm
    TL[2:5, 0:2] = 1.0 / 6.0    # left arm
    TL[2:4, 2:4] = BLANK_W      # inside of the concavity must be blank
    conv1_w[4, 0] = TL                  # type 0: TL
    conv1_w[5, 0] = TL[:, ::-1]         # type 1: TR
    conv1_w[6, 0] = TL[::-1, :]         # type 2: BL
    conv1_w[7, 0] = TL[::-1, ::-1]      # type 3: BR
    conv1_b[4:8] = CORNER_BIAS

    # ------------------------------------------------------------------
    # conv2, channels 0..7: clipped orientation presence
    #   channel k   = relu(boxsum3x3(orientation k) - T0)
    #   channel k+4 = relu(boxsum3x3(orientation k) - T0 - CLIP)
    #   presence y  = (channel k - channel k+4) / CLIP  in [0, 1]
    # ------------------------------------------------------------------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float64)
    conv2_b = np.zeros((16,), dtype=np.float64)
    for k in range(4):
        conv2_w[k, k, 1:4, 1:4] = 1.0
        conv2_b[k] = -T0
        conv2_w[k + 4, k, 1:4, 1:4] = 1.0
        conv2_b[k + 4] = -(T0 + CLIP)

    # ------------------------------------------------------------------
    # conv2, channels 8..11: closed-loop detectors for 4 loop sizes.
    # relu(TL(upper-left) + TR(upper-right) + BL(lower-left) + BR(lower-right) - THETA)
    # ------------------------------------------------------------------
    sizes = [(1, 1), (2, 2), (2, 1), (1, 2)]
    for i, (sy, sx) in enumerate(sizes):
        ch = 8 + i
        r0 = (4 - sy) // 2
        c0 = (4 - sx) // 2
        conv2_w[ch, 4, r0, c0] += 1.0
        conv2_w[ch, 5, r0, c0 + sx] += 1.0
        conv2_w[ch, 6, r0 + sy, c0] += 1.0
        conv2_w[ch, 7, r0 + sy, c0 + sx] += 1.0
        conv2_b[ch] = -THETA

    # ------------------------------------------------------------------
    # conv2, channels 12..15: saturating corner features, coded as ABSENCE:
    #   A = relu(CC - boxsum3x3(corner map t)); presence in a cell = 1 - A/CC.
    # ------------------------------------------------------------------
    for t in range(4):
        conv2_w[12 + t, 4 + t, 1:4, 1:4] = -1.0
        conv2_b[12 + t] = CC

    fc_w = np.zeros((10, 256), dtype=np.float64)
    fc_b = np.zeros((10,), dtype=np.float64)

    # ------------------------------------------------------------------
    # fc part 1: measured orientation cells.
    # With measured "on" rate p of presence feature y for class d:
    #   logit_d += g * ( log(p/(1-p)) * y + log(1-p) ),  g = G_HV or G_D
    # ------------------------------------------------------------------
    ob = np.zeros((10,), dtype=np.float64)
    for (k, a, b), plist in ORI_P.items():
        g = G_HV if k in (0, 2) else G_D
        p = np.clip(np.array(plist, dtype=np.float64), OP_LO, OP_HI)
        lo = np.log(p / (1.0 - p))
        for d in range(10):
            fc_w[d, k * 16 + a * 4 + b] = g * lo[d] / CLIP
            fc_w[d, (k + 4) * 16 + a * 4 + b] = -g * lo[d] / CLIP
            ob[d] += g * math.log(1.0 - p[d])
    ob -= ob.mean()
    fc_b += ob

    # ------------------------------------------------------------------
    # fc part 2: loop features (channels 8..11). Rows 0,1 = upper half, 2,3 = lower.
    # logit_d += GAMMA * (HOLE_NONE[d] + HOLE_UP[d]*H_up + HOLE_LO[d]*H_lo)
    # ------------------------------------------------------------------
    for d in range(10):
        for ch in range(8, 12):
            for a in range(4):
                for b in range(4):
                    v = HOLE_UP[d] if a < 2 else HOLE_LO[d]
                    fc_w[d, ch * 16 + a * 4 + b] = GAMMA * v
        fc_b[d] += GAMMA * HOLE_NONE[d]

    # ------------------------------------------------------------------
    # fc part 3: corner-zone evidence (channels 12..15, absence-coded).
    # N = number of cells of the zone (2 rows x 4 columns) in which the corner
    #     type is present = sum over cells of (1 - A/CC).
    #   logit_d += GAMMA_C * ( log(p/(1-p)) * N / NBAR + log(1-p) )
    # ------------------------------------------------------------------
    zb = np.zeros((10,), dtype=np.float64)
    for (t, z), plist in ZONE_P.items():
        p = np.clip(np.array(plist, dtype=np.float64), ZP_LO, ZP_HI)
        lo = np.log(p / (1.0 - p))
        rows = (0, 1) if z == 0 else (2, 3)
        for d in range(10):
            for a in rows:
                for b in range(4):
                    fc_w[d, (12 + t) * 16 + a * 4 + b] = -GAMMA_C * lo[d] / (CC * NBAR)
            zb[d] += GAMMA_C * (lo[d] * 8.0 / NBAR + math.log(1.0 - p[d]))
    zb -= zb.mean()
    fc_b += zb

    # per-class offsets, then the overall temperature on everything
    fc_b += BIAS_ADJ
    fc_w *= SCALE
    fc_b *= SCALE

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
```
