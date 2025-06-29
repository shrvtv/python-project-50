from gendiff.gendiff import generate_diff


def test_generate_diff_flat_json():
    assert generate_diff(
        'tests/test_data/flat/json/file1.json',
        'tests/test_data/flat/json/file2.json',
        'stylish'
    ) == open('tests/test_data/results/flat').read()


def test_generate_diff_flat_yaml():
    assert generate_diff(
        'tests/test_data/flat/yaml/file1.yml',
        'tests/test_data/flat/yaml/file2.yaml',
        'stylish'
    ) == open('tests/test_data/results/flat').read()


def test_generate_diff_flat_mixed():
    assert generate_diff(
        'tests/test_data/flat/json/file1.json',
        'tests/test_data/flat/yaml/file2.yaml',
        'stylish'
    ) == open('tests/test_data/results/flat').read()


def test_generate_diff_recursive_json():
    assert generate_diff(
        'tests/test_data/recursive/json/file1.json',
        'tests/test_data/recursive/json/file2.json',
        'stylish'
    ) == open('tests/test_data/results/stylish_recursive').read()


def test_generate_diff_recursive_yaml():
    assert generate_diff(
        'tests/test_data/recursive/yaml/file1.yml',
        'tests/test_data/recursive/yaml/file2.yaml',
        'stylish'
    ) == open('tests/test_data/results/stylish_recursive').read()


def test_generate_diff_recursive_mixed():
    assert generate_diff(
        'tests/test_data/recursive/json/file1.json',
        'tests/test_data/recursive/yaml/file2.yaml',
        'stylish'
    ) == open('tests/test_data/results/stylish_recursive').read()
