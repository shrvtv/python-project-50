import json
import os

import yaml

missing = object()


def make_path(path, key):
    return path + ('.' if path else '') + key


def parse(filename):
    current_location = os.getcwd()
    path = os.path.join(current_location, filename)
    file = open(path)
    if filename.endswith('.json'):
        return json.load(file)
    elif filename.endswith('.yaml') or filename.endswith('.yml'):
        return yaml.safe_load(file)
    else:
        raise ValueError('Invalid file type')


def protect_value(value, exception=missing):
    if value is exception or isinstance(value, dict):
        return value
    return str(value)


def flatten(data):
    result = []
    for element in data:
        if isinstance(element, list):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text
