from pathlib import Path

import gendiff.parser

MISSING = object()


def generate_diff(file_path1, file_path2):
    file1 = gendiff.parser.read_file(Path(file_path1))
    file2 = gendiff.parser.read_file(Path(file_path2))

    keys1 = list(file1.keys())
    all_keys_sorted = sorted(
        keys1 + [key for key in file2.keys() if key not in keys1]
    )
    diff = ""

    for key in all_keys_sorted:
        value1 = file1.get(key, MISSING)
        value1 = str(value1).lower() if isinstance(value1, bool) else value1
        value2 = file2.get(key, MISSING)
        value2 = str(value2).lower() if isinstance(value2, bool) else value2
        if value1 is not MISSING and value2 is MISSING:
            diff += f"  - {key}: {value1}\n"
        elif value1 is MISSING and value2 is not MISSING:
            diff += f"  + {key}: {value2}\n"
        else:  # both values exist
            if value1 == value2:
                diff += f"    {key}: {value1}\n"
            else:
                diff += f"  - {key}: {value1}\n"
                diff += f"  + {key}: {value2}\n"
    return "{\n" + diff + "}"  # diff lines end with \n
