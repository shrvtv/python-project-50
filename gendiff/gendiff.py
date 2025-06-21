import argparse
import json
import os

import yaml

import gendiff.utilities as utils

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


def add_change(value, change):
    if isinstance(value, dict):
        if change == 'modified':
            raise ValueError('Modified elements are processed by compare().')
        new_value = {}
        for key in value.keys():
            new_value[key] = add_change(value[key], 'unchanged')
        value = new_value
    elif isinstance(value, tuple):  # The value is modified
        first = add_change(value[0], 'removed')
        second = add_change(value[1], 'added')
        value = (first, second)
    return {
        'change': change,
        'value': value
    }


def compare(old, new, root=True):
    old = utils.protect_value(old, exception=missing)
    new = utils.protect_value(new, exception=missing)

    if old == new:
        return add_change(old, 'unchanged')
    elif old is missing and new:
        return add_change(new, 'added')
    elif new is missing and old:
        return add_change(old, 'removed')
    else:
        if isinstance(old, dict) and isinstance(new, dict):
            all_keys = set(old.keys()).union(set(new.keys()))
            result = {}
            for key in all_keys:
                result[key] = compare(
                    old.get(key, missing),
                    new.get(key, missing),
                    root=False
                )
            return result if root else {
                'change': 'modified',
                'value': result
            }
        return add_change((old, new), 'modified')


def render(element, key=None, level=0):
    change = element['change']
    value = element['value']
    if isinstance(value, tuple):
        removed, added = value
        return render(removed, key) + render(added, key)  # both are lists
    else:
        return [f"{level * '    '}{utils.CHANGE_SYNTAX[change]}{key}: {value}"]


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    comparison = compare(first, second)
    lines = []
    for k in sorted(comparison.keys()):
        lines.extend(render(comparison[k], k))
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
