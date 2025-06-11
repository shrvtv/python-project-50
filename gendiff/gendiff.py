import argparse
import os
import json


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

    current_location = os.getcwd()
    first_path = os.path.join(current_location, args.first_file)
    second_path = os.path.join(current_location, args.second_file)

    first_parsed = json.load(open(first_path))
    second_parsed = json.load(open(second_path))

if __name__ == "__main__":
    main()
