import gendiff.utilities as utils

CHANGE_SYNTAX = {
    'added':          '  + ',
    'removed':        '  - ',
    'unchanged':      '    ',
    'modified_dict':  '    '
}

INDENT = 4 * ' '


def render_node(change, value, level, key=None):
    # CHANGE_SYNTAX replaces 1 INDENT
    if isinstance(value, list):
        if level == 0:  # root node check
            start, end = '{', '}'
        else:
            # CHANGE_SYNTAX replaces 1 INDENT
            start = f"{(level - 1) * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{'
            end = f"{level * INDENT}" + '}'

        return [start, *value, end]

    if isinstance(value, dict):
        children = []
        for k in sorted(value.keys()):
            children.extend(render_node('unchanged', value[k], level + 1, k))
        return render_node(change, children, level, key)

    return [(
                f"{(level - 1) * '    '}{CHANGE_SYNTAX[change]}{key}: {value}"
            ).rstrip()]


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
        result.extend(render_node(change, children, level, key))
        return result
    else:
        if change == 'modified':
            old, new = element['old'], element['new']
            result.extend(render_node('removed', old, level, key))
            result.extend(render_node('added', new, level, key))
        else:
            value = element['value']
            result.extend(render_node(change, value, level, key))
        return result
