from typing import Optional

import typer

from fibery.conf import settings
from fibery.console.commands.api import api
from fibery.console.commands.auth import auth
from fibery.console.commands.config import config
from fibery.console.commands.describe import describe
from fibery.enums import FormatEnum


main = typer.Typer()
main.add_typer(auth, name="auth")
main.add_typer(config, name="config")
main.add_typer(api, name="api")
main.add_typer(describe, name="describe")


@main.callback()
def main_callback(format: Optional[FormatEnum] = None):
    settings.output_format = format or settings.output_format
