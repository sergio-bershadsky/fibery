import functools
import json

from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

import typer
import yaml

from pydantic import BaseModel
from tabulate import tabulate

from fibery.conf import settings


def handle_item(item, exclude: List[str] = None):
    for key in exclude or []:
        if isinstance(item, dict):
            item.pop(key, None)
    if settings.output_format == "text":
        for k, v in item.items():
            if isinstance(v, (list, dict)):
                item[k] = yaml.dump(v, Dumper=yaml.Dumper, default_style="", allow_unicode=True)
    return item


class Output:

    data: Union[BaseModel, Dict, List, str]
    headers: Union[Literal["keys", "firstrow"], List[str]] = None
    exclude: Optional[List[str]] = None

    def __init__(self, data, headers=None, exclude=None):
        if isinstance(data, list):
            data = list(map(functools.partial(handle_item, exclude=exclude), data))
        elif isinstance(data, BaseModel):
            data = data.dict()
            data = handle_item(data, exclude)
        elif isinstance(data, dict):
            data = handle_item(data, exclude)

        self.data = data
        self.headers = headers
        self.exclude = exclude

    def echo(self):
        try:
            getattr(self, f"output_{settings.output_format}")()
        except AttributeError:
            raise ValueError(f"{settings.output_format} is not implemented")

    def output_text(self):
        data = self.data
        if isinstance(data, str):
            data = [[data]]
        elif isinstance(data, dict):
            data = list(data.items())
        typer.echo(tabulate(data, headers=self.headers or tuple()))

    def output_json(self):
        data = self.data
        data = json.dumps(data, indent=2, default=lambda v: str(v))
        typer.echo(data)


output = Output
