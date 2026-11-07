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
    # Pure pass-through, single tap: final cell (r,s) = max of conv1 channel over input
    # rows 4r+4..4r+11 (channels 0-7, centre tap) or 4r+2..4r+9 (channels 8-15, tap (1,1)).
    c2 = np.zeros((16, 8, 5, 5), np.float32)
    b2 = np.zeros(16, np.float32)
    for c in range(8):
        c2[c, c, 2, 2] = 1.0
        c2[8 + c, c, 1, 1] = 1.0
    W['conv2.weight'] = c2
    W['conv2.bias'] = b2

    # ------------------------------------------------------------------ stroke descriptions
    # Each digit is a list of hand-specified strokes in pixel coords (x = column, y = row).
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

    def ellipse(cx, cy, rx, ry, th0=0.0, th1=360.0):
        L = 2 * math.pi * math.sqrt(rx * ry) * abs(th1 - th0) / 360.0
        n = max(2, int(L / 0.5))
        out = []
        for t in range(n + 1):
            th = math.radians(th0 + (th1 - th0) * t / n)
            x, y = cx + rx * math.cos(th), cy - ry * math.sin(th)
            dxp, dyp = -rx * math.sin(th), -ry * math.cos(th)
            phi = math.degrees(math.atan2(-dyp, dxp)) % 180.0
            out.append((x, y, phi, L / n))
        return out

    D = {
        0: ellipse(13.5, 13.5, 7.0, 9.5),
        1: seg(15, 4, 12.5, 23),
        2: arc(13.5, 9.5, 5, 170, -20) + seg(18.2, 11.2, 6.5, 22) + seg(6.5, 22, 21, 22),
        3: arc(13, 9, 4.5, 160, -90) + arc(13, 18.5, 5, 90, -160),
        4: seg(10, 4, 7.5, 15) + seg(7.5, 15, 21, 15) + seg(17, 4, 16, 23),
        5: seg(8, 5, 20, 5) + seg(8, 5, 7.5, 13) + arc(13, 17.5, 5.5, 130, -150),
        6: seg(16, 4, 10.5, 10) + seg(10.5, 10, 8.5, 16) + arc(13.5, 17.5, 5.5, 0, 360),
        7: seg(7, 5, 20, 5) + seg(20, 5, 11, 23),
        # 8: upper loop (open at the bottom), lower loop (open at the top), joined by an X crossing
        8: ellipse(13.5, 8.5, 4.0, 4.0, -40, 220) + ellipse(13.5, 18.8, 5.0, 4.6, 145, 395)
           + seg(10.5, 11.5, 17.0, 16.0) + seg(16.5, 11.5, 10.0, 16.0),
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
        return 1.0 - np.exp(-acc / 3.0)       # presence-like saturation (~3 px of stroke -> 0.63)

    tpls = []
    for d in range(10):
        tpl = np.zeros((16, 4, 4), np.float32)
        tpl[0:8] = make_template(D[d], 0)      # centre-tap channels
        tpl[8:16] = make_template(D[d], -2)    # shifted-tap channels
        tpls.append(tpl.reshape(256))
    tpls = np.stack(tpls)                      # (10, 256)
    Sbar = float(tpls.sum(axis=1).mean())      # mean template mass

    # ------------------------------------------------------------------ fc : nearest template
    # logit_d = s * [ x.w_d  - (1-alpha)*lam_d*||t_d||^2 * sum(x)/Sbar  - alpha*lam_d*gamma*||t_d||^2 ]
    # (mass-scaled weight offset + fixed bias with estimated feature gain gamma), plus negative
    # evidence for unexpected ink / orientation.
    s, beta_ink, beta_ori = 0.6, 0.15, 0.08
    alpha, gamma = 0.5, 0.55
    m = {0: 0.86, 1: 1.00, 2: 1.04, 3: 1.05, 4: 0.93, 5: 1.00, 6: 0.97, 7: 0.93, 8: 0.98, 9: 0.99}
    ink_ch = (0, 7, 8, 15)
    fcw = np.zeros((10, 256), np.float32)
    fcb = np.zeros(10, np.float32)
    for d in range(10):
        t = tpls[d]
        wmap = t.copy().reshape(16, 4, 4)
        tmap = t.reshape(16, 4, 4)
        for c in range(16):
            b = beta_ink if c in ink_ch else beta_ori
            thr = 0.1 if c in ink_ch else 0.05
            wmap[c] = np.where(tmap[c] < thr, -b, tmap[c])
        lam = 0.5 * m[d]
        tt = float((t ** 2).sum())
        offset = (1.0 - alpha) * lam * tt / Sbar
        fcw[d] = s * (wmap.reshape(256) - offset)
        fcb[d] = -s * alpha * lam * gamma * tt
    W['fc.weight'] = fcw
    W['fc.bias'] = fcb
    return W
