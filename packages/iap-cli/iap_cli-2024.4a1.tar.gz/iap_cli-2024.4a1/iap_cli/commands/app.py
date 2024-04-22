"""
Main Typer app for root commands
"""

__version__ = "2024.4a1"

import typer
from rich import print

from iap_cli.commands.config.app import config_app
from iap_cli.commands.get.app import get_app
from iap_cli.commands.restart.app import restart_app

# define typer app
main_app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="CLI tool for interacting with Itential.",
)

# Add additional sub-apps below:
# Configure app
main_app.add_typer(typer_instance=config_app, name="config")
# Get operations
main_app.add_typer(typer_instance=get_app, name="get")
# Restart operations
main_app.add_typer(typer_instance=restart_app, name="restart")


@main_app.command("version")
def version():
    print(__version__)
