import typer

from fibery.console.commands.config_settings import settings


config = typer.Typer()
config.add_typer(settings, name="settings")
