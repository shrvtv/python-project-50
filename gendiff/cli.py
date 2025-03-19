import argparse

import gendiff.gendiff as gendiff


def cli():
    parser = argparse.ArgumentParser(
        description=(
            "Compares two configuration files and shows a difference."
        )
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f", "--format",
        type=str,
        default="stylish",
        help='set format of output (default: "stylish")'
    )
    arguments = parser.parse_args()
    print(
        gendiff.generate_diff(
            arguments.first_file,
            arguments.second_file,
            arguments.format
        )
    )
