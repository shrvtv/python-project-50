from pathlib import Path

import gendiff.parser

MISSING = object()
INDENT = "    "
COMPARISON = {
    "no change": "    ",
        "added": "  + ",
      "removed": "  - "
}


def generate_comparison_line(key, value1, value2, indentation_level=0):
    """Generate a comparison output with the correct indentation.
    Returns a list of lines if given 2 dicts, otherwise return a single line
    """
    indentation = indentation_level * INDENT

    def make_line(comparison_result, value):
        return f"{indentation}{COMPARISON[comparison_result]}{key}: {value}\n"

    if value1 is None:
        return make_line("added", value2)
    elif value2 is None:
        return make_line("removed", value1)
    elif value1 == value2:
        return make_line("no change", value1)
    else:  # value has changed
        if isinstance(value1, dict) and isinstance(value2, dict):
            return stylish(value1, value2)
        else:
            return (
                make_line("removed", value1)
                + make_line("added", value2)
            )


def stylish(dict1, dict2):
    comparisons = [
        generate_comparison_line(key, dict1.get(key), dict2.get(key))
        # merging and sorting all keys before iterating over them
        for key in sorted(dict1.keys() | dict2.keys())
    ]
    return ''.join(["{\n", *comparisons, "}"])


def generate_diff(file_path1, file_path2, format_name="stylish"):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    match format_name:
        case "stylish":
            return stylish(file1, file2)
        case _:
            raise ValueError("unknown output format")
