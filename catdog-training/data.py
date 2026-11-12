"""Kaggle Dogs vs. Cats (2013), resized to 64x64 RGB.

Source: train.zip from https://www.kaggle.com/c/dogs-vs-cats (25,000 labelled photos, 12,500 per class),
downloaded with the Kaggle CLI: `kaggle competitions download dogs-vs-cats -f train.zip -p data/download`.
Each photo is resized so its shorter side is 64 pixels (bilinear), then centre-cropped to 64x64.

Splits, balanced per class, from a fixed random permutation:
  train: 10,000 images (5,000 per class), gradient-descent baselines only
  val:   10,000 images (5,000 per class), the feedback the LLM sees (its training set in practice)
  test:   5,000 images (2,500 per class), never shown to the LLM
"""
import hashlib
import io
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent / "data"
ZIP = HERE / "download" / "train.zip"
ZIP_SHA256 = "736cdebc25d34b39b29947fc2fa94703483488e0b20db6f594388e28f1dc450b"
CACHE = HERE / "catdog64.npz"
SIZE = 64


def _prepare():
    from PIL import Image
    digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
    if digest != ZIP_SHA256:
        raise RuntimeError(f"{ZIP} has SHA-256 {digest}, expected {ZIP_SHA256}")
    images, labels = [], []
    with zipfile.ZipFile(ZIP) as z:
        names = sorted(n for n in z.namelist() if n.endswith(".jpg"))
        for name in names:
            label = 0 if Path(name).name.startswith("cat.") else 1
            with Image.open(io.BytesIO(z.read(name))) as im:
                im = im.convert("RGB")
                w, h = im.size
                scale = SIZE / min(w, h)
                im = im.resize((max(SIZE, round(w * scale)), max(SIZE, round(h * scale))), Image.BILINEAR)
                w, h = im.size
                left, top = (w - SIZE) // 2, (h - SIZE) // 2
                images.append(np.asarray(im.crop((left, top, left + SIZE, top + SIZE)), dtype=np.uint8))
            labels.append(label)
    np.savez(CACHE, x=np.stack(images), y=np.array(labels, dtype=np.int64), names=np.array(names))


def load():
    """Return {"train": (x, y), "val": (x, y), "test": (x, y)}, x of shape (N, 3, 64, 64) in [0, 1]."""
    if not CACHE.exists():
        _prepare()
    z = np.load(CACHE)
    x, y = z["x"], z["y"]
    rng = np.random.default_rng(2013)
    split = {"train": [], "val": [], "test": []}
    for c in (0, 1):
        idx = rng.permutation(np.flatnonzero(y == c))
        split["train"] += list(idx[:5000]); split["val"] += list(idx[5000:10000]); split["test"] += list(idx[10000:12500])
    out = {}
    for k, idx in split.items():
        idx = np.array(sorted(idx))
        out[k] = ((x[idx].transpose(0, 3, 1, 2) / 255.0).astype(np.float32), y[idx])
    return out


SHA256 = ZIP_SHA256
