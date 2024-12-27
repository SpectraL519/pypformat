from dataclasses import asdict, fields

from pformat.format_options import FormatOptions
from pformat.indentation_utility import IndentType
from pformat.text_style import TextStyle


def test_default():
    assert FormatOptions.default("compact") == False
    assert FormatOptions.default("width") == 50
    assert FormatOptions.default("indent_type") == IndentType.NONE()
    assert FormatOptions.default("text_style") == TextStyle()
    assert FormatOptions.default("style_entire_text") == False
    assert FormatOptions.default("exact_type_matching") == False
    assert FormatOptions.default("projections") is None
    assert FormatOptions.default("formatters") is None


def test_init_with_none_text_style():
    sut = FormatOptions(text_style=None)
    assert sut.text_style == TextStyle()


def test_asdict_shallow():
    sut = FormatOptions()
    assert sut.asdict() == sut.asdict(shallow=True)

    expected_dict = {field.name: getattr(sut, field.name) for field in fields(sut)}
    assert sut.asdict() == expected_dict


def test_asdict_deep():
    sut = FormatOptions()
    assert sut.asdict(shallow=False) == asdict(sut)
