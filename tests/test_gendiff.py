from gendiff.gendiff import generate_diff


def test_generate_diff_flat_json():
    assert generate_diff(
        'tests/test_data/flat/json/file1.json',
        'tests/test_data/flat/json/file2.json'
    ) == open('tests/test_data/results/flat').read()
