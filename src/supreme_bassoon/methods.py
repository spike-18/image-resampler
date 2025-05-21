import numpy as np
from numpy.fft import fft2, fftshift, ifft2, ifftshift


def nearest_neighbor(
    image: np.ndarray,
    clip : bool,
    scale : float = 1.0,
    output_dtype: np.dtype | None = None,
) -> np.ndarray:
    """
    Nearest neighbor interpolation for upscaling images.

    Args:
        image (np.ndarray): Input image.
        scale (float or tuple): Scaling factor (float or (h_scale, w_scale)).
        output_dtype (np.dtype, optional): Output dtype. Defaults to input dtype.
        clip (bool): Whether to clip output to input dtype range.

    Returns:
        np.ndarray: Upscaled image.
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
        out_image = np.zeros((out_h, out_w, image.shape[2]), dtype=output_dtype)
    else:
        out_image = np.zeros((out_h, out_w), dtype=output_dtype)

    for i in range(out_h):
        src_i = min(int(np.round(i / h_scale)), in_h - 1)
        for j in range(out_w):
            src_j = min(int(np.round(j / w_scale)), in_w - 1)
            out_image[i, j] = image[src_i, src_j]

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
    Bilinear interpolation for upscaling images.

    Args:
        image (np.ndarray): Input image.
        scale (float or tuple): Scaling factor (float or (h_scale, w_scale)).

    Returns:
        np.ndarray: Upscaled image.
    """
    if isinstance(scale, (int, float)):
        h_scale = w_scale = float(scale)
    else:
        h_scale, w_scale = scale

    in_h, in_w = image.shape[:2]
    out_h, out_w = int(np.round(in_h * h_scale)), int(np.round(in_w * w_scale))

    if image.ndim == 3:
        out_image = np.zeros((out_h, out_w, image.shape[2]), dtype=image.dtype)
    else:
        out_image = np.zeros((out_h, out_w), dtype=image.dtype)

    for i in range(out_h):
        for j in range(out_w):
            x = i / h_scale
            y = j / w_scale

            x0 = int(np.floor(x))
            x1 = min(x0 + 1, in_h - 1)
            y0 = int(np.floor(y))
            y1 = min(y0 + 1, in_w - 1)

            dx = x - x0
            dy = y - y0

            if image.ndim == 3:
                top = (1 - dy) * image[x0, y0] + dy * image[x0, y1]
                bottom = (1 - dy) * image[x1, y0] + dy * image[x1, y1]
                value = (1 - dx) * top + dx * bottom
            else:
                top = (1 - dy) * image[x0, y0] + dy * image[x0, y1]
                bottom = (1 - dy) * image[x1, y0] + dy * image[x1, y1]
                value = (1 - dx) * top + dx * bottom

            out_image[i, j] = value
    return out_image


def piecewise_linear_interpolation(
    image: np.ndarray,
    scale=1.0,
) -> np.ndarray:
    """
    Piecewise linear interpolation for upscaling images.

    Args:
        image (np.ndarray): Input image.
        scale (float or tuple): Scaling factor (float or (h_scale, w_scale)).

    Returns:
        np.ndarray: Upscaled image.
    """
    if isinstance(scale, (int, float)):
        h_scale = w_scale = float(scale)
    else:
        h_scale, w_scale = scale

    in_h, in_w = image.shape[:2]
    new_h = int(np.round(in_h * h_scale))
    temp = np.zeros(
        (new_h, in_w) + (() if image.ndim == 2 else (image.shape[2],)),
        dtype=image.dtype,
    )

    row_indices = np.arange(new_h) / h_scale
    for j in range(in_w):
        if image.ndim == 2:
            col_data = image[:, j]
            temp[:, j] = np.interp(row_indices, np.arange(in_h), col_data)
        else:
            for c in range(image.shape[2]):
                col_data = image[:, j, c]
                temp[:, j, c] = np.interp(row_indices, np.arange(in_h), col_data)

    new_w = int(np.round(in_w * w_scale))
    if image.ndim == 2:
        out_image = np.zeros((new_h, new_w), dtype=image.dtype)
    else:
        out_image = np.zeros((new_h, new_w, image.shape[2]), dtype=image.dtype)

    col_indices = np.arange(new_w) / w_scale
    for i in range(new_h):
        if image.ndim == 2:
            row_data = temp[i, :]
            out_image[i, :] = np.interp(col_indices, np.arange(in_w), row_data)
        else:
            for c in range(image.shape[2]):
                row_data = temp[i, :, c]
                out_image[i, :, c] = np.interp(col_indices, np.arange(in_w), row_data)

    return out_image


def l2_optimal_interpolation(image: np.ndarray, scale: int) -> np.ndarray:
    """
    L2 optimal interpolation via Fourier zero-padding for upscaling images.

    Args:
        image (np.ndarray): Input image.
        scale (int): Integer scaling factor.

    Returns:
        np.ndarray: Upscaled image.
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
