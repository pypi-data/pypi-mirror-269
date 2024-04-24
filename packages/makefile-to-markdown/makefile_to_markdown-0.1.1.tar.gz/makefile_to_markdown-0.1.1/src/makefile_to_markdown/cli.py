import logging
from pathlib import Path

import click

from .core import makefile_2_markdown

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def silent_echo(*args, **kwargs):
    pass


def common_options(func):
    """Decorator to add common options to a command."""
    func = click.option(
        "-p",
        "--path",
        required=True,
        type=click.Path(),
        help="Path to the makefile file.",
    )(func)
    func = click.option(
        "-o",
        "--output",
        required=False,
        type=click.Path(),
        help="Path to the output markdown file.",
    )(func)
    return click.option("--verbose", is_flag=True, help="Enables verbose mode.")(func)


@click.command()
@common_options
def convert(path, output, verbose):
    """Main entry point."""
    if not verbose:
        click.echo = silent_echo

    path = Path(path).expanduser()
    output = Path(output).expanduser() if output else None

    output = makefile_2_markdown(path, output)
    click.secho("Makefile converted to Markdown", fg="green")
    click.secho(f"{output}", dim=True)


# Set up your command-line interface grouping
@click.group()
@click.version_option()
def cli():
    """Simple command-line utility that convertys Makefiles to Markdown if
    specific commenting style is followed."""


cli.add_command(convert)

if __name__ == "__main__":
    cli()
