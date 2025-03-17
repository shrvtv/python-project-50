from pathlib import Path

import gendiff.parser

MISSING = object()


def compare(key, value1, value2):
    if value1 is not MISSING and value2 is MISSING:
        return f"  - {key}: {value1}\n"
    elif value1 is MISSING and value2 is not MISSING:
        return f"  + {key}: {value2}\n"
    else:  # both values exist
        if value1 == value2:
            return f"    {key}: {value1}\n"
        else:
            return (
                f"  - {key}: {value1}\n"
              + f"  + {key}: {value2}\n"
            )    


def generate_diff(file_path1, file_path2):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    keys1 = list(file1.keys())
    all_keys_sorted = sorted(
        keys1 + [key for key in file2.keys() if key not in keys1]
    )
    comparisons = [
        compare(key, file1.get(key, MISSING), file2.get(key, MISSING))
        for key in all_keys_sorted
    ]
    return ''.join(["{\n", *comparisons, "}"])  # diff lines end with \n
