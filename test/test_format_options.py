from pformat.format_options import FormatOptions


def test_default():
    assert FormatOptions.default("width") == 80
    assert FormatOptions.default("indent_width") == 4
    assert FormatOptions.default("compact") == False
    assert FormatOptions.default("projections") is None
