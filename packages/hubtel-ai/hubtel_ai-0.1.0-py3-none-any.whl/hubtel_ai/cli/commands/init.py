# -*- coding: utf-8 -*-
import click
from cookiecutter.main import cookiecutter  # type: ignore
from hubtel_ai.cli.commands.main import cli, print_logo, console
from hubtel_ai.cli.utils import cli_root_path
from cookiecutter.main import cookiecutter
import os

@cli.command()
@click.argument("path", default="./integrations/demo", type=click.Path(exists=True))
def build(path: str) -> None:
    """
    Build docker image for integration in a given path
    """
    console.print(
        "⚓️ Hold on tight: We are putting your stuffs in a container right away.\n"
    )
    DOCKER_IMAGE_NAME = path.split("/")[-1]
    DOCKER_TAG = "latest"
    os.system(f"docker build -t {DOCKER_IMAGE_NAME}:{DOCKER_TAG} {path} ")
    console.print(
        "⚓️ Get up and running: You can run your container with [bold][blue]make run command...\n"
    )


@cli.command()
@click.argument("path", default="./integrations", type=click.Path(exists=True))
def init(path: str) -> None:
    """
    Scaffold a new integration in the given PATH.

    PATH: Path to the integration. If not provided, the current directory will be used.
    """
    print_logo()

    console.print(
        "🚢 Unloading cargo... Setting up your integration at the dock.", style="bold"
    )

    result = cookiecutter(
        cli_root_path + "/cookiecutter",
        output_dir=path,
    )

    name = result.split("/")[-1]

    console.print(
        "\n🌊 Ahoy, Captain! Your project is ready to set sail into the vast ocean of possibilities!",
        style="bold",
    )
    console.print("Here are your next steps:\n", style="bold")

    console.print(
        "⚓️ Dive into development: Start adding your code and resources into the newly created integration folder.\n"
        f"▶️ [bold][blue]cd integrations/{name}[/blue][/bold] and start coding! \n"
    )
    console.print(
        "⚓️ Build your integration: Run [bold][blue]sam build[/blue][/bold] to build all the serverless functions within your integration.\n"
        f"▶️ [bold][blue]sam build[/blue][/bold]\n"
    )

    console.print(" After building, you can ...\n", style="bold")

    console.print(
        "⚓️ Run your integration locally with [blue]API Gateway[/blue]: Run [bold][blue]sam local start-api[/blue] to launch API Gateway endpoints for your lambda functions.\n"
        f"▶️ [bold][blue]sam local start-api {name}[/blue][/bold] \n"
    )
    console.print(
        "⚓️ Run your integration locally with [blue] Lambda Invoke [/blue]: Run [bold][blue] sam  local invoke <FunctionLogicalId> -e <path/to/test.json>[/blue][/bold] to invoke your lambda function \n"
        f"▶️ [bold][blue]sam  local invoke <FunctionLogicalId> -e <path/to/test.json>[/blue][/bold]"
    )