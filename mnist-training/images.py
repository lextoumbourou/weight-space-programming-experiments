"""Digit grids shown to Claude in condition B: white ink on black, as the values are stored, enlarged 4x."""
import base64
import io

import numpy as np
from PIL import Image, ImageDraw

SCALE, GAP = 4, 6
CELL = 28 * SCALE


def _digit(x):
    return Image.fromarray((x[0] * 255).astype(np.uint8)).resize((CELL, CELL), Image.NEAREST)


def grid(xs, columns, row_labels=None, cell_labels=None):
    """A PIL image of digits in a grid. row_labels go on the left, cell_labels above each digit."""
    rows = int(np.ceil(len(xs) / columns))
    left = 28 if row_labels else 0
    top = 16 if cell_labels else 0
    w = left + columns * (CELL + GAP) + GAP
    h = rows * (CELL + GAP + top) + GAP
    img = Image.new("L", (w, h), 128)
    draw = ImageDraw.Draw(img)
    for i, x in enumerate(xs):
        r, c = divmod(i, columns)
        x0, y0 = left + GAP + c * (CELL + GAP), GAP + r * (CELL + GAP + top) + top
        img.paste(_digit(x), (x0, y0))
        if cell_labels:
            draw.text((x0, y0 - top + 2), cell_labels[i], fill=255)
    if row_labels:
        for r, label in enumerate(row_labels):
            draw.text((8, GAP + r * (CELL + GAP + top) + top + CELL // 2 - 6), label, fill=255)
    return img


def image_block(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                        "data": base64.b64encode(buffer.getvalue()).decode()}}
