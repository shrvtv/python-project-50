import argparse
import json

import gendiff.diff as diff
import gendiff.renderers.plain as plain
import gendiff.renderers.stylish as stylish
import gendiff.utilities as utils


def generate_diff(file1, file2, mode='stylish'):
    old = utils.parse(file1)
    new = utils.parse(file2)
    comparison = diff.compare(old, new)
    if mode == 'json':
        return json.dumps(comparison, sort_keys=True)
    if mode == 'stylish':
        lines = utils.flatten(['{', stylish.render(old, new), '}'])
    elif mode == 'plain':
        lines = plain.render(comparison)
    else:
        raise ValueError('Unknown style selected')
    return utils.mimic_json('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument(
        "-f", "--format",
        help="set format of output",
        default="stylish"
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")

    args = parser.parse_args()

    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main()
