from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field

from fibery.client.base import BaseResource


class FiberyField(BaseModel):
    id: str = Field(alias="fibery/id")
    name: str = Field(alias="fibery/name")
    type: str = Field(alias="fibery/type")
    meta: Dict[str, Any] = Field(alias="fibery/meta")


class FiberyType(BaseModel):
    id: str = Field(alias="fibery/id")
    name: str = Field(alias="fibery/name")
    fields: List[FiberyField] = Field(alias="fibery/fields")
    meta: Dict[str, Any] = Field(alias="fibery/meta")


class FiberySchema(BaseModel):
    id: str = Field(alias="fibery/id")
    types: List[FiberyType] = Field(None, alias="fibery/types")
    meta: Dict[str, Any] = Field(alias="fibery/meta")


class Schema(BaseResource):

    name = "fibery.schema/query"

    def get(self) -> FiberySchema:
        return self.client.command(self.name, coerce_to=FiberySchema.parse_obj)
