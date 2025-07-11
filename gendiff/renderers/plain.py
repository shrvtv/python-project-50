from gendiff.utilities import is_tree


def get_converted_value(node: dict, key: str) -> str:
    if is_tree(node):
        return "[complex value]"

    value = node[key]
    if is_tree(value):
        return "[complex value]"
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def make_line(node: dict, key_location: str) -> str:
    change = node['change']
    result = f"Property '{key_location}' was {change}"  # covers the 'removed'
    if change == 'added':
        result += f" with value: {get_converted_value(node, 'value')}"
    elif change == 'updated':
        result += (
            f". From {get_converted_value(node, 'old')} to "
            f"{get_converted_value(node, 'new')}"
        )
    return result


def render(comparison: dict, location: str = '') -> list:
    def locate(k: str) -> str:
        if location == '':
            return k
        return location + '.' + k

    result = []
    for key in sorted(comparison.keys()):
        node = comparison[key]
        change = node['change']
        if is_tree(node) and change == 'updated':
            result.extend(render(node['children'], locate(key)))
        elif change != 'untouched':
            result.append(make_line(node, locate(key)))
    return result
