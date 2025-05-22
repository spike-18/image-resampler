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
    """
    click.secho("Example comparison between interpolation methods is loaded.", fg="green")

    image = data.camera()  # shape: (512, 512)

    scale = 2

    nn_image = nearest_neighbor(image, scale)
    bilinear_image = bilinear_interpolation(image, scale)
    piecewise_image = piecewise_linear_interpolation(image, scale)
    l2_image = l2_optimal_interpolation(image, scale)

    fig, axes = plt.subplots(1, 5, figsize=(20, 5))

    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(nn_image, cmap="gray")
    axes[1].set_title("Nearest Neighbor")
    axes[1].axis("off")

    axes[2].imshow(bilinear_image, cmap="gray")
    axes[2].set_title("Bilinear")
    axes[2].axis("off")

    axes[3].imshow(piecewise_image, cmap="gray")
    axes[3].set_title("Piecewise Linear")
    axes[3].axis("off")

    axes[4].imshow(l2_image, cmap="gray")
    axes[4].set_title("L2 Optimal (FFT)")
    axes[4].axis("off")

    plt.tight_layout()
    plt.show()
