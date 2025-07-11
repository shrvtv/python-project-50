from typing import Any

from gendiff.utilities import is_tree

CHANGE_SYNTAX = {
        'added':        '  + ',
        'removed':      '  - ',
        'untouched':    '    ',
        'updated_dict': '    '
        }

INDENT = 4 * ' '


def wrap_tree(level: int, change: str, key: str, processed_tree: list) -> list:
    result = [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{']
    result.extend(processed_tree)
    result.append((level + 1) * INDENT + '}')
    return result


def make(level: int, change: str, key: str, node: dict) -> list:
    def line(change: str, value: Any) -> list:
        return [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {value}"]

    def tree(change: str, children: dict) -> list:
        result = []
        for k, n in children.items():
            result.extend(make(level + 1, n['change'], k, n))
        return wrap_tree(level, change, key, result)

    if is_tree(node):
        return tree(change, node['children'])

    if change == 'updated':
        old, new = node['old'], node['new']
        old = (
            tree('removed', old['children'])
            if is_tree(old)
            else line('removed', old)
        )
        new = (
            tree('added', new['children'])
            if is_tree(new)
            else line('added', new)
        )
        return [*old, *new]
    return line(change, node['value'])


def render(comparison: dict, level: int = 0) -> list:
    result = []
    for key in sorted(comparison.keys()):
        node = comparison[key]
        change = node['change']
        if is_tree(node) and change == 'updated':
            result.extend(wrap_tree(
                level, 
                "updated_dict", 
                key,
                render(node['children'], level + 1)
            ))
        else:
            result.extend(make(level, change, key, node))
    return result
