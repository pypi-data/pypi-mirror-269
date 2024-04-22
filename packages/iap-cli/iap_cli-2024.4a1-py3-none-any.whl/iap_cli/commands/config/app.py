import typer

from iap_cli.commands.config.add import add_cluster, add_credentials, add_server

# define typer apps
config_app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Manage configurations for the Itential CLI app.",
)
config_app_add = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Add configurations for the Itential CLI app.",
)
config_app.add_typer(typer_instance=config_app_add, name="add")


@config_app_add.command(name="credentials")
def add_credentials_command():
    """Adds a credentials file interactively"""
    add_credentials()


@config_app_add.command(name="server")
def add_server_command():
    """Adds a server to the inventory file interactively"""
    add_server()


@config_app_add.command(name="cluster")
def add_cluster_command():
    """Adds a list of servers that form a cluster to the inventory file interactively"""
    add_cluster()
