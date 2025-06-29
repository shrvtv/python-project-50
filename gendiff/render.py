import gendiff.utilities as utils


def make_stylish(change, key, value, level):
    CHANGE_SYNTAX = {
        'added': '  + ',
        'removed': '  - ',
        'untouched': '    ',
        'updated_dict': '    '
        }
    INDENT = 4 * ' '
    if change == 'updated':
        old, new = value
        return [
            make_stylish('removed', key, old, level),
            make_stylish('added', key, new, level)
        ]

    def line():
        return [
            f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {value}".rstrip()
        ]

    def tree():
        result = [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{']
        if isinstance(value, list):
            result.extend(utils.flatten(value))
        else:
            for k in sorted(value.keys()):
                result.extend(make_stylish('untouched', k, value[k], level + 1))
        result.append((level + 1) * INDENT + '}')
        return result
    return tree() if isinstance(value, (dict, list)) else line()


def make_plain(change, key, value, location):
    pass
