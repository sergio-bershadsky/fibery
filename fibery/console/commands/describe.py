import typer

from typer import Option

from fibery.client.fibery import Fibery
from fibery.client.schema import FiberySchema
from fibery.conf import settings
from fibery.console.commands.base import output
from fibery.console.commands.utils import default_client


describe = typer.Typer()


def list_types(schema: FiberySchema, filter_application):
    result = []
    for fibery_type in sorted(schema.types, key=lambda v: v.name):
        application, table = fibery_type.name.split("/", 1)
        if filter_application and filter_application != application:
            continue
        result.append(
            {
                "ID": fibery_type.id,
                "Application": application,
                "Name": fibery_type.name,
                "Fields number": len(fibery_type.fields),
            }
        )

    output(result, headers="keys")


def _describe_type(schema, name):
    for fibery_type in schema.types:
        if fibery_type.name.strip() == name.strip():
            break
    else:
        raise Exception(f"Type '{name}' does not exists")

    if settings.output_format == "text":
        fibery_type = fibery_type.dict()

        meta = fibery_type.pop("meta", None)
        fields = fibery_type.pop("fields", None)

        typer.echo("Type:")
        output(fibery_type, headers=["property", "value"])
        typer.echo("\n")
        typer.echo("Meta:")
        output(meta, headers=["property", "value"])
        typer.echo("\n")
        typer.echo("Fields:")
        output(list(sorted(fields, key=lambda v: v["name"])), headers="keys")


@describe.command(name="type")
def describe_type(
    name: str = Option(None, help="Get type by name"),
    application: str = Option(None, help="Filter by application name, applied if only name is empty"),
):
    """
    List/Get Fibery types
    """
    fibery = Fibery(client=default_client())

    schema = fibery.schema.get()

    if name:
        return _describe_type(schema, name)
    else:
        return list_types(schema, application)


@describe.command(name="field")
def describe_field(
    name: str = Option(None, help="Get type by name"),
    application: str = Option(None, help="Filter by application name, applied if only name is empty"),
):
    """
    List/Get Fibery types
    """
    fibery = Fibery(client=default_client())

    schema = fibery.schema.get()

    if name:
        return _describe_type(schema, name)
    else:
        return list_types(schema, application)


@describe.command(name="webhook")
def describe_webhook():
    """
    List available hooks
    """
    fibery = Fibery(client=default_client())
    webhooks = fibery.webhook.list()

    result = []
    for item in webhooks.dict()["__root__"]:
        item.pop("runs")
        result.append(item)

    output(result, headers="keys")
