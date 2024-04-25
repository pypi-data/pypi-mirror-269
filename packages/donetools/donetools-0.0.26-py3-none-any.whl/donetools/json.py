import json
import os

import donetools

def dump(obj: dict | list, path: str, indent: int = 4, mode: str = 'w') -> None:
    """Dump a JSON file."""
    os.makedirs(donetools.path.dirname(path), exist_ok=True)
    with open(path, mode=mode) as file:
        json.dump(obj, file, indent=indent)

def load(path: str) -> dict | list:
    """Load a JSON file."""
    with open(path, mode='r') as file:
        return json.load(file)
