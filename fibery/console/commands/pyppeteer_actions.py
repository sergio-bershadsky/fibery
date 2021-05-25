import os

from contextlib import asynccontextmanager

from click import ClickException
from pyppeteer import launch
from pyppeteer.page import Page


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_DIR = os.path.normpath(os.path.join(BASE_DIR, "js"))


@asynccontextmanager
async def login(
    username: str,
    password: str,
    workspace: str,
    login_url: str = "https://fibery.io/login",
    debug: bool = False,
):
    browser = await launch(headless=not debug)
    page = await browser.newPage()

    await do_login(page, login_url, username, password)
    await do_switch_workspace(page, workspace)

    yield page

    await browser.close()


def js(name):
    with open(os.path.join(JS_DIR, name + ".js"), "r") as h:
        return h.read()


async def do_login(page: Page, url: str, username: str, password: str):
    await page.goto(url, waitUntil="networkidle2")
    await page.waitForSelector("#email")

    # Input username
    await page.focus("#email")
    await page.keyboard.type(username)
    await page.focus("#password")
    await page.keyboard.type(password)
    await page.click("#ui-email-form > button")

    # Wait for workspaces loaded
    await page.waitForNavigation()


async def do_switch_workspace(page: Page, name: str):
    await page.goto(f"https://{name}.fibery.io", waitUntil="networkidle0")


async def do_create_token(page: Page):
    page_function = js("token_create")
    result = await page.evaluate(page_function)
    if "value" not in result:
        raise ClickException(f"Error while creating token: {result}")
    return result["value"]


async def do_list_tokens(page: Page):
    page_function = js("token_list")
    result = await page.evaluate(page_function)
    if not isinstance(result, list):
        raise ClickException(f"Error while getting tokens: {result}")
    return result


async def do_delete_token(page: Page, token_id: str):
    page_function = js("token_delete")
    page_function = page_function.replace("#token_id", token_id)
    result = await page.evaluate(page_function)
    if result is not True:
        raise ClickException(f"Error while deleting token: {result}")
    return f"Token with id={token_id} deleted"
