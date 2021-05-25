from typing import TYPE_CHECKING
from typing import Callable
from typing import Literal

import requests

from fibery.client.utils import handle_result


if TYPE_CHECKING:
    from fibery.client.fibery import Fibery


class ArgsDescriptor:
    pass


class FiberyApiError(Exception):
    pass


class BaseClient:

    workspace: str
    endpoint: str

    def __init__(self, token, workspace, endpoint="https://{workspace}.fibery.io/api/"):
        self.endpoint = endpoint.format(workspace=workspace)
        self.workspace = workspace
        self.token = token


class SyncClient(BaseClient):
    def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        resource,
        json: dict = None,
        data: str = None,
        coerce_to: Callable = None,
        many=False,
    ):

        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = "/".join([self.endpoint.strip("/"), resource])
        response = requests.request(method, url, json=json, data=data, headers=headers)
        if response.status_code != 200:
            raise FiberyApiError(f"Error {response.status_code}: {response.content}")

        result = response.json()
        return handle_result(result, coerce_to=coerce_to, many=many)

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def update(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)

    def create(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)

    def command(self, command, args=None, coerce_to: Callable = None, many=False):
        payload = {"command": command}
        if args:
            payload.update({"args": args})

        result = self.request("POST", "commands", json=[payload])[0]
        success = result["success"]
        result = result["result"]
        if not success:
            raise FiberyApiError(result)
        return handle_result(result, coerce_to=coerce_to, many=many)


class BaseResource:

    fibery: "Fibery" = None
    name: str = None

    def __init__(self, fibery):
        self.fibery = fibery

    @property
    def client(self):
        return self.fibery.client

    def get_methods(self):
        result = []
        for c in dir(self):
            member = getattr(self, c)
            if not callable(member):
                continue
            if c in {"init", "get_methods"}:
                continue
            if c.startswith("_"):
                continue
            result.append(c)

        return result
