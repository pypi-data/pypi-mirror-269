from operator import itemgetter

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from iap_cli.models.iap import (
    AdaptersHealthGetResponse,
    AdaptersHealthResult,
    ApplicationsHealthGetResponse,
    ApplicationsHealthResult,
)
from iap_cli.utils import (
    complete_server_name,
    get_client,
    get_servers_from_inventory,
    runner,
)

# define Typer app
get_app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Get resources from your IAP server.",
)
console = Console()


def get_adapters_health(host: str) -> AdaptersHealthResult:
    """
    Get the health of all adapters. Used for the Adapters Status Report

    :param host: Server hostname/FQDN.
    """
    api = get_client(host)
    try:
        response = api.core.get_adapters_health()
        results = AdaptersHealthGetResponse(**response)
        return results.results
    except Exception as e:
        print(e)


def get_applications_health(host: str) -> ApplicationsHealthResult:
    """
    Get the health of all applications. Used for the Applications Status Report

    :param host: Server hostname/FQDN.
    """
    api = get_client(host)
    try:
        response = api.core.get_applications_health()
        results = ApplicationsHealthGetResponse(**response)
        return results.results
    except Exception as e:
        print(e)


@get_app.command("adapters")
def adapters(
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    )
) -> AdaptersHealthResult:
    """Get the health of all [bold]adapters[/bold] for one or more servers."""
    hostnames = get_servers_from_inventory(hosts)
    try:
        data = runner(get_adapters_health, hostnames, ordered=True)
        render_adapter_report(data, env=hosts)
    except Exception as e:
        print(e)


@get_app.command("applications")
def applications(
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    )
) -> ApplicationsHealthResult:
    """Get the health of all [bold]applications[/bold] for one more servers."""
    hostnames = get_servers_from_inventory(hosts)
    try:
        data = runner(get_applications_health, hostnames, ordered=True)
        render_application_report(data, env=hosts)
    except Exception as e:
        print(e)


def render_adapter_report(data: list[dict], env: str) -> None:
    """
    Render Adapter Status Report table using the 'rich' package

    :param data: API results response returned by the 'runner' helper function.
    :param env: Name of the environment/hosts. Used for report title.
    """
    # get a set of all unique adapter names
    adapter_names = {adapter.id for host in data for adapter in host["response"]}
    # create table rows -> dictionaries listing the adapter status for each host
    rows = []
    for name in adapter_names:
        row = {}
        row["package_id"] = ""
        row["id"] = name
        for host in data:
            for adapter in host["response"]:
                if adapter.id == name:
                    row["package_id"] = adapter.package_id
                    row[f"{host['host']}"] = (
                        f"{adapter.state} / {adapter.connection['state']}"
                    )
        rows.append(row)
    # sort rows by packackge ID and then by Adapter ID
    rows = sorted(rows, key=itemgetter("package_id", "id"))
    # create table
    columns = ["Package ID", "Adapter ID"]
    for host in data:
        columns += [f"{host['host'].split('.')[0]}"]
    table = Table(title=f"Adapter Status Report {env}")
    for column in columns:
        table.add_column(column, justify="left", no_wrap=True)
    for row in rows:
        # if the adapter status on any of the hosts is not 'RUNNING / ONLINE', highlight the row
        errors = set(list(row.values())[2:]) - {"RUNNING / ONLINE"}
        if errors:
            style = "yellow"
        else:
            style = None
        table.add_row(*row.values(), style=style)
    console.print()
    console.print(table)


def render_application_report(data: list[dict], env: str) -> None:
    """
    Render Application Status Report table using the 'rich' package

    :param data: API results response returned by the 'runner' helper function.
    :param env: Name of the environment/hosts. Used for report title.
    """
    # get a set of all unique application names
    application_names = {app.id for host in data for app in host["response"]}
    # create table rows -> dictionaries listing the application status for each host
    rows = []
    for name in application_names:
        row = {}
        row["id"] = name
        for host in data:
            for app in host["response"]:
                if app.id == name:
                    row[f"{host['host']}"] = app.state
        rows.append(row)
    # sort rows by Application ID
    rows = sorted(rows, key=itemgetter("id"))
    # create table
    columns = ["App ID"]
    for host in data:
        columns += [f"{host['host'].split('.')[0]}"]
    table = Table(title=f"Application Status Report {env}")
    for column in columns:
        table.add_column(column, justify="left", no_wrap=True)
    for row in rows:
        # if the application status on any of the hosts is not 'RUNNING', highlight the row
        errors = set(list(row.values())[1:]) - {"RUNNING"}
        if errors:
            style = "yellow"
        else:
            style = None
        table.add_row(*row.values(), style=style)
    console.print()
    console.print(table)
