from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel


FiberyEntityType = str


class BaseEffect(BaseModel):
    id: str
    type: FiberyEntityType


class FiberyEntityCreateEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/create"
    values: Dict[str, Any]


class FiberyEntityUpdateEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/update"
    values: Dict[str, Any]
    valuesBefore: Dict[str, Any]


class FiberyEntityDeleteEffect(BaseEffect):
    effect: Literal["fibery.entity/update"] = "fibery.entity/delete"
    valuesBefore: Dict[str, Any]


class FiberyAddCollectionItemsEffect(BaseEffect):
    effect: Literal["fibery.entity/add-collection-items"] = "fibery.entity/add-collection-items"
    field: str
    items: List[Dict[str, Any]]


class FiberyRemoveCollectionItemsEffect(BaseEffect):
    effect: Literal["fibery.entity/add-collection-items"] = "fibery.entity/remove-collection-items"
    field: str
    items: List[Dict[str, Any]]
