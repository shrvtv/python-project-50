import gendiff.utilities as utils

CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    '
}

INDENT_LENGTH = 4


def make_tree(change_type, key='', level=0):
    pass


def make_leaf(change_type, key, value, level=0):
    change_type = 'unchanged' if change_type == 'modified' else change_type
    return f"{level * '    '}{CHANGE_SYNTAX[change_type]}{key}: {value}"


def render(element, key=None, level=None):
    result = []
    change = element['change']
    if utils.is_tree(element):
        if key:
            result.append(
                make_leaf(change, key, '{', 0 if level is None else level)
            )
        children = element['value']
        for key in sorted(children.keys()):
            result.extend(
                render(children[key],
                       key,
                       0 if level is None else level + 1
                )
            )
        return result
    else:
        if change == 'modified':
            old, new = element['old'], element['new']
            result.append(make_leaf('removed', key, old, level))
            result.append(make_leaf('added', key, new, level))
        else:
            value = element['value']
            result.append(make_leaf(change, key, value, level))
        return result
