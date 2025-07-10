from gendiff.utilities import flatten, is_tree

CHANGE_SYNTAX = {
        'added': '  + ',
        'removed': '  - ',
        'untouched': '    ',
        'updated_dict': '    '
        }

INDENT = 4 * ' '


def make(level, change, key, data):
    def line():
        return [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: {data}"]

    def tree():
        result = [f"{level * INDENT}{CHANGE_SYNTAX[change]}{key}: " + '{']
        if change == 'updated_dict':
            result.extend(data)
        result.append((level + 1) * INDENT + '}')
        return result

    return tree() if isinstance(data, (dict, list)) else line()


def render(comparison, level=0):
    result = []
    for key in sorted(comparison.keys()):
        node = comparison[key]
        change = node['change']
        if change == 'updated':
            if is_tree(node):
                result.extend(make(
                    level, 
                    "updated_dict", 
                    key,
                    render(node['children'], level + 1)
                ))
            else:
                result.extend(make(level, 'removed', key, node['old']))
                result.extend(make(level, 'added', key, node['new']))
        else:
            if is_tree(node):
                result.extend(make(level, change, key, node['children']))
            else:
                result.extend(make(level, change, key, node['value']))
    return result
