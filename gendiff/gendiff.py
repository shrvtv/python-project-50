import json
from pathlib import Path


def read_file(filename):
    path_to_file = Path(filename)
    match path_to_file.suffix:
        case ".json":
            return json.load(open(path_to_file))
        case _:
            raise ValueError("Unsupported file type")


MISSING = object()


def generate_diff(file_path1, file_path2):
    file1 = read_file(file_path1)
    file2 = read_file(file_path2)
    keys1 = list(file1.keys())
    all_keys_sorted = sorted(keys1 + [key for key in file2.keys() if key not in keys1])
    diff = ""
    for key in all_keys_sorted:
        value1 = file1.get(key, MISSING)
        value2 = file2.get(key, MISSING)
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
