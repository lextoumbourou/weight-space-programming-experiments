import numpy as np
import math

def build_weights():
    PI = math.pi
    # ================= conv1 =================
    # ch0-3: oriented line detectors; ch4: ink; ch5-7 unused
    # line directions (x right, y down): 0=H, 1="\" (pi/4), 2=V, 3="/" (3pi/4)
    W1 = np.zeros((8, 1, 5, 5)); b1 = np.zeros(8)
    phis = [0.0, PI / 4, PI / 2, 3 * PI / 4]
    for k, phi in enumerate(phis):
        vals = {}
        for r in range(5):
            for c in range(5):
                x, y = c - 2, r - 2
                if x * x + y * y <= 5:
                    d = abs(-math.sin(phi) * x + math.cos(phi) * y)
                    vals[(r, c)] = math.exp(-d * d / 2.0)
        m = np.mean(list(vals.values()))
        for (r, c), v in vals.items():
            W1[k, 0, r, c] = v - m
        W1[k] /= W1[k][W1[k] > 0].sum()
        b1[k] = -0.15
    W1[4, 0, 1:4, 1:4] = 1.0 / 9.0      # ink

    # ================= conv2 =================
    W2 = np.zeros((16, 8, 5, 5)); b2 = np.zeros(16)
    # ch 0-7: orientation k at shift s (ch = 2k+s); 2x2 block at rows/cols (1+s)..(2+s)
    #   final cell (i,j) centre: y = 6.5+2s+4i, x = 6.5+2s+4j
    for k in range(4):
        for s in range(2):
            W2[2 * k + s, k, 1 + s:3 + s, 1 + s:3 + s] = 0.5
    # ch 8-11: ink at shift (sy,sx) (ch = 8+2sy+sx)
    for sy in range(2):
        for sx in range(2):
            W2[8 + 2 * sy + sx, 4, 1 + sy:3 + sy, 1 + sx:3 + sx] = 0.5
    # ch 12-15: curve parts. Input channel ids: H=0, "\"=1, V=2, "/"=3
    H, BS, V, FS = 0, 1, 2, 3
    def put(ch, cin, cells):
        for (r, c, w) in cells:
            W2[ch, cin, r, c] += w
    # 12: cap  (∩) - centre of curvature below the stroke
    put(12, H,  [(1, 1, .5), (1, 2, 1), (1, 3, .5)])
    put(12, FS, [(2, 1, 1), (2, 0, .5), (3, 0, .3)])
    put(12, BS, [(2, 3, 1), (2, 4, .5), (3, 4, .3)])
    # 13: cup  (∪) - centre above
    put(13, H,  [(3, 1, .5), (3, 2, 1), (3, 3, .5)])
    put(13, BS, [(2, 1, 1), (2, 0, .5), (1, 0, .3)])
    put(13, FS, [(2, 3, 1), (2, 4, .5), (1, 4, .3)])
    # 14: left side (⊂) - centre to the right
    put(14, V,  [(1, 1, .5), (2, 1, 1), (3, 1, .5)])
    put(14, FS, [(1, 2, 1), (0, 2, .5), (0, 3, .3)])
    put(14, BS, [(3, 2, 1), (4, 2, .5), (4, 3, .3)])
    # 15: right side (⊃) - centre to the left
    put(15, V,  [(1, 3, .5), (2, 3, 1), (3, 3, .5)])
    put(15, BS, [(1, 2, 1), (0, 2, .5), (0, 1, .3)])
    put(15, FS, [(3, 2, 1), (4, 2, .5), (4, 1, .3)])
    for ch in range(12, 16):
        W2[ch] *= 0.7
        b2[ch] = -0.7 * 1.8      # needs more than one straight piece to fire
    # curve feature final cell centre: y = 7.5+4i, x = 7.5+4j

    # ================= digit drawings =================
    def seg(p0, p1):
        p0 = np.array(p0, float); p1 = np.array(p1, float)
        L = np.linalg.norm(p1 - p0)
        n = max(2, int(L / 0.25) + 1)
        t = np.linspace(0, 1, n)[:, None]
        return p0 + (p1 - p0) * t

    def arc(cx, cy, rx, ry, t0, t1, rot=0.0):
        n = int(abs(t1 - t0) * max(rx, ry) / 0.25) + 2
        t = np.linspace(t0, t1, n)
        x0 = rx * np.cos(t); y0 = ry * np.sin(t)
        x = cx + x0 * math.cos(rot) - y0 * math.sin(rot)
        y = cy + x0 * math.sin(rot) + y0 * math.cos(rot)
        return np.stack([x, y], axis=1)

    digits = {
        0: [[arc(14, 14, 7, 9.5, 0, 2 * PI)],
            [arc(14, 14, 6.5, 9.5, 0, 2 * PI, rot=0.3)]],
        1: [[seg((14, 4.5), (14, 23.5))],
            [seg((16.5, 4.5), (11.5, 23.5))]],
        2: [[arc(14, 10, 5.5, 5, -PI, 0.5),
             seg((18.8, 12.4), (8, 23)),
             seg((8, 23), (21, 22.5))]],
        3: [[arc(13.5, 8.8, 5, 4.3, -2.6, PI / 2),
             seg((10.5, 13.2), (13.5, 13.1)),
             arc(13.5, 18.5, 6, 5.4, -PI / 2, 2.6)]],
        4: [[seg((15, 4.5), (7.5, 17)), seg((7.5, 17), (21, 17)),
             seg((17.5, 9), (17, 23.5))],
            [seg((9, 4.5), (8, 16.5)), seg((8, 16.5), (21, 16.5)),
             seg((17.5, 4.5), (17, 23.5))]],
        5: [[seg((20, 4.5), (10.5, 4.5)), seg((10.5, 4.5), (9.5, 12.5)),
             arc(13.5, 17.2, 6, 5.8, -2.2, 2.6)]],
        6: [[arc(19, 16, 9.5, 11.5, -1.75, -PI),
             arc(14, 18.3, 5, 5, 0, 2 * PI)]],
        7: [[seg((8, 5), (20.5, 5)), seg((20.5, 5), (12.5, 23.5))]],
        8: [[arc(14, 9, 4.5, 4.5, 0, 2 * PI),
             arc(14, 18.5, 5.5, 5, 0, 2 * PI)]],
        9: [[arc(13.5, 9.5, 5, 5, 0, 2 * PI), seg((18.5, 10), (18, 23.5))],
            [arc(14, 9.5, 5, 5, 0, 2 * PI), seg((19, 10), (15, 23.5))]],
    }

    def gauss_grid(px, py, cy0, cx0, sig):
        # px,py: (N,) ; returns (N,4,4) spatial weights for grid y=cy0+4i, x=cx0+4j
        cy = cy0 + 4.0 * np.arange(4); cx = cx0 + 4.0 * np.arange(4)
        gy = np.exp(-(py[:, None] - cy[None, :]) ** 2 / (2 * sig ** 2))
        gx = np.exp(-(px[:, None] - cx[None, :]) ** 2 / (2 * sig ** 2))
        return gy[:, :, None] * gx[:, None, :]

    arc_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]   # ∩, ∪, ⊂, ⊃ : curvature direction

    def features(strokes):
        F_or = np.zeros((8, 4, 4)); F_ink = np.zeros((4, 4, 4)); F_arc = np.zeros((4, 4, 4))
        for pts in strokes:
            d = pts[1:] - pts[:-1]
            mid = 0.5 * (pts[1:] + pts[:-1])
            ds = np.linalg.norm(d, axis=1)
            ang = np.arctan2(d[:, 1], d[:, 0])
            # orientation maps
            for s in range(2):
                g = gauss_grid(mid[:, 0], mid[:, 1], 6.5 + 2 * s, 6.5 + 2 * s, 2.5)
                for k, phi in enumerate(phis):
                    ow = np.maximum(0.0, np.cos(2 * (ang - phi))) ** 2
                    F_or[2 * k + s] += np.tensordot(ds * ow, g, axes=(0, 0))
            # ink maps
            for sy in range(2):
                for sx in range(2):
                    g = gauss_grid(mid[:, 0], mid[:, 1], 6.5 + 2 * sy, 6.5 + 2 * sx, 2.5)
                    F_ink[2 * sy + sx] += np.tensordot(ds, g, axes=(0, 0))
            # curvature
            if len(pts) >= 3:
                Tu = d / np.maximum(ds[:, None], 1e-9)
                dT = Tu[1:] - Tu[:-1]
                dsm = 0.5 * (ds[1:] + ds[:-1])
                K = dT / np.maximum(dsm[:, None], 1e-9)     # curvature vector
                kap = np.linalg.norm(K, axis=1)
                Kh = K / np.maximum(kap[:, None], 1e-9)
                loc = pts[1:-1] + 2.0 * Kh                    # shift toward centre
                g = gauss_grid(loc[:, 0], loc[:, 1], 7.5, 7.5, 3.0)
                for a, (ux, uy) in enumerate(arc_dirs):
                    w = np.maximum(0.0, Kh[:, 0] * ux + Kh[:, 1] * uy) ** 2
                    w = w * np.minimum(kap * 4.0, 1.5) * dsm
                    F_arc[a] += np.tensordot(w, g, axes=(0, 0))
        F_or = 1 - np.exp(-F_or / 2.5)
        F_ink = 1 - np.exp(-F_ink / 2.5)
        F_arc = 1 - np.exp(-F_arc / 3.0)
        return F_or, F_ink, F_arc

    g_or, g_ink, g_arc = 1.0, 0.6, 0.8
    Tn = np.zeros((10, 16, 4, 4))
    for dgt in range(10):
        fs = [features(v) for v in digits[dgt]]
        Fo = np.mean([f[0] for f in fs], axis=0)
        Fi = np.mean([f[1] for f in fs], axis=0)
        Fa = np.mean([f[2] for f in fs], axis=0)
        Tn[dgt, 0:8] = g_or * Fo / np.linalg.norm(Fo)
        Tn[dgt, 8:12] = g_ink * Fi / np.linalg.norm(Fi)
        Tn[dgt, 12:16] = g_arc * Fa / max(np.linalg.norm(Fa), 1e-6)
    Tn = Tn.reshape(10, 256)
    W = Tn - Tn.mean(axis=0, keepdims=True)

    scale = 3.0
    Wf = scale * W
    bf = np.zeros(10)

    return {
        "conv1.weight": W1.astype(np.float32),
        "conv1.bias": b1.astype(np.float32),
        "conv2.weight": W2.astype(np.float32),
        "conv2.bias": b2.astype(np.float32),
        "fc.weight": Wf.astype(np.float32),
        "fc.bias": bf.astype(np.float32),
    }
