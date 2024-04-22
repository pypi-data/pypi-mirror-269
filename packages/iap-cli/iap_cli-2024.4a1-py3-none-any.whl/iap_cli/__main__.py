"""
Allows Typer app to be run as a package instead of a single file.
"""

import typer

from . import iap

iap(prog_name="iap")
