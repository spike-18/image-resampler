import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    click.secho("Basic entry point.\nDoes nothing yet.", fg='green')
