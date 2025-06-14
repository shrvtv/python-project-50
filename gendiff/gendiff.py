import argparse
import json
import os

CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    '
}

def parse(filename):
    current_location = os.getcwd()
    path = os.path.join(current_location, filename)
    if filename.endswith('.json'):
        return json.load(open(path))
    else:
        raise ValueError('Not a JSON file.')


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    all_keys = sorted(first_keys.union(second_keys))
    comparison = []
    for key in all_keys:
        first_value, second_value = first.get(key), second.get(key)

        # Output mimics JSON for bools
        # True | TRUE -> true
        if isinstance(first_value, bool):
            first_value = str(first_value).lower()
        if isinstance(second_value, bool):
            second_value = str(second_value).lower()

        if key not in first_keys and key in second_keys:
            comparison.append((CHANGE_SYNTAX['added'], key, second_value))
        elif key in first_keys and key not in second_keys:
            comparison.append((CHANGE_SYNTAX['removed'], key, first_value))
        else:  # key is present in both files
            if first_value != second_value:
                comparison.append(
                    (CHANGE_SYNTAX['removed'], key, first_value)
                )
                comparison.append((CHANGE_SYNTAX['added'], key, second_value))
            else:
                comparison.append(
                    (CHANGE_SYNTAX['unchanged'], key, first_value)
                )
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

    print(generate_diff(args.first_file, args.second_file))


if __name__ == "__main__":
    main()
