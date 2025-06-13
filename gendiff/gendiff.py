import argparse
import os
import json


CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    '
}


def generate_diff(first, second):
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    all_keys = sorted(first_keys.union(second_keys))
    comparison = []
    for key in all_keys:
        first_value, second_value = first.get(key), second.get(key)
        if key not in first_keys and key in second_keys:
            comparison.append((CHANGE_SYNTAX['added'], key, second_value))
        elif key in first_keys and key not in second_keys:
            comparison.append((CHANGE_SYNTAX['removed'], key, first_value))
        else:  # key is present in both files
            if first_value != second_value:
                comparison.append((CHANGE_SYNTAX['removed'], key, first_value))
                comparison.append((CHANGE_SYNTAX['added'], key, second_value))
            else:
                comparison.append((CHANGE_SYNTAX['unchanged'], key, first_value))
    lines = [f"{prefix}{key}: {value}" for prefix, key, value in comparison]
    return '\n'.join(('{', *lines, '}'))


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument(
        "-f", "--format",
        help="set format of output"
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")

    args = parser.parse_args()

    current_location = os.getcwd()
    first_path = os.path.join(current_location, args.first_file)
    second_path = os.path.join(current_location, args.second_file)

    first_parsed = json.load(open(first_path))
    second_parsed = json.load(open(second_path))

    result = {}
    return result

if __name__ == "__main__":
    main()
