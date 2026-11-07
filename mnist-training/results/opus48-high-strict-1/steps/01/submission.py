import numpy as np

def build_weights():
    # ---------- conv1: channel 0 = 5x5 average (ink density) ----------
    conv1_w = np.zeros((8, 1, 5, 5), dtype=np.float32)
    conv1_w[0, 0, :, :] = 1.0 / 25.0      # local ink density in [0,1]
    conv1_b = np.zeros((8,), dtype=np.float32)

    # ---------- conv2: every out-channel averages conv1 ch0 over 5x5 ----------
    conv2_w = np.zeros((16, 8, 5, 5), dtype=np.float32)
    for k in range(16):
        conv2_w[k, 0, :, :] = 1.0 / 25.0  # all 16 channels -> same 4x4 ink map
    conv2_b = np.zeros((16,), dtype=np.float32)

    # ---------- hand-drawn 4x4 expected ink maps (0..1) ----------
    E = {
        0: [[.2,.8,.8,.2],[.8,.2,.2,.8],[.8,.2,.2,.8],[.2,.8,.8,.2]],
        1: [[.1,.3,.6,.1],[.1,.3,.6,.1],[.1,.3,.6,.1],[.1,.3,.6,.1]],
        2: [[.3,.8,.8,.4],[.1,.1,.6,.5],[.2,.6,.4,.1],[.7,.8,.7,.5]],
        3: [[.4,.8,.8,.3],[.1,.2,.7,.5],[.2,.5,.7,.4],[.4,.8,.7,.2]],
        4: [[.2,.3,.7,.1],[.6,.2,.7,.1],[.7,.8,.8,.5],[.1,.1,.7,.1]],
        5: [[.7,.8,.7,.3],[.6,.3,.1,.1],[.3,.7,.7,.3],[.4,.7,.8,.4]],
        6: [[.2,.7,.7,.3],[.6,.2,.1,.1],[.7,.7,.6,.3],[.3,.7,.7,.4]],
        7: [[.5,.8,.8,.8],[.1,.1,.6,.3],[.1,.4,.5,.1],[.2,.6,.2,.1]],
        8: [[.3,.8,.8,.3],[.5,.3,.3,.5],[.5,.3,.3,.5],[.3,.8,.8,.3]],
        9: [[.3,.8,.8,.3],[.6,.3,.4,.6],[.2,.3,.7,.5],[.2,.4,.8,.3]],
    }
    E = {d: np.array(v, dtype=np.float32) for d, v in E.items()}

    # mean-centre templates across digits so common ink cancels, keep only shape
    Ebar = np.mean(np.stack([E[d] for d in range(10)]), axis=0)
    T = {d: E[d] - Ebar for d in range(10)}

    # ---------- fc: spread each 4x4 template over the 16 identical channels ----------
    scale = 12.0
    fc_w = np.zeros((10, 256), dtype=np.float32)
    for d in range(10):
        for c in range(16):
            for r in range(4):
                for col in range(4):
                    idx = c * 16 + r * 4 + col
                    fc_w[d, idx] = (scale / 16.0) * T[d][r, col]
    fc_b = np.zeros((10,), dtype=np.float32)

    return {
        "conv1.weight": conv1_w,
        "conv1.bias": conv1_b,
        "conv2.weight": conv2_w,
        "conv2.bias": conv2_b,
        "fc.weight": fc_w,
        "fc.bias": fc_b,
    }
