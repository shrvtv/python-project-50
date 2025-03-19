from gendiff import generate_diff


def test_generate_diff_JSON():
    assert generate_diff(  # JSON
        "tests/test_data/flat1.json",
        "tests/test_data/flat2.json"
    ) == open("tests/test_data/results/flat1_vs flat2.txt").read()


def test_generate_diff_YAML():
    assert generate_diff(  # YAML
        "tests/test_data/flat1.yml",
        "tests/test_data/flat2.yml"
    ) == open("tests/test_data/results/flat1_vs flat2.txt").read()


# Output depends on file order
def test_generate_diff_JSON_reversed():
    assert generate_diff(  # JSON
        "tests/test_data/flat2.json",
        "tests/test_data/flat1.json"
    ) == open("tests/test_data/results/flat2_vs_flat1.txt").read()


# Output depends on file order
def test_generate_diff_YAML_reversed():
    assert generate_diff(  # YAML
        "tests/test_data/flat2.yml",
        "tests/test_data/flat1.yml"
    ) == open("tests/test_data/results/flat2_vs_flat1.txt").read()
