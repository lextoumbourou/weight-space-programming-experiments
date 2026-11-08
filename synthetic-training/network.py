"""The fixed network for the synthetic dataset: a two-layer MLP, run in MLX but described in PyTorch terms."""
import mlx.core as mx
import numpy as np

import data

CLASSES = ["class 0", "class 1"]
N_IN = len(data.DESIGN)

PYTORCH_DEFINITION = f"""\
    model = nn.Sequential(
        nn.Linear({N_IN}, 16),   # fc1: {N_IN} features -> 16 hidden units
        nn.ReLU(),
        nn.Linear(16, 2),    # fc2: 16 -> 2 class logits (class 0, class 1)
    )"""
ANONYMOUS_CLASSES, ANONYMOUS_DEFINITION = CLASSES, PYTORCH_DEFINITION

SHAPES = {
    "fc1.weight": (16, N_IN),
    "fc1.bias": (16,),
    "fc2.weight": (2, 16),
    "fc2.bias": (2,),
}
N_PARAMS = sum(int(np.prod(s)) for s in SHAPES.values())
FAN_IN = {"fc1": N_IN, "fc2": 16}


def forward(params, x):
    h = mx.maximum(x @ params["fc1.weight"].T + params["fc1.bias"], 0)
    return h @ params["fc2.weight"].T + params["fc2.bias"]


def cross_entropy(logits, y):
    return (mx.logsumexp(logits, axis=1) - mx.take_along_axis(logits, y[:, None], axis=1)[:, 0]).mean()


def to_mx(weights):
    return {k: mx.array(np.asarray(weights[k], dtype=np.float32)) for k in SHAPES}


def evaluate(weights, x, y):
    """Mean cross-entropy loss, accuracy and 2x2 confusion matrix (rows true, columns predicted)."""
    logits = forward(to_mx(weights), mx.array(x))
    loss = float(cross_entropy(logits, mx.array(y)))
    pred = np.array(logits.argmax(axis=1))
    confusion = np.zeros((2, 2), dtype=int)
    np.add.at(confusion, (y, pred), 1)
    return dict(loss=loss, accuracy=float((pred == y).mean()), confusion=confusion.tolist())


def pytorch_init(seed):
    """PyTorch's default initialisation: uniform in +-1/sqrt(fan_in) for weights and biases."""
    rng = np.random.default_rng(seed)
    return {k: rng.uniform(-1, 1, s).astype(np.float32) / np.sqrt(FAN_IN[k.split(".")[0]]) for k, s in SHAPES.items()}


def numpy_reference(weights, x):
    h = np.maximum(x @ weights["fc1.weight"].T + weights["fc1.bias"], 0)
    return h @ weights["fc2.weight"].T + weights["fc2.bias"]
