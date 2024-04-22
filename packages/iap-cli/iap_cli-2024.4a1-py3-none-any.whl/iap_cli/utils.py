#!/usr/bin/env python3
"""
Collection of reusable helper functions
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Union

from dotenv import load_dotenv
from iap_sdk import Iap

from iap_cli.commands.config.add import add_credentials, add_server
from iap_cli.config import APP_DIR, CREDENTIALS_FILEPATH, INVENTORY_FILEPATH
from iap_cli.enums import Applications


def clear_screen() -> None:
    """Clears terminal screen."""
    os.system("clear")


def complete_application_name(incomplete: str):
    """
    Function used for Typer-cli autocompletion of application names.

    :param incomplete: Beginning character(s) of the application name
    """
    for app in Applications:
        if app.name.startswith(incomplete):
            yield app.name


def complete_server_name(incomplete: str):
    """
    Function used for Typer-cli autocompletion of server names.

    :param incomplete: Beginning character(s) of the server name
    """
    servers = get_all_servers_from_inventory()
    for name in servers.keys():
        if name.startswith(incomplete):
            yield name


def get_all_servers_from_inventory() -> dict:
    """
    Helper function to load the entire inventory.json file
    """
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not INVENTORY_FILEPATH.exists():
        add_server()
    with open(f"{INVENTORY_FILEPATH}", "r", encoding="utf-8") as file:
        inventory = json.load(file)
    return inventory


def get_client(host: str) -> Iap:
    """Create Iap connection instance"""
    # load environment vars
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not CREDENTIALS_FILEPATH.exists():
        add_credentials()
    load_dotenv(dotenv_path=CREDENTIALS_FILEPATH)
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    api = Iap(
        host=host,
        username=username,
        password=password,
        verify=False,
    )
    return api


def get_servers_from_inventory(server_group: str) -> list[str]:
    """
    Helper function to load the IAP server name(s) from inventory.json

    :param server_group: Friendly name of the server/cluster as defined in your inventory.json file
    """
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not INVENTORY_FILEPATH.exists():
        add_server()
    with open(f"{INVENTORY_FILEPATH}", "r", encoding="utf-8") as file:
        inventory = json.load(file)
        servers = inventory[server_group]
        if isinstance(servers, str):
            servers = [servers]
    return sorted(servers)


def runner(
    function: str,
    devices: Union[list[str], str],
    max_workers: int = 30,
    ordered: bool = True,
    args: dict[str, Any] = None,
) -> list[Any]:
    """
    Generic function that allows for running other functions in parallel using the ThreadPoolExecutor.

    :param function: The name of the target function to be run concurrently.
    :param devices: Iterable to use with function (device class instances, hostnames/IPs (depends on target function)).
    :param max_workers: Optional. The maximum number of threads that can be used to execute the given calls. Default = 30
    :param ordered: Optional. Returns the result objects in the same order as the input. Default = True
    :param args: Optional. dictionary containing arguments to be provided to the target function. Default = None
    """
    # check if single host or multiple hosts. Turn single host str into list
    if isinstance(devices, str):
        devices = [devices]
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if args:
            future_to_host = {
                executor.submit(function, device, **args): (idx, device)
                for idx, device in enumerate(devices)
            }
        else:
            future_to_host = {
                executor.submit(function, device): (idx, device)
                for idx, device in enumerate(devices)
            }
        if ordered:
            futures = {}
            for future in as_completed(future_to_host):
                idx, host = future_to_host[future]
                futures[idx] = host, future
            for idx in range(len(futures)):
                host, future = futures[idx]
                try:
                    data = future.result()
                    results.append({"host": host, "response": data})
                except Exception as exc:
                    results.append(f"{host} generated an exception: {exc}")
        else:
            for future in as_completed(future_to_host):
                _, host = future_to_host[future]
                try:
                    data = future.result()
                    results.append({"host": host, "response": data})
                except Exception as exc:
                    results.append(f"{host} generated an exception: {exc}")
    return results
