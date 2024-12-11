import pytest

from itertools import product

from pformat.indentation_utility import indent_size, indent_str, DEFAULT_INDENT_CHARACTER

INDENT_WIDTH_VALS = [1, 2, 3, 4]
DEPTH_VASL = [0, 1, 2, 3]


@pytest.mark.parametrize("indent_width,depth", product(INDENT_WIDTH_VALS, DEPTH_VASL))
def test_indent_size(indent_width: int, depth: int):
    assert indent_size(indent_width, depth) == indent_width * depth


@pytest.mark.parametrize("indent_width,depth", product(INDENT_WIDTH_VALS, DEPTH_VASL))
def test_indent_str(indent_width: int, depth: int):
    assert indent_str(indent_width, depth) == DEFAULT_INDENT_CHARACTER * indent_size(
        indent_width, depth
    )
