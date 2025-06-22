import json
import os

import yaml


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


def protect_value(value, exception):
    if value is exception or isinstance(value, dict):
        return value
    return str(value)


def is_tree(node):
    return isinstance(node.get('value'), dict)


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text
