import click
from .__main__ import main

@click.group()
def cli():
    """Command-line interface for supreme-bassoon image upscaling app."""
    pass

cli.add_command(main, name="upscale")

if __name__ == "__main__":
    cli()
