from collections import deque

import pytest

from pformat.indentation import add_indent
from pformat.pretty_formatter import INDENT_WIDTH, IterableFormatter, PrettyFormatter

SIMPLE_DATA = [123, 3.14, "string", b"bytes"]


class DummyIterable:
    def __init__(self, nested: bool = False):
        if nested:
            self.data = [*SIMPLE_DATA, DummyIterable()]
        else:
            self.data = SIMPLE_DATA

    def __iter__(self):
        yield from self.data


class TestPrettyFormatterSimple:
    @pytest.fixture
    def sut(self):
        return PrettyFormatter()

    @pytest.mark.parametrize("data", SIMPLE_DATA)
    def test_format_single_element(self, sut, data):
        assert sut(data) == repr(data)
        assert sut.format(data) == repr(data)

    @pytest.mark.parametrize("iterable_type", [list, set, frozenset, tuple, deque])
    def test_format_iterable(self, sut, iterable_type: type):
        collection = iterable_type(SIMPLE_DATA)

        opening, closing = IterableFormatter.get_parens(collection)
        assert (opening, closing) != ("![", "]!")

        expected_output = "\n".join(
            [opening, *[f"{add_indent(sut(item), INDENT_WIDTH)}," for item in collection], closing]
        )

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_unrecognized_iterable(self, sut):
        collection = DummyIterable()
        expected_output = "\n".join(
            ["![", *[f"{add_indent(sut(item), INDENT_WIDTH)}," for item in collection], "]!"]
        )

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_mapping(self, sut):
        mapping = {f"key{i}": value for i, value in enumerate(SIMPLE_DATA)}

        expected_output = list()
        for key, value in mapping.items():
            expected_output.append(add_indent(f"{sut(key)}: {sut(value)},", INDENT_WIDTH))
        expected_output = "\n".join(["{", *expected_output, "}"])

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


class TestPrettyFormatterNestedStructures:
    @pytest.fixture
    def sut(self):
        return PrettyFormatter()

    @pytest.mark.parametrize("iterable_type", [list, tuple, deque])
    def test_format_nested_iterable(self, sut, iterable_type: type):
        """
        Sets cannot have nested collections as its elements must be hashable
        """

        collection = iterable_type([*SIMPLE_DATA, iterable_type(SIMPLE_DATA)])

        opening, closing = IterableFormatter.get_parens(collection)
        assert (opening, closing) != ("![", "]!")

        expected_output = [f"{add_indent(sut(item), INDENT_WIDTH)}," for item in SIMPLE_DATA]
        expected_output.extend(
            [
                add_indent(opening, INDENT_WIDTH),
                *[f"{add_indent(sut(item), INDENT_WIDTH, depth=2)}," for item in SIMPLE_DATA],
                add_indent(f"{closing},", INDENT_WIDTH),
            ]
        )
        expected_output = "\n".join([opening, *expected_output, closing])

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_nested_unrecognized_iterable(self, sut):
        collection = DummyIterable(nested=True)

        opening, closing = IterableFormatter.get_parens(collection)
        assert (opening, closing) == ("![", "]!")

        expected_output = [f"{add_indent(sut(item), INDENT_WIDTH)}," for item in SIMPLE_DATA]
        expected_output.extend(
            [
                add_indent(opening, INDENT_WIDTH),
                *[f"{add_indent(sut(item), INDENT_WIDTH, depth=2)}," for item in SIMPLE_DATA],
                add_indent(f"{closing},", INDENT_WIDTH),
            ]
        )
        expected_output = "\n".join([opening, *expected_output, closing])

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output
