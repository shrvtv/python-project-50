from pathlib import Path

import gendiff.parser

MISSING = object()
INDENT = "    "
COMPARISON = {
    "no change": "    ",
        "added": "  + ",
      "removed": "  - "
}


def compare(key, value1, value2, indentation_level=0):
    indentation = indentation_level * INDENT

    def make_comparison_line(comparison_result, value):
        return f"{indentation}{COMPARISON[comparison_result]}{key}: {value}\n"

    if value1 is None:
        return make_comparison_line("added", value2)
    elif value2 is None:
        return make_comparison_line("removed", value1)
    elif value1 == value2:
        return make_comparison_line("no change", value1)
    else:  # value has changed
        return (
            make_comparison_line("removed", value1)
            + make_comparison_line("added", value2)
        )


def stylish(all_keys_sorted, parsed_file1, parsed_file2):
    comparisons = [
        compare(
            key,
            parsed_file1.get(key),
            parsed_file2.get(key)
        )
        for key in all_keys_sorted
    ]
    return ''.join(["{\n", *comparisons, "}"])


def generate_diff(file_path1, file_path2, format_name="stylish"):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    # merging and sorting all keys
    all_keys_sorted = sorted(file1.keys() | file2.keys())

    match format_name:
        case "stylish":
            return stylish(all_keys_sorted, file1, file2)
        case _:
            raise ValueError("unknown output format")
