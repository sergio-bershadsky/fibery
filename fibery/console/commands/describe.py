import functools

import typer

from click import ClickException
from typer import Argument

from fibery.client.fibery import Fibery
from fibery.client.schema import FiberySchema
from fibery.console.commands.base import output
from fibery.console.commands.utils import default_client


describe = typer.Typer()


def get_schema() -> FiberySchema:
    fibery = Fibery(client=default_client())
    return fibery.schema.get()


def handle_exceptions(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            raise ClickException(str(e))

    return wrapper


@describe.command("applications")
@handle_exceptions
def list_applications():
    """
    List all Fibery apps on your account
    """
    schema = get_schema()
    result = [app.dict() for app in schema.list_applications()]
    for item in result:
        item["types"] = len(item["types"])
    output(result, headers="keys").echo()


@describe.command("types")
@handle_exceptions
def list_types(application: str = None):
    """
    List Fibery types on your account
    """
    schema = get_schema()
    result = []
    for fibery_type in schema.list_types(application):
        result.append(
            {
                "Name": fibery_type.name,
                "Fields number": len(fibery_type.fields),
            }
        )
    output(result, headers="keys").echo()


@describe.command("type")
@handle_exceptions
def get_type(name: str):
    """
    Describe single Fibery type with all attributes on your account
    """
    schema = get_schema()
    fibery_type = schema.get_type(name)
    result = fibery_type.dict()
    result.update({"fields": [f.name for f in fibery_type.fields]})
    output(result).echo()


@describe.command("fields")
@handle_exceptions
def list_fields(fibery_type: str = Argument(..., metavar="type")):
    """
    List Fibery all Type fields on your account
    """
    schema = get_schema()
    fibery_type = schema.get_type(fibery_type)
    result = []
    for field in fibery_type.fields:
        result.append(
            {
                "Name": field.name,
                "Type": field.type,
            }
        )
    output(result, headers="keys").echo()


@describe.command("field")
@handle_exceptions
def get_field(fibery_type: str = Argument(..., metavar="type"), name: str = Argument(...)):
    """
    Get single Field description on your account
    """
    schema = get_schema()
    fibery_type = schema.get_type(fibery_type)
    result = fibery_type.get_field(name)
    output(result).echo()


@describe.command(name="webhooks")
def list_webhooks():
    """
    List all registered hooks on your account
    """
    fibery = Fibery(client=default_client())
    webhooks = fibery.webhook.list()

    result = []
    for webhook in webhooks:
        result.append(webhook.dict())

    output(result, headers="keys", exclude=["runs"]).echo()
