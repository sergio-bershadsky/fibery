import asyncio

import typer

from fibery.conf import settings
from fibery.console.commands import pyppeteer_actions as action
from fibery.console.commands.base import output


token = typer.Typer()


@token.callback()
def token_callback(username: str = typer.Option(None), workspace: str = typer.Option(None)):
    settings.username = username or settings.username
    settings.workspace = workspace or settings.workspace


def run(coroutine):
    asyncio.get_event_loop().run_until_complete(coroutine)


def get_password():
    password = settings.password.get_secret_value()
    return password or typer.prompt("Password", hide_input=True)


@token.command(name="create")
def token_create():

    # Get password securely
    password = get_password()

    async def login_and_create_token():
        async with action.login(settings.username, password, settings.workspace, settings.login_url) as page:
            result = await action.do_create_token(page)
            output(result, headers=["Token created"])

    run(login_and_create_token())


@token.command(name="list")
def token_list():

    # Get password securely
    password = get_password()

    async def login_and_list_tokens():
        async with action.login(settings.username, password, settings.workspace, settings.login_url) as page:
            result = await action.do_list_tokens(page)
            output(result, headers="keys")

    run(login_and_list_tokens())


@token.command(name="delete")
def token_delete(token_id: str = typer.Option(...)):

    # Get password securely
    password = get_password()

    async def login_and_delete_token():
        async with action.login(settings.username, password, settings.workspace, settings.login_url) as page:
            result = await action.do_delete_token(page, token_id)
            output(result)

    run(login_and_delete_token())
