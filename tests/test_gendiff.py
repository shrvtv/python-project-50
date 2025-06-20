from gendiff.gendiff import generate_diff


def test_generate_diff_flat_json():
    assert generate_diff(
        'tests/test_data/flat/json/file1.json',
        'tests/test_data/flat/json/file2.json'
    ) == open('tests/test_data/results/flat').read()


def test_generate_diff_flat_yaml():
    assert generate_diff(
        'tests/test_data/flat/yaml/file1.yml',
        'tests/test_data/flat/yaml/file2.yaml'
    ) == open('tests/test_data/results/flat').read()


def test_generate_diff_flat_mixed_format():
    assert generate_diff(
        'tests/test_data/flat/json/file1.json',
        'tests/test_data/flat/yaml/file2.yaml'
    ) == open('tests/test_data/results/flat').read()
