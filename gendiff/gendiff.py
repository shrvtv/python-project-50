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


def compare(old, new):
    old = utils.protect_value(old, exception=missing)
    new = utils.protect_value(new, exception=missing)

    if old == new:
        return {
            'change': 'unchanged',
            'value': old
        }
    elif old is missing and new:
        return {
            'change': 'added',
            'value': new
        }
    elif new is missing and old:
        return {
            'change': 'removed',
            'value': old
        }
    else:
        return {
            'change': 'modified',
            'value': (old, new)
        }


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    lines = []
    all_keys = set(first.keys()).union(set(second.keys()))
    for key in sorted(all_keys):
        comparison = compare(first.get(key, missing), second.get(key, missing))
        change, value = comparison['change'], comparison['value']
        if comparison['change'] != 'modified':
            lines.append(utils.make_line(change, key, value))
        else:
            lines.append(utils.make_line('removed', key, value[0]))
            lines.append(utils.make_line('added', key, value[1]))
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
