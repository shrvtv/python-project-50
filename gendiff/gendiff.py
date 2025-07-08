import argparse
import json

import gendiff.utilities as utils
from gendiff.json import render as render_json
from gendiff.plain import render as render_plain
from gendiff.stylish import render as render_stylish


def generate_diff(file1, file2, mode='stylish'):
    old = utils.parse(file1)
    new = utils.parse(file2)
    if mode == 'stylish':
        lines = utils.flatten(['{', render_stylish(old, new), '}'])
        return utils.mimic_json('\n'.join(lines))
    elif mode == 'plain':
        lines = utils.flatten(render_plain(old, new))
        return utils.mimic_json('\n'.join(lines))
    elif mode == 'json':
        return json.dumps(render_json(old, new))
    else:
        raise ValueError('Unknown style selected')


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
