from gendiff.utilities import missing


def convert(value):
    if isinstance(value, dict):
        return "[complex value]"
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def make_line(change, key_location, value):
    result = f"Property '{key_location}' was {change}"  # covers the 'removed'
    if change == 'added':
        result += f" with value: {convert(value)}"
    elif change == 'updated':
        old, new = value
        result += f". From {convert(old)} to {convert(new)}"
    return result


def render(first, second, location=''):
    def locate(k):
        if location == '':
            return k
        return location + '.' + k

    result = []
    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, missing)
        new = second.get(key, missing)
        if new is missing:
            result.append(make_line('removed', locate(key), old))
        elif old is missing:
            result.append(make_line('added', locate(key), new))
        elif old != new:
            if isinstance(old, dict) and isinstance(new, dict):
                result.extend(render(old, new, locate(key)))
            else:
                result.append(make_line('updated', locate(key), (old, new)))
    return result