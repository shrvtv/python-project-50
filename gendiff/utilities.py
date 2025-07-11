import json
import os

import yaml

missing = object()


def parse(filename: str) ->dict:
    current_location = os.getcwd()
    path = os.path.join(current_location, filename)
    file = open(path)
    if filename.endswith('.json'):
        return json.load(file)
    elif filename.endswith('.yaml') or filename.endswith('.yml'):
        return yaml.safe_load(file)
    else:
        raise ValueError('Invalid file type')


def is_tree(node) -> bool:
    return (
        True if isinstance(node, dict) and 'children' in node.keys() else False
    )


def flatten(data: list) -> list:
    result = []
    for element in data:
        if isinstance(element, list):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def mimic_json(text: str) -> str:
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text
