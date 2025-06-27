import gendiff.utilities as utils

CHANGE_SYNTAX = {
    'added':          '  + ',
    'removed':        '  - ',
    'untouched':      '    '
}

INDENT = 4 * ' '


def make(change, key, value, level):
    if not isinstance(value, dict):
        return [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {value}"]
    # result = [(f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {{")]
    # result.append(f"{(level + 1) * INDENT}" + '}')
    # return result


def stylish(tree, level=0):
    result = []
    for key in sorted(tree):
        element = tree[key]
        change, value = element['change'], element['value']
        if change == 'updated':
            if isinstance(value, tuple):
                old, new = value
                result.extend(make('removed', key, old, level))
                result.extend(make('added', key, new, level))
            else:
                result.extend(make('untouched', key, value, level))
        else:
            result.extend(make(change, key, value, level))
    return ['{', result, '}'] if level == 0 else result


def render(mode, tree):
    if mode == 'stylish':
        formatter = stylish
    else:
        raise ValueError('Unknown formatting selected')
    return utils.flatten(formatter(tree['value']))
