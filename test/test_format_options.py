from dataclasses import asdict, fields

from pformat.format_options import FormatOptions
from pformat.indentation_utility import IndentType


def test_asdict_shallow():
    sut = FormatOptions()
    assert sut.asdict() == sut.asdict(shallow=True)

    expected_dict = {field.name: getattr(sut, field.name) for field in fields(sut)}
    assert sut.asdict() == expected_dict


def test_asdict_deep():
    sut = FormatOptions()
    assert sut.asdict(shallow=False) == asdict(sut)


def test_default():
    assert FormatOptions.default("width") == 80
    assert FormatOptions.default("indent_type") == IndentType.NONE()
    assert FormatOptions.default("compact") == False
    assert FormatOptions.default("projections") is None
    assert FormatOptions.default("formatters") is None
