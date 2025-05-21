
from pathlib import Path

import numpy as np
from PIL import Image

from supreme_bassoon.io import load_image, save_image


def test_load_image_and_save_image(tmp_path) -> None:
    # Create a dummy image and save it
    arr = (np.random.Generator(10, 10, 3) * 255).astype(np.uint8)
    file_path = tmp_path / "test_img.png"
    Image.fromarray(arr).save(file_path)
    # Test load_image
    loaded = load_image(str(file_path))
    assert np.allclose(loaded, arr)
    # Test save_image
    out_path = tmp_path / "out_img.png"
    save_image(loaded, str(out_path))
    loaded2 = np.array(Image.open(out_path))
    assert np.allclose(loaded2, arr)


def test_load_image_filelike(tmp_path) -> None:
    arr = (np.random.Generator(8, 8) * 255).astype(np.uint8)
    file_path = tmp_path / "test_img2.png"
    Image.fromarray(arr).save(file_path)
    with Path.open(file_path, "rb") as f:
        loaded = load_image(f)
        assert np.allclose(loaded, arr)
