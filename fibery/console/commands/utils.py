from fibery.client.base import SyncClient
from fibery.conf import settings


def default_client(cls=SyncClient):
    return cls(token=settings.api_token.get_secret_value(), workspace=settings.workspace)
