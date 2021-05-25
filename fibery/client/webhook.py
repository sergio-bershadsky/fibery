from typing import List
from typing import Optional

from pydantic import AnyUrl
from pydantic import BaseModel

from fibery.client.base import BaseResource
from fibery.models import FiberyEntityType


class Run(BaseModel):
    http_status: Optional[str]
    elapsed_time: Optional[str]
    request_time: Optional[str]


class AddResult(BaseModel):
    id: int
    url: AnyUrl
    type: FiberyEntityType
    state: str
    runs: List[Run] = []


class GetResult(AddResult):
    pass


class WebHook(BaseResource):

    name = "webhooks/v2"

    def create(self, url: str, type: FiberyEntityType) -> AddResult:
        return self.client.create(self.name, json={"url": url, "type": type}, coerce_to=AddResult.parse_obj)

    def list(self) -> List[GetResult]:
        return self.client.get(self.name, coerce_to=GetResult.parse_obj, many=True)

    def delete(self, pk) -> bool:
        name = f"{self.name}/{pk}"
        return self.client.delete(name)
