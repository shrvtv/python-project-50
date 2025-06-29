import argparse

import gendiff.render as render
import gendiff.utilities as utils

missing = object()


def compare(first, second, level=0):
    result = []
    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, missing)
        new = second.get(key, missing)
        if new is missing:
            result.extend(render.make('removed', key, old, level))
        elif old is missing:
            result.extend(render.make('added', key, new, level))
        elif old == new:
            result.extend(render.make('untouched', key, old, level))
        else:
            if isinstance(old, dict) and isinstance(new, dict):
                result.extend(render.make(
                    'updated_dict',
                    key,
                    compare(old, new, level + 1),
                    level
                ))
            else:
                result.extend(render.make('updated', key, (old, new), level))
    return result


def generate_diff(file1, file2, mode='stylish'):
    first = utils.parse(file1)
    second = utils.parse(file2)
    lines = compare(first, second)
    return render.render(mode, lines)


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
