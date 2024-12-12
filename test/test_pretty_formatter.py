from collections import deque
from collections.abc import Iterable
from dataclasses import asdict

import pytest

from pformat.format_options import FormatOptions
from pformat.indentation import add_indent, add_indents
from pformat.pretty_formatter import IterableFormatter, PrettyFormatter

SIMPLE_DATA = [123, 3.14, "string", b"bytes"]
INDENT_WIDTH = FormatOptions.default("indent_width")


class TestPrettyFormatterInitialization:
    def test_default_init(self):
        "Should be initialized with the default format options"

        sut = PrettyFormatter()
        assert sut._options == FormatOptions()

        sut_new = PrettyFormatter.new()
        assert sut_new._options == FormatOptions()

    def test_custom_init(self):
        custom_options = FormatOptions(
            width=100,
            indent_width=3,
            compact=True,
        )

        sut = PrettyFormatter(custom_options)
        assert sut._options == custom_options

        sut_new = PrettyFormatter.new(**asdict(custom_options))
        assert sut_new._options == custom_options


def gen_mapping(data: Iterable) -> dict:
    return {f"key{i}": value for i, value in enumerate(data)}


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
        mapping = gen_mapping(SIMPLE_DATA)

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

    def test_format_nested_mapping(self, sut):
        mapping = gen_mapping(SIMPLE_DATA)
        nested_key = "nested"
        mapping[nested_key] = gen_mapping(SIMPLE_DATA)

        expected_simple_mapping_output = list()
        for key, value in gen_mapping(SIMPLE_DATA).items():
            expected_simple_mapping_output.append(
                add_indent(f"{sut(key)}: {sut(value)},", INDENT_WIDTH)
            )

        expected_nested_mapping_output = [
            f"{sut(nested_key)}: {{",
            *expected_simple_mapping_output,
            "},",
        ]
        expected_output = "\n".join(
            [
                "{",
                *expected_simple_mapping_output,
                *add_indents(expected_nested_mapping_output, INDENT_WIDTH),
                "}",
            ]
        )

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


def test_iterable_formatter_get_parnens():
    assert IterableFormatter.get_parens(list()) == ("[", "]")
    assert IterableFormatter.get_parens(set()) == ("{", "}")
    assert IterableFormatter.get_parens(frozenset()) == ("frozen{", "}")
    assert IterableFormatter.get_parens(tuple()) == ("(", ")")
    assert IterableFormatter.get_parens(range(3)) == ("(", ")")
    assert IterableFormatter.get_parens(deque()) == ("deque([", "])")
    assert IterableFormatter.get_parens(DummyIterable()) == ("![", "]!")
