import copy


def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{change_type}{key}: {value}"


def protect_value(value, exception):
    if value is exception:
        return exception
    if isinstance(value, dict):
        return copy.deepcopy(value)
    return str(value)


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text


def make_path(path, key):
    return path + ('.' if path else '') + key


def make_element(element_type, change, value, location):
    return {
            'type': element_type,
            'path': location,
            'change': change,
            'value': value
    }
