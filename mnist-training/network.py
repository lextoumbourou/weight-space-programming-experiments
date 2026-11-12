"""The fixed MNIST network, run in MLX but described to Claude in PyTorch terms.

Weights are stored in PyTorch layout (conv: out, in, kh, kw) and flattening is PyTorch's (channel, row, column)
order, so the prompt can use the PyTorch definition below. MLX's NHWC layout is handled here.
"""
import mlx.core as mx
import numpy as np

PYTORCH_DEFINITION = """\
    model = nn.Sequential(
        nn.Conv2d(1, 8, 5),    # conv1: 1x28x28 -> 8x24x24
        nn.ReLU(),
        nn.MaxPool2d(2),       #        8x24x24 -> 8x12x12
        nn.Conv2d(8, 16, 5),   # conv2: 8x12x12 -> 16x8x8
        nn.ReLU(),
        nn.MaxPool2d(2),       #        16x8x8 -> 16x4x4
        nn.Flatten(),          #        16x4x4 -> 256, in (channel, row, column) order
        nn.Linear(256, 10),    # fc:    256 -> 10 class logits
    )"""

SHAPES = {
    "conv1.weight": (8, 1, 5, 5),
    "conv1.bias": (8,),
    "conv2.weight": (16, 8, 5, 5),
    "conv2.bias": (16,),
    "fc.weight": (10, 256),
    "fc.bias": (10,),
}
N_PARAMS = sum(int(np.prod(s)) for s in SHAPES.values())
FAN_IN = {"conv1": 25, "conv2": 200, "fc": 256}


def _maxpool2(x):
    n, h, w, c = x.shape
    return x.reshape(n, h // 2, 2, w // 2, 2, c).max(axis=(2, 4))


def forward(params, x):
    """params: dict of mx arrays in PyTorch layout. x: (N, 1, 28, 28) mx array. Returns (N, 10) logits."""
    h = x.transpose(0, 2, 3, 1)  # NCHW -> NHWC
    h = mx.conv2d(h, params["conv1.weight"].transpose(0, 2, 3, 1)) + params["conv1.bias"]
    h = _maxpool2(mx.maximum(h, 0))
    h = mx.conv2d(h, params["conv2.weight"].transpose(0, 2, 3, 1)) + params["conv2.bias"]
    h = _maxpool2(mx.maximum(h, 0))
    h = h.transpose(0, 3, 1, 2).reshape(h.shape[0], -1)  # back to NCHW so flatten matches PyTorch
    return h @ params["fc.weight"].T + params["fc.bias"]


def cross_entropy(logits, y):
    return (mx.logsumexp(logits, axis=1) - mx.take_along_axis(logits, y[:, None], axis=1)[:, 0]).mean()


def to_mx(weights):
    return {k: mx.array(np.asarray(weights[k], dtype=np.float32)) for k in SHAPES}


def logits(weights, x, batch=2_000):
    params = to_mx(weights)
    return np.concatenate([np.array(forward(params, mx.array(x[s:s + batch]))) for s in range(0, len(x), batch)])


def evaluate(weights, x, y):
    """Mean cross-entropy loss, accuracy, 10x10 confusion matrix (rows true, columns predicted), and the
    per-image predictions and probabilities (used to show condition B its mistakes)."""
    z = logits(weights, x).astype(np.float64)
    z -= z.max(axis=1, keepdims=True)
    log_p = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    pred = log_p.argmax(axis=1)
    confusion = np.zeros((10, 10), dtype=int)
    np.add.at(confusion, (y, pred), 1)
    return dict(loss=float(-log_p[np.arange(len(y)), y].mean()), accuracy=float((pred == y).mean()),
                confusion=confusion.tolist(), pred=pred, prob=np.exp(log_p))


def pytorch_init(seed):
    """PyTorch's default initialisation: uniform in +-1/sqrt(fan_in) for weights and biases."""
    rng = np.random.default_rng(seed)
    return {k: rng.uniform(-1, 1, s).astype(np.float32) / np.sqrt(FAN_IN[k.split(".")[0]]) for k, s in SHAPES.items()}


def numpy_reference(weights, x):
    """Slow, explicit PyTorch-semantics forward pass, used only to check `forward`."""
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
        return h.reshape(n, c, hh // 2, 2, ww // 2, 2).max(axis=(3, 5))

    h = pool(np.maximum(conv(x, weights["conv1.weight"], weights["conv1.bias"]), 0))
    h = pool(np.maximum(conv(h, weights["conv2.weight"], weights["conv2.bias"]), 0))
    return h.reshape(len(h), -1) @ weights["fc.weight"].T + weights["fc.bias"]
