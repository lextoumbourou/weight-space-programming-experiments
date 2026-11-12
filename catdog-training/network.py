"""The fixed cats-vs-dogs network, run in MLX but described to the model in PyTorch terms.

Weights are stored in PyTorch layout (conv: out, in, kh, kw) and flattening is PyTorch's (channel, row, column)
order, so the prompt can use the PyTorch definition below. MLX's NHWC layout is handled here.
"""
import mlx.core as mx
import numpy as np

CLASSES = ["cat", "dog"]

PYTORCH_DEFINITION = """\
    model = nn.Sequential(
        nn.Conv2d(3, 16, 5),   # conv1: 3x64x64 -> 16x60x60
        nn.ReLU(),
        nn.MaxPool2d(2),       #        16x60x60 -> 16x30x30
        nn.Conv2d(16, 32, 5),  # conv2: 16x30x30 -> 32x26x26
        nn.ReLU(),
        nn.MaxPool2d(2),       #        32x26x26 -> 32x13x13
        nn.Conv2d(32, 32, 3),  # conv3: 32x13x13 -> 32x11x11
        nn.ReLU(),
        nn.MaxPool2d(2),       #        32x11x11 -> 32x5x5 (the last row and column are dropped)
        nn.Flatten(),          #        32x5x5 -> 800, in (channel, row, column) order
        nn.Linear(800, 2),     # fc:    800 -> 2 class logits (0 = cat, 1 = dog)
    )"""

SHAPES = {
    "conv1.weight": (16, 3, 5, 5),
    "conv1.bias": (16,),
    "conv2.weight": (32, 16, 5, 5),
    "conv2.bias": (32,),
    "conv3.weight": (32, 32, 3, 3),
    "conv3.bias": (32,),
    "fc.weight": (2, 800),
    "fc.bias": (2,),
}
N_PARAMS = sum(int(np.prod(s)) for s in SHAPES.values())
FAN_IN = {"conv1": 75, "conv2": 400, "conv3": 288, "fc": 800}


def _maxpool2(x):
    """PyTorch MaxPool2d(2): floor the output size, dropping an odd last row or column."""
    n, h, w, c = x.shape
    x = x[:, : h // 2 * 2, : w // 2 * 2, :]
    return x.reshape(n, h // 2, 2, w // 2, 2, c).max(axis=(2, 4))


def _conv(h, params, name):
    return mx.conv2d(h, params[f"{name}.weight"].transpose(0, 2, 3, 1)) + params[f"{name}.bias"]


def forward(params, x):
    """params: dict of mx arrays in PyTorch layout. x: (N, 3, 64, 64) mx array. Returns (N, 2) logits."""
    h = x.transpose(0, 2, 3, 1)  # NCHW -> NHWC
    for name in ("conv1", "conv2", "conv3"):
        h = _maxpool2(mx.maximum(_conv(h, params, name), 0))
    h = h.transpose(0, 3, 1, 2).reshape(h.shape[0], -1)  # back to NCHW so flatten matches PyTorch
    return h @ params["fc.weight"].T + params["fc.bias"]


def cross_entropy(logits, y):
    return (mx.logsumexp(logits, axis=1) - mx.take_along_axis(logits, y[:, None], axis=1)[:, 0]).mean()


def to_mx(weights):
    return {k: mx.array(np.asarray(weights[k], dtype=np.float32)) for k in SHAPES}


def evaluate(weights, x, y, batch=1_000):
    """Mean cross-entropy loss, accuracy and KxK confusion matrix (rows true, columns predicted)."""
    params = to_mx(weights)
    losses, preds = [], []
    for s in range(0, len(y), batch):
        logits = forward(params, mx.array(x[s:s + batch]))
        yb = mx.array(y[s:s + batch])
        losses.append(float(cross_entropy(logits, yb)) * len(y[s:s + batch]))
        preds.append(np.array(logits.argmax(axis=1)))
    pred = np.concatenate(preds)
    k = len(CLASSES)
    confusion = np.zeros((k, k), dtype=int)
    np.add.at(confusion, (y, pred), 1)
    return dict(loss=sum(losses) / len(y), accuracy=float((pred == y).mean()), confusion=confusion.tolist())


def pytorch_init(seed):
    """PyTorch's default initialisation: uniform in +-1/sqrt(fan_in) for weights and biases."""
    rng = np.random.default_rng(seed)
    return {k: rng.uniform(-1, 1, s).astype(np.float32) / np.sqrt(FAN_IN[k.split(".")[0]]) for k, s in SHAPES.items()}


def numpy_reference(weights, x):
    """Slow, explicit PyTorch-semantics forward pass, used only to test `forward`."""
    def conv(h, w, b):
        n, c, hh, ww = h.shape
        o, _, k, _ = w.shape
        out = np.zeros((n, o, hh - k + 1, ww - k + 1), np.float32)
        for i in range(hh - k + 1):
            for j in range(ww - k + 1):
                out[:, :, i, j] = np.einsum("ncij,ocij->no", h[:, :, i:i + k, j:j + k], w) + b
        return out

    def pool(h):
        n, c, hh, ww = h.shape
        h = h[:, :, : hh // 2 * 2, : ww // 2 * 2]
        return h.reshape(n, c, hh // 2, 2, ww // 2, 2).max(axis=(3, 5))

    h = x
    for name in ("conv1", "conv2", "conv3"):
        h = pool(np.maximum(conv(h, weights[f"{name}.weight"], weights[f"{name}.bias"]), 0))
    return h.reshape(len(h), -1) @ weights["fc.weight"].T + weights["fc.bias"]
