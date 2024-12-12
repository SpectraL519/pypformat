from dataclasses import field

from pformat.format_options import FormatOptions


def test_default():
    assert FormatOptions.default("width") == 80
    assert FormatOptions.default("indent_width") == 4
    assert FormatOptions.default("compact") == False

    # Dummy field with a default factory
    list_field = "list"
    FormatOptions.__dataclass_fields__[list_field] = field(default_factory=list)
    assert FormatOptions.default(list_field) == list()
