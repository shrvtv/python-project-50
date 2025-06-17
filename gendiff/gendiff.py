import argparse
import json
import os

import yaml

import gendiff.utilities as utils

CHANGE_SYNTAX = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    '
}

missing = object()


def parse(filename):
    current_location = os.getcwd()
    path = os.path.join(current_location, filename)
    file = open(path)
    if filename.endswith('.json'):
        return json.load(file)
    elif filename.endswith('.yaml') or filename.endswith('.yml'):
        return yaml.safe_load(file)
    else:
        raise ValueError('Invalid file type')


def compare(first, second):
    if isinstance(first, dict) and isinstance(second, dict):
        comparison = {}
        first_keys = set(first.keys())
        second_keys = set(second.keys())
        for key in first_keys.union(second_keys):
            first_value = first.get(key, missing)
            second_value = second.get(key, missing)
            comparison[key] = compare(first_value, second_value)
        return comparison

    first = utils.protect_value(value=first, exception=missing)
    second = utils.protect_value(value=second, exception=missing)
    if first is missing and second:
        change_type = 'added'
        value = second
    elif second is missing and first:
        change_type = 'removed'
        value = first
    else:  # key is present in both files
        if first == second:
            change_type = 'unchanged'
            value = first
        else:
            change_type = 'modified'
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
    comparison = compare(first, second)
    lines = []
    for key in sorted(comparison.keys()):
        element = comparison[key]
        change_type, value = element['change_type'], element['value']
        if change_type == 'modified':  # in this case a dict is returned
            lines.extend([
                utils.make_line(CHANGE_SYNTAX['removed'], key, value['old']),
                utils.make_line(CHANGE_SYNTAX['added'], key, value['new'])
            ])
        else:
            lines.append(
                utils.make_line(CHANGE_SYNTAX[change_type], key, value)
            )

    return utils.mimic_json('\n'.join(('{', *lines, '}')))


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
