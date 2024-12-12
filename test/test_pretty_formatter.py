import pytest

from pformat.indentation import add_indent
from pformat.pretty_formatter import INDENT_WIDTH, IterableFormatter, PrettyFormatter

SIMPLE_DATA = [123, 3.14, "string", b"bytes"]


class TestPrettyFormatterSimple:
    @pytest.fixture
    def sut(self):
        return PrettyFormatter()

    @pytest.mark.parametrize("data", SIMPLE_DATA)
    def test_format_single_element(self, sut, data):
        assert sut(data) == repr(data)
        assert sut.format(data) == repr(data)

    @pytest.mark.parametrize("iterable_type", [list, set, frozenset, tuple])
    def test_format_iterable(self, sut, iterable_type):
        collection = iterable_type(SIMPLE_DATA)

        opening, closing = IterableFormatter.get_parens(collection)
        expected_output = "\n".join(
            [opening, *[f"{add_indent(sut(item), INDENT_WIDTH)}," for item in collection], closing]
        )

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output
