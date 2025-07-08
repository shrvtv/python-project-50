import json

from gendiff.utilities import missing


def render(first, second):
    result = {}
    for key in sorted(first.keys() | second.keys()):
        old, new = first.get(key, missing), second.get(key, missing)
        if isinstance(old, dict) and isinstance(new, dict):
            result[key] = {
                'change': 'updated',
                'value': render(old, new)
            }
        else:
            if old is missing:
                result[key] = {
                    'change': 'added',
                    'value': new
                }
            elif new is missing:
                result[key] = {
                    'change': 'removed',
                    'value': old
                }
            elif old == new:
                result[key] = {
                    'change': 'untouched',
                    'value': old
                }
            else:
                result[key] = {
                    'change': 'updated',
                    'old_value': old,
                    'new_value': new
                }
    return json.dumps(result)
