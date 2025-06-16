import argparse
import json
import os

import yaml

EXCEPTIONS = (True, False)

CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    ',
    'changed': None
}


def parse(filename):
    current_location = os.getcwd()
    path = os.path.join(current_location, filename)
    if filename.endswith('.json'):
        return json.load(open(path))
    elif filename.endswith('.yaml') or filename.endswith('.yml'):
        return yaml.safe_load(open(path))
    else:
        raise ValueError('Invalid file type')


def make_line(change_type, key, value, level=0):
    return f"{level * '    '}{change_type}{key}: {value}"


def mimic_json(text):
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    text = text.replace('None', 'null')
    return text


def compare(first, second):
    if first in EXCEPTIONS:
        first = str(first)
    if second in EXCEPTIONS:
        second = str(second)

    if second and not first:
        change_type = CHANGE_SYNTAX['added']
        value = second
    elif first and not second:
        change_type = CHANGE_SYNTAX['removed']
        value = first
    else:  # key is present in both files
        if first == second:
            change_type = CHANGE_SYNTAX['unchanged']
            value = first
        else:
            change_type = CHANGE_SYNTAX['changed']
            value = {
                'old': first,
                'new': second
            }
    return {
        'change_type': change_type,
        'value': value
    }


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    comparison = {}
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    for key in first_keys.union(second_keys):
        first_value, second_value = first.get(key), second.get(key)
        comparison[key] = compare(first_value, second_value)

    lines = []
    for key in sorted(comparison.keys()):
        element = comparison[key]
        if not element['change_type'] == CHANGE_SYNTAX['changed']:
            lines.append(
                make_line(element['change_type'], key, element['value'])
            )
        else:
            lines.extend([
                make_line(
                    CHANGE_SYNTAX['removed'], key, element['value']['old']
                ),
                make_line(
                    CHANGE_SYNTAX['added'], key, element['value']['new']
                )
            ])

    return mimic_json('\n'.join(('{', *lines, '}')))


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
