from typing import Any
from typing import Callable


def handle_result(data: Any, coerce_to: Callable = None, many: bool = False):
    if coerce_to is not None and not callable(coerce_to):
        raise ValueError(f"Callable expected in `coerce_to` got {coerce_to}")

    if coerce_to is None:
        return data

    if many is True:
        result = list(map(coerce_to, data))
    else:
        result = coerce_to(data)
    return result
