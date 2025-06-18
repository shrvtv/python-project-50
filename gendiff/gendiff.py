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


def compare(first, second, location=''):
    if isinstance(first, dict) and isinstance(second, dict):
        change = 'unchanged' if first == second else 'modified'
        comparison = {}
        first_keys = set(first.keys())
        second_keys = set(second.keys())
        for key in first_keys.union(second_keys):
            first_value = first.get(key, missing)
            second_value = second.get(key, missing)
            comparison[key] = compare(
                first_value,
                second_value,
                utils.make_location(location, key)
            )
        return {
            'type': 'node',
            'path': location,
            'change': change,
            'value': comparison
        }

    first = utils.protect_value(value=first, exception=missing)
    second = utils.protect_value(value=second, exception=missing)
    if first is missing and second:
        change = 'added'
        value = second
    elif second is missing and first:
        change = 'removed'
        value = first
    else:  # key is present in both files
        if first == second:
            change = 'unchanged'
            value = first
        else:
            change = 'modified'
            value = {
                'old': first,
                'new': second
            }
    return {
        'type': 'leaf',
        'path': location,
        'change': change,
        'value': value
    }


def render_tree(tree):
    lines = []
    for key in sorted(tree['value'].keys()):
        element = tree['value'][key]
        level = element['path'].count('.')
        change_type, value = element['change'], element['value']
        if element['type'] == 'node':
            pass
        else:
            if change_type == 'modified':  # in this case a dict is returned
                lines.extend([
                    utils.make_line(
                        CHANGE_SYNTAX['removed'], key, value['old'], level
                    ),
                    utils.make_line(
                        CHANGE_SYNTAX['added'], key, value['new'], level
                    )
                ])
            else:
                lines.append(
                    utils.make_line(
                        CHANGE_SYNTAX[change_type], key, value, level
                    )
                )

    return utils.mimic_json('\n'.join(('{', *lines, '}')))


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    comparison = compare(first, second)
    return render_tree(comparison)


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
