from gendiff import generate_diff


def test_generate_diff_flat_json():
    assert generate_diff(  # JSON
        "tests/test_data/flat1.json",
        "tests/test_data/flat2.json"
    ) == open("tests/test_data/results/flat1_vs flat2.txt").read()


def test_generate_diff_flat_yaml():
    assert generate_diff(  # YAML
        "tests/test_data/flat1.yml",
        "tests/test_data/flat2.yml"
    ) == open("tests/test_data/results/flat1_vs flat2.txt").read()


# Output depends on file order
def test_generate_diff_flat_json_reversed():
    assert generate_diff(  # JSON
        "tests/test_data/flat2.json",
        "tests/test_data/flat1.json"
    ) == open("tests/test_data/results/flat2_vs_flat1.txt").read()


# Output depends on file order
def test_generate_diff_flat_yaml_reversed():
    assert generate_diff(  # YAML
        "tests/test_data/flat2.yml",
        "tests/test_data/flat1.yml"
    ) == open("tests/test_data/results/flat2_vs_flat1.txt").read()


def test_generate_diff_nested_json():
    assert generate_diff(  # JSON
        "tests/test_data/nested1.json",
        "tests/test_data/nested2.json"
    ) == open("tests/test_data/results/nested1_vs_nested2.txt").read()


def test_generate_diff_nested_yaml():
    assert generate_diff(  # YAML
        "tests/test_data/nested1.yml",
        "tests/test_data/nested2.yml"
    ) == open("tests/test_data/results/nested1_vs_nested2.txt").read()
