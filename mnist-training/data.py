"""MNIST, downloaded once and checked against a fixed SHA-256.

Splits:
  train: the first 50,000 official training images (gradient-descent baselines only)
  val:   the last 10,000 official training images (the feedback the LLM sees)
  test:  the official 10,000 test images (never shown to the LLM)
"""
import hashlib
import urllib.request
from pathlib import Path

import numpy as np

URL = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
SHA256 = "731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1"
PATH = Path(__file__).resolve().parent / "data" / "mnist.npz"


def _download():
    PATH.parent.mkdir(exist_ok=True)
    if not PATH.exists():
        urllib.request.urlretrieve(URL, PATH)
    digest = hashlib.sha256(PATH.read_bytes()).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"{PATH} has SHA-256 {digest}, expected {SHA256}")


def load():
    """Return {"train": (x, y), "val": (x, y), "test": (x, y)} with x of shape (N, 1, 28, 28) in [0, 1]."""
    _download()
    z = np.load(PATH)
    to_float = lambda a: (a[:, None] / 255.0).astype(np.float32)
    x_train, y_train = to_float(z["x_train"]), z["y_train"].astype(np.int64)
    return {
        "train": (x_train[:50_000], y_train[:50_000]),
        "val": (x_train[50_000:], y_train[50_000:]),
        "test": (to_float(z["x_test"]), z["y_test"].astype(np.int64)),
    }
