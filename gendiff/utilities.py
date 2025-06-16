def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{change_type}{key}: {value}"


def protect_singleton(text):
    match text:
        case True:
            return 'true'
        case False:
            return 'false'
        case None:
            return 'null'
    raise ValueError('Not a singleton')
