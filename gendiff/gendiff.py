import argparse

import gendiff.render as render
import gendiff.utilities as utils


def add_change(change, value):
    return {
        'change': change,
        'value': value
    }


def compare(old, new):
    old = utils.protect_value(old)
    new = utils.protect_value(new)

    if old == new:
        return add_change('untouched', old)
    if new is utils.missing:
        return add_change('removed', old)
    if old is utils.missing:
        return add_change('added', new)

    if isinstance(old, dict) and isinstance(new, dict):
        diff = {}
        for key in old.keys() | new.keys():
            diff[key] = compare(
                old.get(key, utils.missing), new.get(key, utils.missing)
            )
        return add_change('updated', diff)
    else:
        return add_change('updated', (old, new))


def generate_diff(file1, file2, mode='stylish'):
    first = utils.parse(file1)
    second = utils.parse(file2)
    lines = render.render(mode, compare(first, second))
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
