from fibery.client.base import BaseClient
from fibery.client.schema import Schema
from fibery.client.webhook import WebHook


class Fibery:

    client: BaseClient = None

    def __init__(self, client: BaseClient):
        self.client = client

    @property
    def webhook(self) -> WebHook:
        return WebHook(self)

    @property
    def schema(self) -> Schema:
        return Schema(self)

    def get_resources(self):
        return [c for c in dir(self) if isinstance(getattr(self, c), WebHook)]
