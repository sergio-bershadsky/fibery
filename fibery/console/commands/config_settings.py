import typer

from fibery.conf import settings as fibery_settings
from fibery.console.commands.base import output


settings = typer.Typer()


@settings.command(name="show")
def settings_get():
    output(fibery_settings, headers=["name", "value"])
