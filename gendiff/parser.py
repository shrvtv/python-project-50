import json

import yaml

QUOTATION_MARKS = ('\"', '\'')


def process_value(value):
    extracted_value = value.strip()
    if extracted_value.endswith(','):
        has_comma = True
        extracted_value = extracted_value[:-1]
    else:
        has_comma = False

    if not (
        extracted_value in "{}"
        or (
                extracted_value.startswith(QUOTATION_MARKS)
                and extracted_value.endswith(QUOTATION_MARKS)
        )
    ):
        extracted_value = f'"{extracted_value}"'
    return (extracted_value + ',') if has_comma else extracted_value


def process_file_string(file_string):
    splitted_pairs = file_string.split('\n')
    processed_pairs = []
    for pair in splitted_pairs:
        if ':' in pair:
            key, value = pair.split(':')
            processed_pairs.append(f"{key}: {process_value(value)}")
        else:
            processed_pairs.append(pair)
    return '\n'.join(processed_pairs)


def read_file(path_to_file):
    file_string = process_file_string(open(path_to_file).read())
    match path_to_file.suffix:
        case ".json":
            return json.loads(process_file_string(file_string))
        case ".yml" | ".yaml":
            return yaml.safe_load(process_file_string(file_string))
        case _:
            raise ValueError("Unsupported file type")
