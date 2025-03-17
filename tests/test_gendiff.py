from gendiff import generate_diff


def test_generate_diff():
    assert generate_diff(  # JSON
        "tests/test_data/file1.json",
        "tests/test_data/file2.json"
    ) == open("tests/test_data/results/file1_vs_file2.txt").read()

    assert generate_diff(  # YAML
        "tests/test_data/file1.yml",
        "tests/test_data/file2.yml"
    ) == open("tests/test_data/results/file1_vs_file2.txt").read()


def test_generate_diff_reversed():
    # Output depends on file order
    assert generate_diff(  # JSON
        "tests/test_data/file2.json",
        "tests/test_data/file1.json"
    ) == open("tests/test_data/results/file2_vs_file1.txt").read()

    assert generate_diff(  # YAML
        "tests/test_data/file2.yml",
        "tests/test_data/file1.yml"
    ) == open("tests/test_data/results/file2_vs_file1.txt").read()
