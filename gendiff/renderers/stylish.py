from gendiff.utilities import flatten, missing

CHANGE_SYNTAX = {
        'added': '  + ',
        'removed': '  - ',
        'untouched': '    ',
        'updated_dict': '    '
        }

INDENT = 4 * ' '


def make(change, key, value, level):
    if change == 'updated':
        old, new = value
        return [
            make('removed', key, old, level),
            make('added', key, new, level)
        ]

    def line():
        return [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {value}"]

    def tree():
        result = [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{']
        if isinstance(value, list):
            result.extend(flatten(value))
        else:
            for k in sorted(value.keys()):
                result.extend(
                    make('untouched', k, value[k], level + 1)
                )
        result.append((level + 1) * INDENT + '}')
        return result

    return tree() if isinstance(value, (dict, list)) else line()


def render(first, second, level=0):
    result = []
    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, missing)
        new = second.get(key, missing)
        if new is missing:
            result.extend(make('removed', key, old, level))
        elif old is missing:
            result.extend(make('added', key, new, level))
        elif old == new:
            result.extend(make('untouched', key, old, level))
        else:
            if isinstance(old, dict) and isinstance(new, dict):
                result.extend(make(
                    'updated_dict',
                    key,
                    render(old, new, level + 1),
                    level
                ))
            else:
                result.extend(make(
                    'updated',
                    key,
                    (old, new),
                    level
                ))
    return result
