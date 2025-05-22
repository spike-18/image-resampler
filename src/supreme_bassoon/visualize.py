import click
import matplotlib.pyplot as plt
from skimage import data

from .methods import (
    bilinear_interpolation,
    l2_optimal_interpolation,
    nearest_neighbor,
    piecewise_linear_interpolation,
)


@click.command()
def example() -> None:
    """Runs a visual comparison of interpolation methods.

    Loads a standard test image, applies each interpolation method with a scale factor of 2,
    and displays the results side by side for visual inspection.
    Shows the pixelated (nearest neighbor) result first, then progressively less pixelated results.
    """
    click.secho("Example comparison between interpolation methods is loaded.", fg="green")

    image = data.camera()  # shape: (512, 512)
    scale = 2

    # Downscale and then upscale to make pixelation visible
    downscale_factor = 8
    small = image[::downscale_factor, ::downscale_factor]

    # Upscale using each method
    nn_image = nearest_neighbor(small, scale * downscale_factor)
    bilinear_image = bilinear_interpolation(small, scale * downscale_factor)
    piecewise_image = piecewise_linear_interpolation(small, scale * downscale_factor)
    l2_image = l2_optimal_interpolation(small, scale * downscale_factor)

    # Arrange outputs in two rows for better visibility
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()

    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(small, cmap="gray")
    axes[1].set_title(f"Downscaled ({downscale_factor}x)")
    axes[1].axis("off")

    axes[2].imshow(nn_image, cmap="gray")
    axes[2].set_title("Nearest Neighbor")
    axes[2].axis("off")

    axes[3].imshow(bilinear_image, cmap="gray")
    axes[3].set_title("Bilinear")
    axes[3].axis("off")

    axes[4].imshow(piecewise_image, cmap="gray")
    axes[4].set_title("Piecewise Linear")
    axes[4].axis("off")

    axes[5].imshow(l2_image, cmap="gray")
    axes[5].set_title("L2 Optimal (FFT)")
    axes[5].axis("off")

    for i in range(6, len(axes)):
        axes[i].axis("off")

    plt.tight_layout()
    plt.show()
