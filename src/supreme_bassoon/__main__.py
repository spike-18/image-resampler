import click
import matplotlib.pyplot as plt

from . import __version__
from .io import load_image, save_image
from .methods import (
    bilinear_interpolation,
    l2_optimal_interpolation,
    nearest_neighbor,
    piecewise_linear_interpolation,
)


@click.command()
@click.version_option(version=__version__)
@click.argument("file", type=click.File(mode="rb"))
@click.option("-m", "--method", default="nn", help="Method to use for interpolation. [nn|bl|pw|l2]")
@click.option("-s", "--scale", type=int, default=2, help="Scaling factor.")
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Print interpolation parameters."
)
@click.option(
    "--save", is_flag=True, default=False, help="Save interpolated image to examples/output/."
)
def main(
    file: click.File,
    method: str,
    scale: int,
    save: bool,
    verbose: bool,
) -> int | None:
    """Upscales an input image using the selected method.

    After that displays the result.
    Optionally saves the upscaled image to examples/output/ as <filename>_interp.png.
    """
    if verbose:
        click.secho(f"Interpolation method: {method}")
        click.secho(f"Filename: {file.name}")
        click.secho(f"Scaling factor {scale}")
        click.secho(f"Save image? {'yes' if save else 'no'}")

    image = load_image(file)
    grey_scale = image.ndim == 2

    match method:
        case "nn":
            out_image = nearest_neighbor(image, scale)
        case "bl":
            out_image = bilinear_interpolation(image, scale)
        case "pw":
            out_image = piecewise_linear_interpolation(image, scale)
        case "l2":
            out_image = l2_optimal_interpolation(image, scale)
        case _:
            click.secho(f"Incorrect '{method}' method. List of valid methods:", fg="red")
            list_methods()
            return 1

    if save:
        out_name = str(file.name).split("/")[-1].split(".")[0]
        save_image(out_image, f"examples/output/{out_name}_interp.png")
        click.secho(f"Image {out_name} has been saved to examples/output/", fg="green")

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Show original and upscaled images side by side
    if grey_scale:
        axes[0].imshow(image, cmap="gray")
        axes[1].imshow(out_image, cmap="gray")
    else:
        axes[0].imshow(image)
        axes[1].imshow(out_image)

    axes[0].set_title("Original")
    axes[0].axis("off")
    axes[1].set_title("Interpolated")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()
    return None


def list_methods() -> None:
    click.echo(
        """
    nn - nearest neighbor
    bl - bilinear
    pw - piecewise linear
    l2 - l2 optimal
"""
    )


if __name__ == "__main__":
    click.echo(
        "Use 'poetry run example' to print example or 'poetry run upscale' to upscale image.",
    )
