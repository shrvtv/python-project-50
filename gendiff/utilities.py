def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{change_type}{key}: {value}"


def protect_value(value, exception):
    return str(value) if value != exception else exception


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text


def make_location(location, key):
    return location + ('.' if location else '') + key
