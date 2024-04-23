# -*- coding: utf-8 -*-
import click
from cookiecutter.main import cookiecutter  # type: ignore
from .main import cli, print_logo, console
from ..utils import cli_root_path
from hubtel_ai.cli.commands.main import cli, print_logo, console
import os


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def validate(path: str) -> None:
    """
    Build docker image for integration in a given path
    """
    console.print(
        "⚓️ Hold on tight: We are validating your integration ...\n"
    )
    response = os.system(f"sam validate {path}")
    
    console.print(
        f"⚓️ Integration Validation Result: {response}\n"
    )
