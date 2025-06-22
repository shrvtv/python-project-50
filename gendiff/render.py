import gendiff.utilities as utils

CHANGE_SYNTAX = {
    'added':     '  + ',
    'removed':   '  - ',
    'unchanged': '    ',
    'modified':  '    '
}

INDENT = 4 * ' '


def make_tree(change, children, level, key=None):
    if level == 0:  # root node check
        start, end = '{', '}'
    else:
        # CHANGE_SYNTAX replaces 1 INDENT
        start = f"{(level - 1) * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{'
        end = f"{level * INDENT}" + '}'

    return [start, *children, end]


def make_leaf(change_type, key, value, level):
    change_type = 'unchanged' if change_type == 'modified' else change_type
    # CHANGE_SYNTAX replaces 1 INDENT
    return (
        f"{(level - 1) * '    '}{CHANGE_SYNTAX[change_type]}{key}: {value}"
    ).rstrip()


def render(element, key=None, level=0):
    result = []
    change = element['change']
    if utils.is_tree(element):
        value = element['value']
        children = []
        for k in sorted(value.keys()):
            children.extend(render(
                value[k],
                k,
                level + 1
            ))
        result.extend(make_tree(change, children, level, key))
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
