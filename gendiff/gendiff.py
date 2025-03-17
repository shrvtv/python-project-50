from pathlib import Path

import gendiff.parser

MISSING = object()


def compare(key, value1, value2):
    if value1 is MISSING:     # new key
        return f"  + {key}: {value2}\n"
    elif value2 is MISSING:   # key removed
        return f"  - {key}: {value1}\n"
    else:                     # both values exist
        if value1 == value2:  # value didn't change
            return f"    {key}: {value1}\n"
        else:                 # value has been changed
            return (
                f"  - {key}: {value1}\n"
              + f"  + {key}: {value2}\n"
            )    


def generate_diff(file_path1, file_path2):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    # merging and sorting all keys
    all_keys_sorted = sorted(file1.keys() | file2.keys())

    comparisons = [
        compare(key, file1.get(key, MISSING), file2.get(key, MISSING))
        for key in all_keys_sorted
    ]

    return ''.join(["{\n", *comparisons, "}"])
