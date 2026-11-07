**Step 7 — diagnosis.** 59.3%. The missing-stroke penalty worked for the sub-shape problem (9→4 and 4→9 are now balanced, 7→9 fell), but it shifted the class balance again: dense classes (8, 9) carry more "expected" cells and get penalised more, while 1 (fewest expected cells, most empty cells) collects the largest emptiness reward → 1 is predicted 1913 times, 8 only 399.

Change: instead of hand-tuning biases after each swing, I **normalise each class's ideal score**: compute from the template the logit a perfectly matching input would get (ink ≈ 4, orientation ≈ 3, emptiness ≈ 1.5 per unit) and set the bias to cancel it, so all ten classes share the same maximum logit. Small manual deltas on top (1 −0.3, 8 +0.3, 6 +0.15, 7 −0.15, 9 +0.1). W_MISS slightly reduced to 0.08 so natural shape variation of dense digits is penalised less.

```python
import numpy as np
import math

def build_weights():
    def clip01(v):
        return min(1.0, max(0.0, v))

    # ======================= conv1: 8 hand-drawn 5x5 feature detectors =======================
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    # ch0: ink detector (3x3 box). A ~2.5px stroke through the centre gives ~4.
    conv1_w[0, 0, 1:4, 1:4] = 0.55

    # ch1..ch6: oriented line detectors at 0,30,60,90,120,150 degrees
    # (0 = horizontal stroke, 90 = vertical, 45 = "\", 135 = "/").
    # Positive along the line (sum +5), negative flanks >=1.5px away (sum -3), bias -1.0.
    angles = [0, 30, 60, 90, 120, 150]
    for c, ang in enumerate(angles):
        phi = math.radians(ang)
        pos = np.zeros((5, 5)); neg = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                di, dj = i - 2, j - 2
                d = abs(di * math.cos(phi) - dj * math.sin(phi))   # distance from the line
                pos[i, j] = clip01((0.9 - d) / 0.4)
                neg[i, j] = clip01((d - 1.4) / 0.6)
        conv1_w[1 + c, 0] = 5.0 * pos / pos.sum() - 3.0 * neg / neg.sum()
        conv1_b[1 + c] = -1.0

    # ch7: emptiness detector: ReLU(1.5 - 0.25 * ink in 5x5) -> 1.5 on blank patches, 0 on strokes
    conv1_w[7, 0] = -0.25
    conv1_b[7] = 1.5

    # ======================= conv2: pass-through, two spatial grids =======================
    # out channel c   = conv1 channel c sampled at kernel tap (2,2)  -> grid A
    # out channel 8+c = conv1 channel c sampled at kernel tap (3,3)  -> grid B (shifted 2 px)
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    for c in range(8):
        conv2_w[c, c, 2, 2] = 1.0
        conv2_w[8 + c, c, 3, 3] = 1.0

    # ======================= fc: stroke templates =======================
    # Frame: x = (row-4)/4, y = (col-4)/4 -> the 20x20 digit box is [0,5]x[0,5], image centre x=2.5.
    # Grid A cell u responds to strokes near x = u+0.875, grid B near x = u+1.375 (same for columns).
    def cellw(x, centre):
        return clip01((0.9 - abs(x - centre)) / 0.4)

    def ellipse(cx, cy, rx, ry, n=32):
        return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n))
                for k in range(n + 1)]

    def sh(pts, dx=0.0, dy=0.0):       # shift a polyline (centre-of-mass correction)
        return [(x + dx, y + dy) for (x, y) in pts]

    # Hand-described digit prototypes: lists of polylines (x=row, y=col)
    digits = {
        0: [ellipse(2.5, 2.5, 2.3, 1.7)],
        1: [[(0.2, 2.85), (4.8, 2.15)]],                   # slightly slanted vertical stroke
        2: [sh([(1.5, 0.7), (0.8, 1.1), (0.3, 2.0), (0.3, 3.0), (0.8, 3.9), (1.5, 4.3),
                (2.3, 3.8), (3.2, 2.7), (4.0, 1.5), (4.7, 0.7), (4.7, 4.5)], dx=-0.35)],
        3: [sh([(0.6, 0.9), (0.3, 2.0), (0.4, 3.3), (1.0, 4.2), (1.8, 4.0), (2.4, 2.6),
                (2.8, 3.7), (3.8, 4.3), (4.6, 3.6), (4.8, 2.2), (4.4, 0.9)], dy=-0.3)],
        4: [[(0.4, 2.0), (3.0, 0.7), (3.0, 4.4)],          # left stroke + crossbar
            [(0.4, 3.6), (4.8, 3.4)]],                     # right vertical
        5: [sh([(0.3, 4.3), (0.3, 1.0), (2.3, 0.8), (2.1, 2.2), (2.5, 3.5), (3.4, 4.3),
                (4.3, 3.8), (4.8, 2.3), (4.4, 0.8)], dx=0.2, dy=0.2)],
        6: [sh([(0.2, 3.7), (1.0, 2.3), (2.0, 1.0), (3.0, 0.5)], dx=-0.5, dy=0.3),
            sh(ellipse(3.6, 2.3, 1.35, 1.7), dx=-0.5, dy=0.3)],
        7: [sh([(0.5, 0.8), (0.5, 4.3), (5.0, 1.8)], dx=0.6, dy=-0.35)],
        8: [ellipse(1.4, 2.5, 1.2, 1.5), ellipse(3.6, 2.5, 1.3, 1.7)],
        9: [sh(ellipse(1.5, 2.5, 1.3, 1.6), dx=0.5, dy=-0.2),
            sh([(1.5, 4.1), (4.0, 3.6), (4.8, 2.2)], dx=0.5, dy=-0.2)],
    }

    # Hand-placed negative evidence: (x, y, conv1 channel, strength).
    # 4 never has a horizontal stroke across the top centre (that is the closed top of 9/8/0).
    hand_negatives = {
        4: [(0.7, 2.0, 1, 0.12), (0.7, 3.0, 1, 0.12)],
    }

    def orient_weights(dx, dy):
        # soft-assign a stroke direction to the 6 orientation channels (30 deg spacing)
        phi = math.degrees(math.atan2(dx, dy)) % 180.0
        ws = []
        for ang in angles:
            dist = abs(phi - ang)
            dist = min(dist, 180.0 - dist)
            ws.append(clip01(1.0 - dist / 30.0))
        return ws

    def rasterise(polylines):
        # coverage T[grid, channel(0=ink, 1..6=orientation), u, v] in [0,1]
        T = np.zeros((2, 7, 4, 4))
        ds = 0.05
        for pl in polylines:
            for (x0, y0), (x1, y1) in zip(pl[:-1], pl[1:]):
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 1e-6:
                    continue
                ow = orient_weights(x1 - x0, y1 - y0)
                n = max(1, int(L / ds))
                for k in range(n):
                    t = (k + 0.5) / n
                    x = x0 + t * (x1 - x0); y = y0 + t * (y1 - y0)
                    for g in range(2):
                        off = 0.875 + 0.5 * g
                        for u in range(4):
                            wx = cellw(x, u + off)
                            if wx == 0.0:
                                continue
                            for v in range(4):
                                w = wx * cellw(y, v + off) * (L / n)
                                if w == 0.0:
                                    continue
                                T[g, 0, u, v] += w
                                for c in range(6):
                                    T[g, 1 + c, u, v] += w * ow[c]
        return np.clip(T / 0.6, 0.0, 1.0)

    templates = {d: rasterise(digits[d]) for d in range(10)}
    sizes = {d: templates[d].sum() for d in range(10)}
    mean_size = sum(sizes.values()) / 10.0

    P_SCALE = 2.5     # positive weight: per-class total = P_SCALE * (size/mean)^0.25
    W_NEG = 0.16      # per-unit penalty for ink in cells expected empty (ink channel)
    W_EMPTY = 0.14    # per-unit reward for emptiness channel in cells expected empty
    W_MISS = 0.08     # per-unit penalty for emptiness in cells where ink IS expected (missing stroke)

    # assumed feature responses of a perfectly matching digit (used only to equalise class maxima)
    R_INK, R_ORIENT, R_EMPTY = 4.0, 3.0, 1.5

    # small manual bias deltas on top of the equalised maxima (from step-6 confusions)
    manual = {0: 0.0, 1: -0.3, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.15, 7: -0.15, 8: 0.3, 9: 0.1}

    fc_w = np.zeros((10, 256), dtype=np.float32)
    fc_b = np.zeros(10, dtype=np.float32)
    for d in range(10):
        T = templates[d]
        wp = P_SCALE * (sizes[d] / mean_size) ** 0.25 / sizes[d]
        W = np.zeros((16, 4, 4))            # [conv2 channel, u, v]
        ideal = 0.0
        for g in range(2):
            ink = T[g, 0]
            empty = 1.0 - ink
            for c in range(7):
                W[g * 8 + c] += wp * T[g, c]            # expected ink / orientation
            W[g * 8 + 0] -= W_NEG * empty               # ink where none is expected
            W[g * 8 + 7] += W_EMPTY * empty             # emptiness where none is expected
            W[g * 8 + 7] -= W_MISS * ink                # emptiness where a stroke IS expected
            ideal += wp * (R_INK * ink.sum() + R_ORIENT * T[g, 1:7].sum()) + W_EMPTY * R_EMPTY * empty.sum()
            off = 0.875 + 0.5 * g
            for (hx, hy, ch, s) in hand_negatives.get(d, []):
                for u in range(4):
                    for v in range(4):
                        W[g * 8 + ch, u, v] -= s * cellw(hx, u + off) * cellw(hy, v + off)
        fc_w[d] = W.reshape(-1).astype(np.float32)      # flatten order = (channel,row,col)
        fc_b[d] = -ideal + manual[d]                     # equalise the maximum achievable logit

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
```
