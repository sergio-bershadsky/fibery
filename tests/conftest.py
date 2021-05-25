import pytest

from fibery.client.fibery import Fibery
from fibery.conf import MaskedSecretStr, settings
from fibery.console.commands.utils import default_client


@pytest.fixture
def setup():
    settings.workspace = "foobar"
    settings.username = "username"
    settings.password = MaskedSecretStr("password")
    settings.api_token = MaskedSecretStr("token")


@pytest.fixture
def fibery():
    return Fibery(client=default_client())
