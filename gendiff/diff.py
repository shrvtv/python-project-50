from typing import Any

from gendiff.utilities import missing


def build_node(change: str, value: Any, is_diff: bool = False) -> dict:
    if isinstance(value, dict):
        if is_diff:
            return {
                'change': change,
                'children': value
            }

        children = {}
        for key in value:
            children[key] = build_node('untouched', value[key])
        return {
            'change': change,
            'children': children
        }

    if change == 'updated':
        old, new = value
        if isinstance(old, dict):
            old = build_node('untouched', old)
        if isinstance(new, dict):
            new = build_node('untouched', new)

        return {
            'change': change,
            'old': old,
            'new': new
        }

    return {
        'change': change,
        'value': value
    }


def compare(first: dict, second: dict) -> dict:
    comparison = {}
    for key in first.keys() | second.keys():
        old = first.get(key, missing)
        new = second.get(key, missing)

        if new is missing:
            comparison[key] = build_node('removed', old)
        elif old is missing:
            comparison[key] = build_node('added', new)
        elif old == new:
            comparison[key] = build_node('untouched', old)
        else:
            if isinstance(old, dict) and isinstance(new, dict):
                comparison[key] = build_node(
                    'updated', compare(old, new), is_diff=True
                )
            else:
                comparison[key] = build_node('updated', (old, new))

    return comparison
