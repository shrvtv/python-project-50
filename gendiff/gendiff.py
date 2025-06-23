import argparse

import gendiff.render as render
import gendiff.utilities as utils

missing = object()


def add_change(change, value, new_value=None):
    if change == 'modified':
        if new_value is None:
            raise ValueError('Value is modified, but only old provided')
        return {
            'change': change,
            'old': value,
            'new': new_value
        }

    if isinstance(value, dict):
        result = {}
        for key in value.keys():
            result[key] = add_change('unchanged',
                # Since these elements weren't protected by compare()
                # they have to be protected here manually.
                utils.protect_value(value[key], missing)
            )
        return {
        'change': change,
        'value': result
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
            'change': 'modified_dict',
            'value': result
        }
    if old is missing and new:
        return add_change('added', new)
    elif new is missing and old:
        return add_change('removed', old)
    else:
        return add_change('modified', old, new)


def generate_diff(file1, file2, format='stylish'):
    first = utils.parse(file1)
    second = utils.parse(file2)
    if format == 'stylish':
        lines = render.stylish(compare(first, second))
    else:
        lines = []

    return utils.mimic_json('\n'.join(lines))


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

    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main()
