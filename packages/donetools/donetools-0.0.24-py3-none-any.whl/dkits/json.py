import json
import os
import typing

import dkits

T = typing.TypeVar('T')

def dump(obj: typing.Any, path: str, indent: int = 4, mode: str = 'w') -> None:
    """Dump a JSON file."""
    os.makedirs(dkits.path.dirname(path), exist_ok=True)
    with open(path, mode=mode) as file:
        json.dump(obj, file, indent=indent)

def load(path: str, datatype: typing.Type[T] = dict) -> T:
    """Load a JSON file."""
    with open(path, mode='r') as file:
        return datatype(**json.load(file))
