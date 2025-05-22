import numpy as np
from numpy.fft import fft2, fftshift, ifft2, ifftshift


def nearest_neighbor(
    image: np.ndarray,
    clip: bool,
    scale: float = 1.0,
    output_dtype: np.dtype | None = None,
) -> np.ndarray:
    """
    Nearest neighbor interpolation for upscaling images.
    """
    if isinstance(scale, (int, float)):
        h_scale = w_scale = float(scale)
    else:
        h_scale, w_scale = scale
    in_h, in_w = image.shape[:2]
    out_h, out_w = int(np.round(in_h * h_scale)), int(np.round(in_w * w_scale))
    if output_dtype is None:
        output_dtype = image.dtype
    if image.ndim == 3:
        out_image = np.empty((out_h, out_w, image.shape[2]), dtype=output_dtype)
    else:
        out_image = np.empty((out_h, out_w), dtype=output_dtype)
    # Vectorized index calculation
    row_idx = np.clip(np.round(np.arange(out_h) / h_scale).astype(int), 0, in_h - 1)
    col_idx = np.clip(np.round(np.arange(out_w) / w_scale).astype(int), 0, in_w - 1)
    if image.ndim == 3:
        for c in range(image.shape[2]):
            out_image[..., c] = image[row_idx[:, None], col_idx, c]
    else:
        out_image[:, :] = image[row_idx[:, None], col_idx]
    if clip:
        info = (
            np.iinfo(image.dtype)
            if np.issubdtype(image.dtype, np.integer)
            else np.finfo(image.dtype)
        )
        out_image = np.clip(out_image, info.min, info.max)
    return out_image


def bilinear_interpolation(image: np.ndarray, scale=1.0) -> np.ndarray:
    """
    Bilinear interpolation for upscaling images (vectorized).
    """
    if isinstance(scale, (int, float)):
        h_scale = w_scale = float(scale)
    else:
        h_scale, w_scale = scale
    in_h, in_w = image.shape[:2]
    out_h, out_w = int(np.round(in_h * h_scale)), int(np.round(in_w * w_scale))
    # Generate grid of coordinates in output image
    x = np.arange(out_h) / h_scale
    y = np.arange(out_w) / w_scale
    x0 = np.floor(x).astype(int)
    x1 = np.clip(x0 + 1, 0, in_h - 1)
    y0 = np.floor(y).astype(int)
    y1 = np.clip(y0 + 1, 0, in_w - 1)
    dx = x - x0
    dy = y - y0
    if image.ndim == 3:
        out_image = np.empty((out_h, out_w, image.shape[2]), dtype=image.dtype)
        for c in range(image.shape[2]):
            for i in range(out_h):
                for j in range(out_w):
                    top = (1 - dy[j]) * image[x0[i], y0[j], c] + dy[j] * image[x0[i], y1[j], c]
                    bottom = (1 - dy[j]) * image[x1[i], y0[j], c] + dy[j] * image[x1[i], y1[j], c]
                    out_image[i, j, c] = (1 - dx[i]) * top + dx[i] * bottom
    else:
        out_image = np.empty((out_h, out_w), dtype=image.dtype)
        for i in range(out_h):
            for j in range(out_w):
                top = (1 - dy[j]) * image[x0[i], y0[j]] + dy[j] * image[x0[i], y1[j]]
                bottom = (1 - dy[j]) * image[x1[i], y0[j]] + dy[j] * image[x1[i], y1[j]]
                out_image[i, j] = (1 - dx[i]) * top + dx[i] * bottom
    return out_image


def piecewise_linear_interpolation(
    image: np.ndarray,
    scale=1.0,
) -> np.ndarray:
    """
    Piecewise linear interpolation for upscaling images (vectorized).
    """
    if isinstance(scale, (int, float)):
        h_scale = w_scale = float(scale)
    else:
        h_scale, w_scale = scale
    in_h, in_w = image.shape[:2]
    new_h = int(np.round(in_h * h_scale))
    row_indices = np.arange(new_h) / h_scale
    if image.ndim == 2:
        temp = np.empty((new_h, in_w), dtype=image.dtype)
        for j in range(in_w):
            temp[:, j] = np.interp(row_indices, np.arange(in_h), image[:, j])
    else:
        temp = np.empty((new_h, in_w, image.shape[2]), dtype=image.dtype)
        for j in range(in_w):
            for c in range(image.shape[2]):
                temp[:, j, c] = np.interp(row_indices, np.arange(in_h), image[:, j, c])
    new_w = int(np.round(in_w * w_scale))
    col_indices = np.arange(new_w) / w_scale
    if image.ndim == 2:
        out_image = np.empty((new_h, new_w), dtype=image.dtype)
        for i in range(new_h):
            out_image[i, :] = np.interp(col_indices, np.arange(in_w), temp[i, :])
    else:
        out_image = np.empty((new_h, new_w, image.shape[2]), dtype=image.dtype)
        for i in range(new_h):
            for c in range(image.shape[2]):
                out_image[i, :, c] = np.interp(col_indices, np.arange(in_w), temp[i, :, c])
    return out_image


def l2_optimal_interpolation(image: np.ndarray, scale: int) -> np.ndarray:
    """
    L2 optimal interpolation via Fourier zero-padding for upscaling images.
    """
    if not float(scale).is_integer():
        msg = "L2 optimal interpolation via Fourier zero-padding requires an integer scale factor."
        raise ValueError(msg)
    scale = int(scale)

    def fourier_upscale(channel: np.ndarray) -> np.ndarray:
        h, w = channel.shape
        f = fftshift(fft2(channel))
        new_h, new_w = h * scale, w * scale
        f_up = np.zeros((new_h, new_w), dtype=complex)
        h_center, w_center = new_h // 2, new_w // 2
        h_half, w_half = h // 2, w // 2
        f_up[
            h_center - h_half : h_center - h_half + h,
            w_center - w_half : w_center - w_half + w,
        ] = f
        upscaled = np.real(ifft2(ifftshift(f_up)))
        return upscaled * (scale**2)

    if image.ndim == 2:
        return fourier_upscale(image)
    channels = [fourier_upscale(image[..., c]) for c in range(image.shape[2])]
    return np.stack(channels, axis=-1)
