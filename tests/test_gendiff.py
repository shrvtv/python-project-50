from gendiff.gendiff import generate_diff


def test_generate_diff_flat_json():
    assert generate_diff(
        'tests/test_data/file1.json',
        'tests/test_data/file2.json'
    ) == open('tests/test_data/file1_vs_file2').read()
