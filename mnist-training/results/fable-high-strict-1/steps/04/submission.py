import numpy as np
import math

def build_weights():
    W = {}
    ANGLES = [0, 30, 60, 90, 120, 150]      # conv1 channels 1..6 ; 0 = fine ink, 7 = broad ink

    # ------------------------------------------------------------------ conv1
    c1 = np.zeros((8, 1, 5, 5), np.float32)
    b1 = np.zeros(8, np.float32)
    c1[0, 0, 1:4, 1:4] = 1.0 / 9          # ch0 fine ink (3x3 mean)
    b1[0] = -0.05
    c1[7, 0, :, :] = 1.0 / 25             # ch7 broad ink (5x5 mean)
    b1[7] = -0.1
    # oriented band filters: cells within perpendicular distance 1 of a line through
    # the centre at angle a get positive weight (sum 2), others negative (sum -4), bias -0.4
    for k, a in enumerate(ANGLES):
        th = math.radians(a)
        dx, dy = math.cos(th), -math.sin(th)          # direction (x right, y down); "/" for 0<a<90
        band = np.zeros((5, 5), bool)
        for i in range(5):
            for j in range(5):
                dist = abs((j - 2) * dy - (i - 2) * dx)
                band[i, j] = dist <= 1.0
        npos, nneg = band.sum(), 25 - band.sum()
        c1[1 + k, 0] = np.where(band, 2.0 / npos, -4.0 / nneg)
        b1[1 + k] = -0.4
    W['conv1.weight'] = c1
    W['conv1.bias'] = b1

    # ------------------------------------------------------------------ conv2
    # Pure pass-through with a single tap, so final cell (r,s) = max of conv1 channel
    # over input rows 4r+4..4r+11 (channels 0-7, centre tap) or 4r+2..4r+9 (8-15, tap (1,1)).
    c2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for c in range(8):
        c2[c, c, 2, 2] = 1.0
        c2[8 + c, c, 1, 1] = 1.0
    W['conv2.weight'] = c2
    W['conv2.bias'] = b2

    # ------------------------------------------------------------------ stroke descriptions
    # Each digit is a list of strokes in pixel coords (x = column, y = row), digit box 4..23.
    def seg(x0, y0, x1, y1):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(L / 0.5))
        phi = math.degrees(math.atan2(-(y1 - y0), x1 - x0)) % 180.0
        return [(x0 + (x1 - x0) * t / n, y0 + (y1 - y0) * t / n, phi, L / n) for t in range(n + 1)]

    def arc(cx, cy, r, th0, th1):
        # angles in degrees, math convention (th=90 is up); points (cx + r cos, cy - r sin)
        L = abs(math.radians(th1 - th0)) * r
        n = max(2, int(L / 0.5))
        out = []
        for t in range(n + 1):
            th = math.radians(th0 + (th1 - th0) * t / n)
            phi = (math.degrees(th) + 90.0) % 180.0       # tangent orientation
            out.append((cx + r * math.cos(th), cy - r * math.sin(th), phi, L / n))
        return out

    def ellipse(cx, cy, rx, ry):
        n = 120
        out = []
        for t in range(n):
            th = 2 * math.pi * t / n
            x, y = cx + rx * math.cos(th), cy - ry * math.sin(th)
            dxp, dyp = -rx * math.sin(th), -ry * math.cos(th)
            phi = math.degrees(math.atan2(-dyp, dxp)) % 180.0
            out.append((x, y, phi, 2 * math.pi * math.sqrt(rx * ry) / n))
        return out

    D = {
        0: ellipse(13.5, 13.5, 6.5, 9.0),
        1: seg(15, 4, 12.5, 23),
        2: arc(13.5, 9.5, 5, 170, -20) + seg(18.2, 11.2, 6.5, 22) + seg(6.5, 22, 21, 22),
        3: arc(13, 9, 4.5, 160, -90) + arc(13, 18.5, 5, 90, -160),
        4: seg(10, 4, 7.5, 15) + seg(7.5, 15, 21, 15) + seg(17, 4, 16, 23),
        5: seg(8, 5, 20, 5) + seg(8, 5, 7.5, 13) + arc(13, 17.5, 5.5, 130, -150),
        6: seg(17, 4, 11, 10) + seg(11, 10, 8.5, 16) + arc(13.5, 17.5, 5.5, 0, 360),
        7: seg(7, 5, 20, 5) + seg(20, 5, 11, 23),
        8: arc(13.5, 9.2, 4.7, 0, 360) + arc(13.5, 18, 5.5, 0, 360),
        9: arc(13.5, 9.5, 5, 0, 360) + seg(18.5, 10, 14.5, 23),
    }

    def ang_w(phi, a):
        d = abs(phi - a) % 180.0
        d = min(d, 180.0 - d)
        return max(0.0, 1.0 - d / 30.0)

    # rasterise strokes into the (8 feature, 4, 4) cell grid for a given receptive-field offset
    def make_template(strokes, off):
        acc = np.zeros((8, 4, 4), np.float32)
        for (x, y, phi, ds) in strokes:
            rows = [r for r in range(4) if 4 * r + 4 + off <= y <= 4 * r + 11 + off]
            cols = [s for s in range(4) if 4 * s + 4 + off <= x <= 4 * s + 11 + off]
            for r in rows:
                for s in cols:
                    acc[0, r, s] += ds
                    acc[7, r, s] += ds
                    for k, a in enumerate(ANGLES):
                        acc[1 + k, r, s] += ang_w(phi, a) * ds
        tpl = 1.0 - np.exp(-acc / 3.0)        # presence-like saturation (~3 px of stroke -> 0.63)
        # correlation matching: centre each 4x4 map over its cells
        for c in range(8):
            if tpl[c].max() > 0:
                tpl[c] = tpl[c] - tpl[c].mean()
        return tpl

    # ------------------------------------------------------------------ fc
    scale = 1.5
    fcw = np.zeros((10, 256), np.float32)
    for d in range(10):
        full = np.zeros((16, 4, 4), np.float32)
        full[0:8] = make_template(D[d], 0)     # centre-tap channels
        full[8:16] = make_template(D[d], -2)   # shifted-tap channels
        v = full.reshape(256)
        v = v / (np.linalg.norm(v) + 1e-6)
        fcw[d] = scale * v
    W['fc.weight'] = fcw
    W['fc.bias'] = np.zeros(10, np.float32)
    return W
