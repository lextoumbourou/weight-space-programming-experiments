## Step 1: a hand-built orientation-histogram network with one drawn template per digit

**Conv1 (8 channels): oriented line detectors.**
- Each 5×5 kernel is a zero-sum difference of Gaussians in the direction across the stroke. It looks for a thin bright line at angles 0°, 22.5°, …, 157.5°.
- Each kernel is scaled so that a full-ink stroke lying along its centre band gives about 1.
- A bias of −0.3 cuts out weak responses from strokes at other angles.

**Conv2 (16 channels): orientation counts in coarse windows.**
- Each output channel adds up one conv1 orientation over a 3×3 block of pool1 cells, with weight 1/3 per tap. A stroke crossing the window then gives about 1.
- Channels 0–7 use taps 1..3. After pool2 this gives a 4×4 grid of windows that tiles input rows and columns 4..23.
- Channels 8–15 are the same windows moved 2 px down and to the right, for finer spatial sampling.
- The result is a histogram of stroke orientation at each grid location.

**FC: nearest-template classifier.**
- I describe each digit by hand as strokes: lines, arcs and ellipses in 28×28 coordinates.
- From that drawing I work out its template t_d geometrically. Each template value is the length of drawn stroke with a matching orientation that falls inside each window.
- The logit is α(2γ f·t_d − ‖t_d‖²). This is the negative squared distance between the features and the template, plus a term that is the same for every class.
- γ makes up for real conv1 responses being weaker than ideal.

```python
import numpy as np
import math

def build_weights():
    # ---------------- conv1: 8 oriented line detectors ----------------
    thetas = [k * math.pi / 8 for k in range(8)]   # line direction; 0=horizontal, pi/2=vertical (y down)
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float64)
    for k, th in enumerate(thetas):
        D = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                y, x = i - 2, j - 2
                D[i, j] = -x * math.sin(th) + y * math.cos(th)   # perpendicular distance to line
        narrow = np.exp(-D**2 / 2.0)
        wide = np.exp(-D**2 / (2 * 2.2**2))
        c = narrow.sum() / wide.sum()            # make kernel zero-sum (flat ink -> 0)
        w = narrow - c * wide
        R = w[np.abs(D) <= 1.2].sum()            # weight in the central band
        conv1_w[k, 0] = w / R                    # ideal stroke along the band -> ~1
    conv1_b = np.full(8, -0.3)                   # suppress weak / off-orientation responses

    # ---------------- conv2: orientation sums over 3x3 pool1 cells ----------------
    conv2_w = np.zeros((16, 8, 5, 5))
    for k in range(16):
        o = k % 8
        s = 0 if k < 8 else 1                    # s=1: window shifted 2 input px down-right
        for ty in range(1 + s, 4 + s):
            for tx in range(1 + s, 4 + s):
                conv2_w[k, o, ty, tx] = 1.0 / 3.0
    conv2_b = np.zeros(16)

    # ---------------- hand-drawn digit strokes (x right, y down) ----------------
    def line(p0, p1):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        n = int(L / 0.25) + 2
        return [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
                for t in np.linspace(0, 1, n)]

    def arc(cx, cy, rx, ry, a0, a1):
        n = int(abs(a1 - a0) / 2) + 2
        return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
                for a in np.linspace(a0, a1, n)]

    def poly(pts):
        out = []
        for a, b in zip(pts[:-1], pts[1:]):
            out += line(a, b)
        return out

    digits = {
        0: [arc(14, 14, 6, 9, 0, 360)],
        1: [line((15.5, 4.5), (12.5, 23.5))],
        2: [arc(14, 9.5, 5, 5, 190, 390), line((18.3, 12), (9, 23)), line((9, 23), (20, 23))],
        3: [arc(13.5, 9, 4.5, 4.5, 200, 450), arc(13.5, 18.5, 5, 5, 270, 520)],
        4: [line((11, 4), (8, 15)), line((8, 15), (20, 15)), line((17, 5), (17, 24))],
        5: [line((19, 4.5), (10.5, 4.5)), line((10.5, 4.5), (10, 12.5)),
            line((10, 12.5), (11, 13.7)), arc(13.5, 18, 5, 5, 240, 510)],
        6: [poly([(17.5, 4.5), (14, 6.5), (11, 10), (9.5, 14), (9, 18)]),
            arc(13.5, 18.5, 4.8, 4.8, 0, 360)],
        7: [line((8.5, 5), (20, 5)), line((20, 5), (13, 24))],
        8: [arc(14, 9.2, 4.3, 4.5, 0, 360), arc(14, 18.5, 5, 5, 0, 360)],
        9: [arc(14, 9.5, 5, 5, 0, 360), line((19, 9.5), (17, 24))],
    }

    th_arr = np.array(thetas)

    def soft_win(v, lo, hi):
        # 1 inside [lo,hi], linear ramp to 0 within 1 px outside
        below = np.clip(1 - (lo - v), 0, 1)
        above = np.clip(1 - (v - hi), 0, 1)
        return np.where(v < lo, below, np.where(v > hi, above, 1.0))

    def template(strokes):
        X, Y, L, P = [], [], [], []
        for st in strokes:
            for a, b in zip(st[:-1], st[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                l = math.hypot(dx, dy)
                if l < 1e-9:
                    continue
                X.append((a[0] + b[0]) / 2); Y.append((a[1] + b[1]) / 2)
                L.append(l); P.append(math.atan2(dy, dx) % math.pi)
        X, Y, L, P = map(np.array, (X, Y, L, P))
        # orientation membership (N,8)
        M = np.clip((np.cos(2 * (P[:, None] - th_arr[None, :])) - 0.3) / 0.7, 0, None)
        # window membership for conv2 positions r=0..7, shift s=0/1
        WY = np.zeros((len(X), 2, 8)); WX = np.zeros((len(X), 2, 8))
        for s in range(2):
            for r in range(8):
                lo, hi = 2 * r + 3.5 + 2 * s, 2 * r + 9.5 + 2 * s
                WY[:, s, r] = soft_win(Y, lo, hi)
                WX[:, s, r] = soft_win(X, lo, hi)
        v = np.einsum('n,no,ngr,ngc->gorc', L, M, WY, WX) / 6.0   # (2,8,8,8)
        v = v.reshape(16, 8, 8)                                    # channel = g*8+o
        t = v.reshape(16, 4, 2, 4, 2).max(axis=(2, 4))             # pool2 max
        return t.reshape(256)

    # ---------------- fc: nearest-template logits ----------------
    alpha, gamma = 0.6, 1.6
    fc_w = np.zeros((10, 256)); fc_b = np.zeros(10)
    for d in range(10):
        t = template(digits[d])
        fc_w[d] = alpha * 2 * gamma * t
        fc_b[d] = -alpha * np.dot(t, t)

    return {
        'conv1.weight': conv1_w.astype(np.float32),
        'conv1.bias': conv1_b.astype(np.float32),
        'conv2.weight': conv2_w.astype(np.float32),
        'conv2.bias': conv2_b.astype(np.float32),
        'fc.weight': fc_w.astype(np.float32),
        'fc.bias': fc_b.astype(np.float32),
    }
```
