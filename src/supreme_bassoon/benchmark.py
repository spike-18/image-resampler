import time

import click
from skimage.transform import resize

from .io import load_image
from .methods import (
    bilinear_interpolation,
    l2_optimal_interpolation,
    nearest_neighbor,
    piecewise_linear_interpolation,
)
from .metrics import compute_mse, compute_psnr, compute_ssim


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-s", "--scale", type=int, default=2, help="Scaling factor.")
def benchmark(input1, scale) -> None:
    """Benchmark all interpolation methods on a single image.

    Downscales the image, then upscales it back and compares to the original.
    """
    original = load_image(input1)
    # Downscale the image
    down_shape = (original.shape[0] // scale, original.shape[1] // scale)
    if original.ndim == 3:
        down_shape = (down_shape[0], down_shape[1], original.shape[2])
    low_res = resize(original, down_shape, anti_aliasing=True, preserve_range=True).astype(
        original.dtype
    )

    methods = {
        "Nearest Neighbor": nearest_neighbor,
        "Bilinear": bilinear_interpolation,
        "Piecewise Linear": piecewise_linear_interpolation,
        "L2 Optimal": l2_optimal_interpolation,
    }
    for name, func in methods.items():
        start = time.time()
        upscaled = func(low_res, scale)
        elapsed = time.time() - start
        # Ensure upscaled and original are the same shape
        if upscaled.shape != original.shape:
            upscaled = resize(
                upscaled, original.shape, anti_aliasing=True, preserve_range=True
            ).astype(original.dtype)
        psnr = compute_psnr(original, upscaled)
        ssim = compute_ssim(original, upscaled)
        mse = compute_mse(original, upscaled)
        click.echo(f"{name}: time={elapsed:.3f}s, PSNR={psnr:.2f}, SSIM={ssim:.3f}, MSE={mse:.2f}")


if __name__ == "__main__":
    benchmark()
