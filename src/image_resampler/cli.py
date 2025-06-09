import click

from .__main__ import main as upscale
from .benchmark import benchmark
from .gui import rungui
from .visualize import example


@click.group()
def cli() -> None:
    """image-resampler: Image Upscaling Toolkit CLI."""


cli.add_command(example, name="example")
cli.add_command(benchmark, name="benchmark")
cli.add_command(upscale, name="upscale")


@click.command()
def gui() -> None:
    """Launch the graphical user interface."""
    rungui()


cli.add_command(gui, name="gui")

if __name__ == "__main__":
    cli()
