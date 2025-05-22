import numpy as np
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity

def compute_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    data_range = img1.max() - img1.min()
    if data_range == 0:
        return float("inf") if np.allclose(img1, img2) else float("nan")
    return peak_signal_noise_ratio(img1, img2, data_range=data_range)

def compute_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    data_range = img1.max() - img1.min()
    if data_range == 0:
        return 1.0 if np.allclose(img1, img2) else float("nan")
    channel_axis = -1 if img1.ndim == 3 else None
    min_side = min(img1.shape[0], img1.shape[1])
    win_size = 7 if min_side >= 7 else min_side if min_side % 2 == 1 else min_side - 1
    return structural_similarity(
        img1, img2, data_range=data_range, channel_axis=channel_axis, win_size=win_size
    )

def compute_mse(img1: np.ndarray, img2: np.ndarray) -> float:
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    return mean_squared_error(img1, img2)