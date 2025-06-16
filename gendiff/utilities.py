def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{change_type}{key}: {value}"


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text
