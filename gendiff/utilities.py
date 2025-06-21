CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    '
}


def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{CHANGE_SYNTAX[change_type]}{key}: {value}"


def protect_value(value, exception):
    if value is exception or isinstance(value, dict):
        return value
    return str(value)


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text


def make_path(path, key):
    return path + ('.' if path else '') + key
