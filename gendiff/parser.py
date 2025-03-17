import json

import yaml


def read_file(path_to_file):
    match path_to_file.suffix:
        case ".json":
            return json.load(open(path_to_file))
        case ".yml" | ".yaml":
            return yaml.safe_load(open(path_to_file))
        case _:
            raise ValueError("Unsupported file type")
