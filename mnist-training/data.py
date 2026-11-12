"""MNIST, downloaded once and checked against a fixed SHA-256.

Two splits:
  train: the last 10,000 official training images. Claude's feedback comes from these, and the Adam baselines
         train on them too, so both learn from the same images.
  test:  the official 10,000 test images. Scored at every step, never shown to Claude.
"""
import hashlib
import urllib.request
from pathlib import Path

import numpy as np

URL = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
SHA256 = "731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1"
PATH = Path(__file__).resolve().parent / "data" / "mnist.npz"


def load():
    """{"train": (x, y), "test": (x, y)}, with x of shape (N, 1, 28, 28) in [0, 1]."""
    PATH.parent.mkdir(exist_ok=True)
    if not PATH.exists():
        urllib.request.urlretrieve(URL, PATH)
    digest = hashlib.sha256(PATH.read_bytes()).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"{PATH} has SHA-256 {digest}, expected {SHA256}")
    z = np.load(PATH)
    to_float = lambda a: (a[:, None] / 255.0).astype(np.float32)
    return {
        "train": (to_float(z["x_train"][50_000:]), z["y_train"][50_000:].astype(np.int64)),
        "test": (to_float(z["x_test"]), z["y_test"].astype(np.int64)),
    }


def examples(y, per_class=5, seed=0):
    """Indices of `per_class` training images of each digit, in digit order (condition B's starting examples)."""
    rng = np.random.default_rng(seed)
    return np.concatenate([rng.choice(np.flatnonzero(y == d), per_class, replace=False) for d in range(10)])
