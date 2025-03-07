import json
from pathlib import Path


def read_file(filename):
    path_to_file = Path(filename)
    match path_to_file.suffix:
        case ".json":
            return json.load(open(path_to_file))
        case _:
            raise ValueError("Unsupported file type")
