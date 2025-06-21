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


def add_change(change, value, new_value=None):
    if change == 'modified':
        if new_value is None:
            raise ValueError('Value is modified, but only old provided')
        return {
            'change': change,
            'old': value,
            'new': new_value
        }
    return {
        'change': change,
        'value': value
    }


def compare(old, new):
    old = utils.protect_value(old, exception=missing)
    new = utils.protect_value(new, exception=missing)

    if old == new:
        return add_change('unchanged', old)

    if isinstance(old, dict) and isinstance(new, dict):
        result = {}
        for key in old.keys() | new.keys():
            result[key] = compare(old.get(key, missing), new.get(key, missing))
        return {
            'change': 'modified',
            'value': result
        }
    if old is missing and new:
        return add_change('added', new)
    elif new is missing and old:
        return add_change('removed', old)
    else:
        return add_change('modified', old, new)


def is_tree(node):
    return isinstance(node.get('value'), dict)


def is_leaf(node):
    return not is_tree(node)


def render(element, key=None):
    result = []
    change = element['change']
    if is_tree(element):
        children = element['value']
        for key in sorted(children.keys()):
            result.extend(render(children[key], key))
        return result
    else:
        if change == 'modified':
            old, new = element['old'], element['new']
            result.append(utils.make_line('removed', key, old))
            result.append(utils.make_line('added', key, new))
        else:
            value = element['value']
            result.append(utils.make_line(change, key, value))
        return result


def generate_diff(file1, file2):
    first = parse(file1)
    second = parse(file2)
    lines = render(compare(first, second))

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
