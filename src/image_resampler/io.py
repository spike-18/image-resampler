from typing import IO

import numpy as np
from PIL import Image


def load_image(file: str | IO | bytes) -> np.ndarray:
    """
    Load an image from a file path or file-like object and return as a numpy array.
    """
    img = Image.open(file)
    return np.array(img)


def save_image(image: np.ndarray, path: str) -> None:
    """
    Save a numpy array as an image to the specified path.
    """
    img = Image.fromarray(image)
    img.save(path)
