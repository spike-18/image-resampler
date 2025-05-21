import numpy as np
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity


def compute_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compute Peak Signal-to-Noise Ratio between two images."""
    return peak_signal_noise_ratio(img1, img2, data_range=img1.max() - img1.min())


def compute_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compute Structural Similarity Index between two images."""
    # Set channel_axis for color images and adjust win_size if needed
    channel_axis = -1 if img1.ndim == 3 else None
    min_side = min(img1.shape[0], img1.shape[1])
    win_size = 7 if min_side >= 7 else min_side if min_side % 2 == 1 else min_side - 1
    return structural_similarity(
        img1, img2, data_range=img1.max() - img1.min(), channel_axis=channel_axis, win_size=win_size
    )


def compute_mse(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compute Mean Squared Error between two images."""
    return mean_squared_error(img1, img2)
