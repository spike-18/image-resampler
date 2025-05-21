import numpy as np
import pytest

from supreme_bassoon import metrics


def test_compute_psnr_identical() -> None:
    arr = np.ones((10, 10), dtype=np.float32)
    assert metrics.compute_psnr(arr, arr) == float("inf")


def test_compute_psnr_different() -> None:
    arr1 = np.zeros((10, 10), dtype=np.float32)
    arr2 = np.ones((10, 10), dtype=np.float32)
    psnr = metrics.compute_psnr(arr1, arr2)
    assert psnr < 1


def test_compute_ssim_identical() -> None:
    arr = np.ones((10, 10), dtype=np.float32)
    assert metrics.compute_ssim(arr, arr) == 1.0


def test_compute_ssim_different() -> None:
    arr1 = np.zeros((10, 10), dtype=np.float32)
    arr2 = np.ones((10, 10), dtype=np.float32)
    ssim = metrics.compute_ssim(arr1, arr2)
    assert 0 <= ssim < 0.2


def test_compute_mse_identical() -> None:
    arr = np.ones((10, 10), dtype=np.float32)
    assert metrics.compute_mse(arr, arr) == 0.0


def test_compute_mse_different() -> None:
    arr1 = np.zeros((10, 10), dtype=np.float32)
    arr2 = np.ones((10, 10), dtype=np.float32)
    mse = metrics.compute_mse(arr1, arr2)
    assert mse == 1.0


def test_shape_mismatch() -> None:
    arr1 = np.zeros((10, 10), dtype=np.float32)
    arr2 = np.zeros((8, 8), dtype=np.float32)
    with pytest.raises(ValueError, match="shape mismatch"):
        metrics.compute_psnr(arr1, arr2)
    with pytest.raises(ValueError, match="shape mismatch"):
        metrics.compute_ssim(arr1, arr2)
    with pytest.raises(ValueError, match="shape mismatch"):
        metrics.compute_mse(arr1, arr2)
