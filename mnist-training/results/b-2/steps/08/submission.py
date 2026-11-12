import numpy as np
import math

def build_weights():
    # ================= conv1: 4 orientations x 2 polarities of edge detectors =================
    # ch0: horizontal edge, ink ABOVE   ch1: horizontal edge, ink BELOW
    # ch2/3: "/" edges                  ch4: vertical edge, ink LEFT
    # ch5: vertical edge, ink RIGHT     ch6/7: "\" edges
    thetas = [0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4]
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_b = np.zeros(8, dtype=np.float32)

    def edge_kernel(theta):
        K = np.zeros((5, 5))
        ct, st = math.cos(theta), math.sin(theta)
        for r in range(5):
            for c in range(5):
                u = c - 2
                v = -(r - 2)
                a = u * ct + v * st
                n = -u * st + v * ct
                K[r, c] = n * math.exp(-a * a / (2 * 1.5 ** 2) - n * n / (2 * 1.0 ** 2))
        K /= K[K > 0].sum()
        return K

    for k, th in enumerate(thetas):
        K = edge_kernel(th)
        conv1_w[2 * k, 0] = K
        conv1_w[2 * k + 1, 0] = -K
        conv1_b[2 * k] = -0.25
        conv1_b[2 * k + 1] = -0.25

    INK_ABOVE, INK_BELOW, INK_LEFT, INK_RIGHT = 0, 1, 4, 5
    DIAG = [2, 3, 6, 7]
    HORZ = [INK_ABOVE, INK_BELOW]
    VERT = [INK_LEFT, INK_RIGHT]

    # ================= conv2 =================
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    conv2_b = np.zeros(16, dtype=np.float32)
    # ch0..3: orientation energy (horizontal, "/", vertical, "\")
    for o in range(4):
        for p in range(2):
            conv2_w[o, 2 * o + p, 1:4, 1:4] = 0.15

    w = 0.2
    def wall(c, side, wt):
        if side == 'L':
            conv2_w[c, INK_LEFT, 1:4, 0:2] += wt
        elif side == 'R':
            conv2_w[c, INK_RIGHT, 1:4, 3:5] += wt
        elif side == 'T':
            conv2_w[c, INK_ABOVE, 0:2, 1:4] += wt
        elif side == 'B':
            conv2_w[c, INK_BELOW, 3:5, 1:4] += wt

    def empty_centre(c, pen=0.4):
        conv2_w[c, :, 2, 2] -= pen

    # ch4: closed hole
    for s in 'LRTB':
        wall(4, s, w)
    empty_centre(4)
    conv2_b[4] = -0.8
    # ch5..8: bays
    bays = {5: ('LRB', 'T'), 6: ('LRT', 'B'), 7: ('TRB', 'L'), 8: ('TLB', 'R')}
    for c, (walls_on, open_side) in bays.items():
        for s in walls_on:
            wall(c, s, w)
        wall(c, open_side, -2 * w)
        empty_centre(c)
        conv2_b[c] = -0.5
    # ch9: tall side walls, empty middle
    conv2_w[9, INK_LEFT, 0:5, 0:2] += 0.15
    conv2_w[9, INK_RIGHT, 0:5, 3:5] += 0.15
    empty_centre(9)
    conv2_b[9] = -0.7

    # ch10..13: stroke END detectors (tip pointing up / down / left / right)
    cap = np.zeros((5, 5)); cap[1:3, 1:4] = 0.3          # cap edge (ink below, bg above)
    cont = np.zeros((5, 5)); cont[3:5, 1:4] = 0.1        # stroke continuing downward
    nobot = np.zeros((5, 5)); nobot[1:4, 1:4] = -0.3     # no bottom boundary of a bar
    empty = np.zeros((5, 5)); empty[0, :] = -0.15        # nothing above the tip
    tips = [
        (10, 0, INK_BELOW, INK_ABOVE, VERT + DIAG),   # up
        (11, 2, INK_ABOVE, INK_BELOW, VERT + DIAG),   # down
        (12, 1, INK_RIGHT, INK_LEFT, HORZ + DIAG),    # left
        (13, 3, INK_LEFT, INK_RIGHT, HORZ + DIAG),    # right
    ]
    for (c, k, capch, oppch, contchs) in tips:
        conv2_w[c, capch] += np.rot90(cap, k)
        conv2_w[c, oppch] += np.rot90(nobot, k)
        for ch in contchs:
            conv2_w[c, ch] += np.rot90(cont, k)
        for ch in range(8):
            conv2_w[c, ch] += np.rot90(empty, k)
        conv2_b[c] = -0.8      # stricter than step 7
    # ch14, ch15 unused

    # ================= fc =================
    cell_c = np.array([7.5 + 4 * m for m in range(4)])

    def ellipse(cx, cy, rx, ry, n=40):
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    S2 = [0.0, 0.3]
    protos = {
        0: [(1.0, [ellipse(14, 14, 6.0, 9.0)], S2)],
        1: [(1.0, [[(14, 4), (14, 24)]], [0.0, 0.3, 0.6])],
        2: [(0.6, [[(8, 8), (10, 5), (14, 4), (18, 5), (19, 9), (17, 13), (13, 17),
                    (9, 21), (8, 23), (13, 22.5), (21, 23)]], S2),
            (0.4, [[(8, 8), (11, 4.5), (16, 4), (19, 7), (18, 11), (14, 16), (10, 20),
                    (8, 23), (11, 24), (13, 21.5), (11, 20), (9, 22), (14, 23.5), (21, 23)]], S2)],
        3: [(1.0, [[(8, 6), (12, 4), (17, 4), (19, 7), (18, 11), (13, 13)],
                   [(13, 13), (18, 14), (20, 18), (18, 22), (13, 24), (8, 22)]], S2)],
        4: [(0.5, [[(14, 4), (8, 15), (20, 15)], [(17, 7), (17, 24)]], S2),
            (0.5, [[(8, 5), (8, 15), (20, 15)], [(18, 4), (18, 24)]], S2)],
        5: [(1.0, [[(19, 4), (10, 4), (9, 12)],
                   [(9, 12), (14, 11), (18, 13), (20, 17), (18, 22), (13, 23), (8, 21)]], S2)],
        6: [(0.5, [[(17, 4), (12, 8), (9, 14), (9, 19), (12, 23), (16, 23), (19, 20),
                    (18, 15), (14, 13), (10, 16)]], S2),
            (0.5, [[(16, 4), (11, 12), (9, 18), (11, 23), (15, 23), (18, 20), (17, 16),
                    (13, 15), (10, 18)]], S2)],
        7: [(0.5, [[(7, 5), (20, 5), (17, 11), (14, 17), (13, 24)]], S2),
            (0.5, [[(7, 5), (19, 5), (18, 10), (16.5, 24)]], S2)],
        8: [(1.0, [[(18, 6), (15, 4), (12, 5), (11, 8), (13, 11), (16, 14), (18, 18),
                    (17, 22), (13.5, 24), (10, 22), (9.5, 18), (12, 15), (16, 11),
                    (18.5, 8), (18, 6)]], S2)],
        9: [(1.0, [ellipse(14, 9, 4.5, 4.0), [(18.5, 9), (17, 24)]], S2)],
    }
    sig = 2.5

    def add_polys(T, polys, wgt, s):
        for poly in polys:
            pts = [(x + s * (14 - y), y) for (x, y) in poly]
            for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                phi = math.atan2(-dy, dx) % math.pi
                ow = np.array([max(0.0, math.cos(2 * (phi - th))) ** 2 for th in thetas])
                ns = max(1, int(L / 0.5))
                for i in range(ns):
                    t = (i + 0.5) / ns
                    x = x0 + t * dx
                    y = y0 + t * dy
                    sy = np.exp(-(y - cell_c) ** 2 / (2 * sig ** 2))
                    sx = np.exp(-(x - cell_c) ** 2 / (2 * sig ** 2))
                    T += wgt * ow[:, None, None] * sy[None, :, None] * sx[None, None, :] * (L / ns)

    temps = np.zeros((10, 4, 4, 4))
    for d in range(10):
        T = np.zeros((4, 4, 4))
        for wgt, polys, shs in protos[d]:
            for s in shs:
                add_polys(T, polys, wgt / len(shs), s)
        temps[d] = T / np.linalg.norm(T)
    temps -= temps.mean(axis=0, keepdims=True)
    for d in range(10):
        temps[d] -= temps[d].mean()
        temps[d] /= np.linalg.norm(temps[d])

    alpha = 8.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        fc_w[d, :64] = alpha * temps[d].reshape(-1)

    # ---- structural templates: (conv2 channel, x, y, weight) ----
    # 4=hole 5=U 6=n 7=open-left 8=open-right 9=side walls
    # 10=tip up 11=tip down 12=tip left 13=tip right
    struct = {
        0: [(6, 14, 9, 1.0), (5, 14, 19, 1.0), (9, 14, 14, 1.0), (4, 14, 14, 0.6)],
        1: [(10, 15, 4.5, 1.0), (11, 13, 23.5, 1.0)],
        2: [(6, 12, 10, 0.5), (7, 12, 11, 0.5), (5, 18, 19, 0.5),
            (11, 8, 8, 0.5), (12, 8, 8, 0.5), (13, 21, 23, 1.0)],
        3: [(7, 13, 8.5, 1.0), (7, 13, 18.5, 1.0), (12, 8, 6, 0.7), (12, 8, 22, 0.7)],
        4: [(5, 13, 10, 1.0), (9, 13, 10, 0.7), (4, 13, 11, 0.5),
            (10, 10, 5, 0.5), (10, 18, 5, 0.5), (11, 17.5, 23.5, 1.0), (13, 21, 15, 0.5)],
        5: [(8, 13, 8, 0.8), (7, 13, 18, 1.0), (13, 19.5, 4, 1.0), (12, 8, 21, 0.7)],
        6: [(4, 14, 18.5, 1.0), (10, 17, 4, 0.7), (13, 17, 4, 0.3)],
        7: [(6, 12, 11, 0.4), (7, 12, 11, 0.4), (12, 7, 5, 1.0), (11, 14, 23.5, 1.0)],
        8: [(4, 15, 8.5, 1.0), (4, 13.5, 18.5, 1.0)],
        9: [(4, 14, 9, 1.0), (6, 12, 18, 0.4), (7, 12, 18, 0.4), (11, 17, 23.5, 1.0)],
    }
    S = np.zeros((10, 16, 4, 4))
    for d in range(10):
        for (c, x, y, wt) in struct[d]:
            sy = np.exp(-(y - cell_c) ** 2 / (2 * sig ** 2))
            sx = np.exp(-(x - cell_c) ** 2 / (2 * sig ** 2))
            S[d, c] += wt * sy[:, None] * sx[None, :]
    S[:, 4:14] -= S[:, 4:14].mean(axis=0, keepdims=True)
    beta = 11.0    # holes / bays / walls (channels 4..9)
    gamma = 3.0    # stroke tips (channels 10..13), much weaker than in step 7
    for d in range(10):
        for c in range(4, 10):
            fc_w[d, c * 16:(c + 1) * 16] = beta * S[d, c].reshape(-1)
        for c in range(10, 14):
            fc_w[d, c * 16:(c + 1) * 16] = gamma * S[d, c].reshape(-1)

    fc_b = np.array([-0.2, -0.5, 0.0, -0.3, 0.3, 0.0, 0.0, 0.0, 1.5, -0.4], dtype=np.float32)

    return {
        "conv1.weight": conv1_w.astype(np.float32),
        "conv1.bias": conv1_b.astype(np.float32),
        "conv2.weight": conv2_w.astype(np.float32),
        "conv2.bias": conv2_b.astype(np.float32),
        "fc.weight": fc_w.astype(np.float32),
        "fc.bias": fc_b.astype(np.float32),
    }
