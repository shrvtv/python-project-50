import textwrap

from gendiff import generate_diff


def test_generate_diff():
    assert generate_diff(
        "tests/test_data/file1.json",
        "tests/test_data/file2.json"
    ) == textwrap.dedent('''\
        {
          - follow: false
            host: hexlet.io
          - proxy: 123.234.53.22
          - timeout: 50
          + timeout: 20
          + verbose: true
        }
    ''')
