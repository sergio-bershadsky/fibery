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

    def get_field(self, name) -> FiberyField:
        for f in self.fields:
            if f.name.strip() == name.strip():
                return f

        choices = ", ".join([f"'{f.name}'" for f in self.fields])
        raise Exception(f"Field '{name}' does not exist, choices are: {choices}")


class FiberyApplication(BaseModel):
    name: str
    types: List[FiberyType]


class FiberySchema(BaseModel):
    id: str = Field(alias="fibery/id")
    types: List[FiberyType] = Field(None, alias="fibery/types")
    meta: Dict[str, Any] = Field(alias="fibery/meta")

    def list_applications(self) -> List[FiberyApplication]:
        result = {}
        for t in self.types:
            app_name, type_name = t.name.split("/", 1)
            if app_name not in result:
                result[app_name] = FiberyApplication(name=app_name, types=[t])
            else:
                result[app_name].types.append(t)
        return list(sorted(result.values(), key=lambda a: a.name.lower()))

    def has_application(self, application):
        result = set()
        for t in self.types:
            app_name, type_name = t.name.split("/", 1)
            result.add(app_name)
        return application in result

    def list_types(self, application=None):
        result = []
        all_applications = self.list_applications()
        application_choices = ", ".join([f"'{app.name}'" for app in all_applications])
        if application and not self.has_application(application):
            raise Exception(f"Application '{application}' does not exist, choices are: {application_choices}")

        for fibery_type in sorted(self.types, key=lambda v: v.name.lower()):
            type_application, table = fibery_type.name.split("/", 1)
            if application and application != type_application:
                continue
            result.append(fibery_type)
        return result

    def get_type(self, name) -> FiberyType:
        for t in self.types:
            if t.name.strip() == name.strip():
                return t

        choices = ", ".join([f"'{t.name}'" for t in self.types])
        raise Exception(f"Type '{name}' does not exist, choices are: {choices}")


class Schema(BaseResource):

    name = "fibery.schema/query"

    def get(self) -> FiberySchema:
        return self.client.command(self.name, coerce_to=FiberySchema.parse_obj)
