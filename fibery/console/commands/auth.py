import typer

from fibery.console.commands.auth_token import token


auth = typer.Typer()
auth.add_typer(token, name="token")
