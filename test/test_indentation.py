from itertools import product

import pytest

from pformat.indentation import (
    DEFAULT_INDENT_CHARACTER,
    add_indent,
    add_indents,
    indent_size,
    indent_str,
)

INDENT_WIDTH_VALS = [1, 2, 3, 4]
DEPTH_VASL = [0, 1, 2, 3]


def indentation_test_params():
    return "indent_width,depth", product(INDENT_WIDTH_VALS, DEPTH_VASL)


@pytest.mark.parametrize(*indentation_test_params())
def test_indent_size(indent_width: int, depth: int):
    assert indent_size(indent_width, depth) == indent_width * depth


@pytest.mark.parametrize(*indentation_test_params())
def test_indent_str(indent_width: int, depth: int):
    assert indent_str(indent_width, depth) == DEFAULT_INDENT_CHARACTER * indent_size(
        indent_width, depth
    )


@pytest.fixture
def dummy_str() -> str:
    return "string"


@pytest.mark.parametrize("indent_width", INDENT_WIDTH_VALS)
def test_add_indent_default_depth(indent_width: int, dummy_str):
    assert (
        add_indent(dummy_str, indent_width)
        == f"{DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth=1)}{dummy_str}"
    )


@pytest.mark.parametrize(*indentation_test_params())
def test_add_indent(indent_width: int, depth: int, dummy_str):
    assert (
        add_indent(dummy_str, indent_width, depth)
        == f"{DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth)}{dummy_str}"
    )


@pytest.mark.parametrize(*indentation_test_params())
def test_add_indents_for_empty_list(indent_width: int, depth: int):
    assert len(add_indents(list(), indent_width, depth)) == 0


@pytest.mark.parametrize("indent_width", INDENT_WIDTH_VALS)
def test_add_indents_default_depth(indent_width: int, dummy_str):
    assert all(
        s_out == f"{DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth=1)}{dummy_str}"
        for s_out in add_indents([dummy_str for _ in range(5)], indent_width)
    )


@pytest.mark.parametrize(*indentation_test_params())
def test_add_indents(indent_width: int, depth: int, dummy_str):
    assert all(
        s_out == f"{DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth)}{dummy_str}"
        for s_out in add_indents([dummy_str for _ in range(5)], indent_width, depth)
    )
