# -*- coding: utf-8 -*-

import click

from ..version import __version__
from .main import cli, console


@cli.command()
@click.option(
    "-s",
    "--short",
    "short",
    default=False,
    is_flag=True,
    required=False,
    help="Display only the short version number.",
)
def version(short: bool) -> None:
    """
    Displays the version of the Ocean package.
    """
    if short:
        console.print(__version__)
    else:
        console.print(f"🌊 Hubtel AI version: {__version__}")
