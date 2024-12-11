import pytest

from pformat.pretty_formatter import PrettyFormatter

from icecream import ic


@pytest.mark.parametrize("data", ["string", 123, 3.14, b"bytes"])
def test_format_simple(data):
    sut = PrettyFormatter()

    assert sut(data) == str(data)
    assert sut.format(data) == str(data)
