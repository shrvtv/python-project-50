from pathlib import Path

import gendiff.parser

MISSING = object()
INDENT = "    "
COMPARISON = {
    "unchanged": "    ",
        "added": "  + ",
      "removed": "  - "
}


def flatten_recursively(nested_list):
    """GENERATOR that yields nested lists recursively."""
    for i in nested_list:
        if isinstance(i, list):
            yield from flatten_recursively(i)
        else:
            yield i


def indent(content):
    """Add a single indent to the entire input."""
    if isinstance(content, list):
        return [INDENT + line for line in flatten_recursively(content)]
    return INDENT + content


def wrap_list(content, beginning=MISSING):
    """Wrap a list into curly braces according to the requirements."""
    beginning_exists = True if beginning is not MISSING else False
    if beginning_exists:
        return [
            f"{beginning}: {{",
            *indent(content),
            # additional indentation is required to balance comparison's prefix
            indent('}')
        ]
    else:
        return ['{', *content, '}']


def create_entry(key, value, comparison_result="unchanged"):
    """Covers all cases that do not require dictionary comparison."""
    # COMPARISON["changed"] is never accessed
    beginning = COMPARISON[comparison_result] + key
    if isinstance(value, dict):
        return wrap_list(
            [create_entry(k, v)
             for k, v in value.items()],
            beginning
        )
    else:
        return f"{beginning}: {value}"


def compare_values(first, second):
    if first == second:
        return "unchanged", first
    if first is MISSING:
        return "added", second
    if second is MISSING:
        return "removed", first
    return "changed", ...


def generate_comparison(dict1, dict2):
    """Compare 2 dictionaries keeping the formatting as per requirements."""
    all_keys_sorted = sorted(dict1.keys() | dict2.keys())
    result = []

    for key in all_keys_sorted:
        value1, value2 = dict1.get(key, MISSING), dict2.get(key, MISSING)
        diff, value = compare_values(value1, value2)

        if diff == "changed":
            if isinstance(value1, dict) and isinstance(value2, dict):
                result.append(indent([
                    f"{key}: {'{'}",
                    generate_comparison(value1, value2),
                    '}'
                ]))
            else:
                result.append(create_entry(key, value1, "removed"))
                result.append(create_entry(key, value2, "added"))
        else:
            result.append(create_entry(key, value, diff))

    return result


def generate_diff(file_path1, file_path2, format_name="stylish"):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    match format_name:
        case "stylish":
            return '\n'.join(wrap_list(
                flatten_recursively(generate_comparison(file1, file2))
            ))
        case _:
            raise ValueError("unknown output format")
