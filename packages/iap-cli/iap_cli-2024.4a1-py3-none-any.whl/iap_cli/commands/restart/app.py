import typer
from rich import print

from iap_cli.enums import Applications
from iap_cli.utils import (
    complete_application_name,
    complete_server_name,
    get_client,
    get_servers_from_inventory,
    runner,
)

# define typer app
restart_app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Restart resources in your IAP server.",
)


def restart_adapter(host: str, adapter: str) -> list[dict]:
    """
    Start (if adapter is stopped) or restart an adapter in IAP.

    :param host: Server hostname/FQDN.
    :param adapter: Name of adapter to be restarted (case-sensitive).
    """
    api = get_client(host)
    try:
        adapter_health = api.core.get_adapter_health(adapter)
        if "STOPPED" in adapter_health["state"]:
            response = api.core.start_adapter(adapter)
        else:
            response = api.core.restart_adapter(adapter)
        return response
    except Exception as e:
        print(e)


def restart_application(host: str, application: str) -> list[dict]:
    """
    Start (if application is stopped) or restart an application in IAP.

    :param host: Server hostname/FQDN.
    :param application: Name of application to be restarted (case-sensitive).
    """
    api = get_client(host)
    try:
        application_health = api.core.get_application_health(application)
        if "STOPPED" in application_health["state"]:
            response = api.core.start_application(application)
        else:
            response = api.core.restart_application(application)
        return response
    except Exception as e:
        print(e)


@restart_app.command("adapter", no_args_is_help=True)
def adapter(
    name: str = typer.Argument(
        ...,
        help="The target adapter name. [bold red]The adapter name is case-sensitive![/bold red]",
    ),
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    ),
) -> list[dict]:
    """Start (if adapter is stopped) or restart an adapter in IAP."""
    hosts = get_servers_from_inventory(hosts)
    try:
        data = runner(restart_adapter, hosts, args={"adapter": name})
        print(data)
    except Exception as e:
        print(e)


@restart_app.command("application", no_args_is_help=True)
def application(
    name: str = typer.Argument(
        ...,
        help="The target application name.",
        autocompletion=complete_application_name,
    ),
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    ),
) -> list[dict]:
    """Start (if application is stopped) or restart an application in IAP. Possible values are:\n
    AGManager
    AppArtifacts
    AutomationCatalog
    AutomationStudio
    ConfigurationManager
    FormBuilder
    JsonForms
    Jst
    LifecycleManager
    MOP
    OperationsManager
    Search
    Tags
    TemplateBuilder
    WorkflowBuilder
    WorkFlowEngine"""
    application = [app.value for app in Applications if app.name == name]
    hosts = get_servers_from_inventory(hosts)
    try:
        data = runner(restart_application, hosts, args={"application": application[0]})
        print(data)
    except Exception as e:
        print(e)
