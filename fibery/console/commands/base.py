import json

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Literal
from typing import Union

import typer

from pydantic import BaseModel
from tabulate import tabulate

from fibery.conf import settings


@dataclass
class Output:

    data: Union[BaseModel, Dict, List, str]
    headers: Union[Literal["keys", "firstrow"], List[str]] = None

    def __post_init__(self):
        try:
            getattr(self, f"output_{settings.output_format}")()
        except AttributeError:
            raise ValueError(f"{settings.output_format} is not implemented")

    def output_text(self):
        data = self.data
        if isinstance(data, BaseModel):
            data = list(data.dict().items())
        elif isinstance(data, str):
            data = [[data]]
        elif isinstance(data, dict):
            data = list(data.items())
        typer.echo(tabulate(data, headers=self.headers or tuple()))

    def output_json(self):
        data = self.data
        if isinstance(data, BaseModel):
            data = data.json(indent=2)
        else:
            data = json.dumps(data, indent=2)
        typer.echo(data)


output = Output
