import argparse
import json

import gendiff.render as render
import gendiff.utilities as utils

missing = object()


def stylish(first, second, level=0):
    result = []
    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, missing)
        new = second.get(key, missing)
        if new is missing:
            result.extend(render.make_stylish('removed', key, old, level))
        elif old is missing:
            result.extend(render.make_stylish('added', key, new, level))
        elif old == new:
            result.extend(render.make_stylish('untouched', key, old, level))
        else:
            if isinstance(old, dict) and isinstance(new, dict):
                result.extend(render.make_stylish(
                    'updated_dict',
                    key,
                    stylish(old, new, level + 1),
                    level
                ))
            else:
                result.extend(render.make_stylish(
                    'updated',
                    key,
                    (old, new),
                    level
                ))
    return result


def plain(first, second, location=''):
    def locate(k):
        if location == '':
            return k
        return location + '.' + k

    result = []
    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, missing)
        new = second.get(key, missing)
        if new is missing:
            result.append(render.make_plain('removed', locate(key), old))
        elif old is missing:
            result.append(render.make_plain('added', locate(key), new))
        elif old != new:
            if isinstance(old, dict) and isinstance(new, dict):
                result.extend(plain(old, new, locate(key)))
            else:
                result.append(render.make_plain(
                    'updated', locate(key), (old, new)
                ))
    return result


def jsonify(first, second):
    result = {}
    for key in sorted(first.keys() | second.keys()):
        old, new = first.get(key, missing), second.get(key, missing)
        if isinstance(old, dict) and isinstance(new, dict):
            result[key] = {
                'change': 'updated',
                'value': jsonify(old, new)
            }
        else:
            if old is missing:
                result[key] = {
                    'change': 'added',
                    'value': new
                }
            elif new is missing:
                result[key] = {
                    'change': 'removed',
                    'value': old
                }
            elif old == new:
                result[key] = {
                    'change': 'untouched',
                    'value': old
                }
            else:
                result[key] = {
                    'change': 'updated',
                    'old_value': old,
                    'new_value': new
                }
    return result


def generate_diff(file1, file2, mode):
    old = utils.parse(file1)
    new = utils.parse(file2)
    if mode == 'stylish':
        lines = utils.flatten(['{', stylish(old, new), '}'])
        return utils.mimic_json('\n'.join(lines))
    elif mode == 'plain':
        lines = utils.flatten(plain(old, new))
        return utils.mimic_json('\n'.join(lines))
    elif mode == 'json':
        return json.dumps(jsonify(old, new))
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

    print(generate_diff(args.format, args.first_file, args.second_file))


if __name__ == "__main__":
    main()
