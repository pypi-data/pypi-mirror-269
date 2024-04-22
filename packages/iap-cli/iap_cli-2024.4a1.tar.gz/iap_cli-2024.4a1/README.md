# itential-iap-cli
Lightweight CLI tool to simplify the process of interacting with the Itential Automation Platform.

This is an early alpha release. It is incomplete and will change.

The CLI tool is built using [Typer](https://typer.tiangolo.com/) and [Typer-CLI](https://typer.tiangolo.com/typer-cli/). It uses [iap-sdk](https://pypi.org/project/iap-sdk/) for any API calls to IAP.

This package was written for Itential Automation Platform 2023.1.

## Installation
Make sure you have a supported version of Python installed, and then create and activate a virtual environment:
```bash
python -m venv venv
source /venv/bin/activate
python -m pip install --upgrade pip
```
You can install the iap_cli from Pypi as follows:
```bash
pip install iap-cli
```
Or you can install it from source as follows:
```bash
git clone https://github.com/awetomate/itential-iap-cli.git
cd itential-iap-cli
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Verify
Verify that the CLI tool got installed correctly:
```bash
iap version
```

If the 'iap' command does not get recognised, try adding your current path to the Python path as follows:
```bash
export PYTHONPATH=`pwd`
```

### Install autocompletion for your shell
Install the autocompletion for your shell using the following command and then restart your terminal.
```bash
iap --install-completion
```

## First Steps / Setup
### Use the --help option
Use the --help option to see all available command completions for the current position. In most cases, sending an incomplete command will also show the help page.
If you have the autocompletion installed, you can just hit TAB-TAB, which will keep autocompleting and showing the available options.
```bash
iap --help
```
```
 Usage: iap [OPTIONS] COMMAND [ARGS]...

 CLI tool for interacting with Itential.

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                  │
│ --help                        Show this message and exit.                                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config                  Manage configurations for the Itential CLI app.                                                                                         │
│ get                     Get resources from your IAP server.                                                                                                     │
│ restart                 Restart resources in your IAP server.                                                                                                   │
│ version                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
```bash
iap get --help
```
```
 Usage: iap get [OPTIONS] COMMAND [ARGS]...

 Get resources from your IAP server.

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ adapters                       Get the health of all adapters for one or more servers.                                                                          │
│ applications                   Get the health of all applications for one more servers.                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### 1. Configure username and password
Define the username and password that will be used to connect to the IAP servers. The credentials will be stored in a .env file in your user profile. 
The CLI tool will use these credentials for all API calls.
```bash
iap config add credentials
```
```
Provide the user credentials to use to authenticate with the Itential servers.
The credentials will be stored in the /Users/your_user/.iap_cli/.env file.
Username: your_username
Password:
```

### 2. Add servers to your inventory
Add servers and/or clusters to an inventory file. An inventory.json file will created in your user profile.

Add individual server:
```bash
iap config add server
```
```
Provide a friendly name for the server (will be used for all CLI operations) and an FQDN/IP address.
The server will be stored in the /Users/your_user/.iap_cli/inventory.json file.
Server Friendly Name: dev1
Server FQDN or IP: iap1-dev.domain.com
```

Add a server cluster:
```bash
iap config add cluster
```
```
Provide a friendly name for the cluster (will be used for all CLI operations) and a comma-separated list of FQDNs/IP addresses.
The cluster will be stored in the /Users/your_user/.iap_cli/inventory.json file.
Cluster Friendly Name: devAll
Server FQDNs or IP addresses: iap1-dev.domain.com,iap2-dev.domain.com,iap3-dev.domain.com
```

The commands above will create an inventory.json file that looks like this:
```json
{
    "dev1": "iap1-dev.domain.com",
    "dev2": "iap2-dev.domain.com",
    "dev3": "iap3-dev.domain.com",
    "devAll": [
        "iap1-dev.domain.com",
        "iap2-dev.domain.com",
        "iap3-dev.domain.com"
    ]
}
```
If you have the autocompletion installed, you can just hit TAB-TAB, which will keep autocompleting and showing the available server/cluster names.
```bash
iap restart application AGManager dev
dev1    dev2    dev3    devAll
```
You can also modify the inventory.json file directly. 

## Available Operations
### config
| operation | description |
|---|---|
| iap config add credentials | Creates/updates a .env file to store the username and password to use for the API calls to IAP |
| iap config add cluster | Creates/updates an inventory.json file to store the server connections in.<br><br>Cluster Friendly Name:<br>Friendly/short name to identify the cluster. You will use this value for all CLI operations. E.g. devAll or PROD or cluster1<br><br>Server FQDNs or IP addresses:<br>A comma-separated string containing all server FQDNs or IP addresses. E.g. iap1-dev.domain.com,iap2-dev.domain.com,iap3-dev.domain.com |
| iap config add server | Creates/updates an inventory.json file to store the server connections in.<br><br>Server Friendly Name:<br>Friendly/short name to identify the server. You will use this value for all CLI operations. E.g. dev1 or PROD1 or server1<br><br>Server FQDNs or IP addresses:<br>The FQDN or IP address of the server. E.g. iap1-dev.domain.com |

### get
| operation | description |
|---|---|
| iap get adapters *host*| Get a list and health status for all adapters on the target server/cluster<br>*host*: Use the friendly name of the server/cluster as the target host.<br>Examples:<br>iap get adapters dev1<br>iap get adapters devAll|
| iap get applications *host* | Get a list and health status for all applications on the target server/cluster<br>*host*: Use the friendly name of the server/cluster as the target host.<br>Examples:<br>iap get applications dev1<br>iap get applications devAll |

If you have the autocompletion installed, you can just hit TAB-TAB, which will keep autocompleting and showing the available server/cluster names.

### restart
| operation | description |
|---|---|
| iap restart adapter *name* *host*| Start (if adapter is stopped) or restart an adapter in a server or a cluster of servers.<br>*name*: Enter the name of the adapter to start/restart(case-sensitive!)<br>*host*: Use the friendly name of the server/cluster as the target host.<br>Examples:<br>iap restart adapter ServiceNow devAll<br>iap restart adapter Email dev1<br><br>NOTE: the adapter name is case-sensitive!|
| iap restart application *name* *host* | Start (if application is stopped) or restart an application in a server or a cluster of servers.<br>*name*: Enter the name of the application to start/restart. Use autocompletion or use --help to see the list of available application names.<br>*host*: Use the friendly name of the server/cluster as the target host.<br>Examples:<br>iap restart application AGManager devAll<br>iap restart application Jst dev1 |

If you have the autocompletion installed, you can just hit TAB-TAB, which will keep autocompleting and showing the available server/cluster names and Application names (this does not work for adapter names).

### version
| operation | description |
|---|---|
| iap version | Displays the CLI app version. |
