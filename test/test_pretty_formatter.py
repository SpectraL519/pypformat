from collections import deque
from collections.abc import Iterable, Mapping
from itertools import product

import pytest
from colored import Back, Fore, Style

from pformat.format_options import FormatOptions
from pformat.formatter_types import normal_formatter
from pformat.indentation_utility import IndentType
from pformat.pretty_formatter import IterableFormatter, MappingFormatter, PrettyFormatter
from pformat.text_style import TextStyle


class TestPrettyFormatterInitialization:
    def test_default_init(self):
        "Should be initialized with the default format options"

        sut = PrettyFormatter()
        assert sut._options == FormatOptions()

        sut_new = PrettyFormatter.new()
        assert sut_new._options == FormatOptions()

    def test_custom_init(self):
        custom_options = FormatOptions(width=100, compact=True, indent_type=IndentType.DOTS())

        sut = PrettyFormatter(custom_options)
        assert sut._options == custom_options

        sut_new = PrettyFormatter.new(**custom_options.asdict())
        assert sut_new._options == custom_options


def gen_mapping(data: Iterable) -> dict:
    return {f"key{i}": value for i, value in enumerate(data)}


SIMPLE_DATA = [123, 3.14, "string", b"bytes", bytearray([1, 2, 3])]
SIMPLE_HASHABLE_DATA = [data for data in SIMPLE_DATA if data.__hash__ is not None]
INDENT_WIDTH_VALS = [2, 4]
INDENT_TYPE_VALS = [
    gen(width=w)
    for gen, w in product([IndentType.NONE, IndentType.DOTS, IndentType.LINE], INDENT_WIDTH_VALS)
]
RECOGNIZABLE_ITERABLE_TYPES = [list, set, frozenset, tuple, deque]
RECOGNIZABLE_NHASH_ITERABLE_TYPES = [list, tuple, deque]


class DummyIterable:
    def __init__(self, nested: bool = False):
        if nested:
            self.data = [*SIMPLE_HASHABLE_DATA, DummyIterable()]
        else:
            self.data = SIMPLE_HASHABLE_DATA

    def __iter__(self):
        yield from self.data


class TestPrettyFormatterSimple:
    @pytest.fixture(params=INDENT_TYPE_VALS, ids=[f"indent_type={it}" for it in INDENT_TYPE_VALS])
    def sut(self, request: pytest.FixtureRequest) -> PrettyFormatter:
        self.indent_type = request.param
        return PrettyFormatter.new(indent_type=self.indent_type)

    @pytest.mark.parametrize(
        "element", SIMPLE_DATA, ids=[f"element={repr(v)}" for v in SIMPLE_DATA]
    )
    def test_format_single_element(self, sut: PrettyFormatter, element):
        assert sut(element) == repr(element)
        assert sut.format(element) == repr(element)

    @pytest.mark.parametrize("iterable_type", RECOGNIZABLE_ITERABLE_TYPES)
    def test_format_iterable(self, sut: PrettyFormatter, iterable_type: type):
        collection = iterable_type(SIMPLE_HASHABLE_DATA)
        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = "\n".join(
            [
                opening,
                *[f"{self.indent_type.add_to(repr(item))}," for item in collection],
                closing,
            ]
        )

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_unrecognized_iterable(self, sut):
        collection = DummyIterable()
        expected_output = "\n".join(
            [
                "DummyIterable(",
                *[f"{self.indent_type.add_to(repr(item))}," for item in collection],
                ")",
            ]
        )

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_mapping(self, sut):
        mapping = gen_mapping(SIMPLE_DATA)

        expected_output = list()
        for key, value in mapping.items():
            expected_output.append(self.indent_type.add_to(f"{repr(key)}: {repr(value)},"))
        expected_output = "\n".join(["{", *expected_output, "}"])

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


class TestPrettyFormatterForNestedStructures:
    @pytest.fixture(params=INDENT_TYPE_VALS, ids=[f"indent_type={it}" for it in INDENT_TYPE_VALS])
    def sut(self, request: pytest.FixtureRequest) -> PrettyFormatter:
        self.indent_type = request.param
        return PrettyFormatter.new(indent_type=self.indent_type)

    @pytest.mark.parametrize("iterable_type", RECOGNIZABLE_NHASH_ITERABLE_TYPES)
    def test_format_nested_iterable(self, sut: PrettyFormatter, iterable_type: type):
        collection = iterable_type([*SIMPLE_DATA, iterable_type(SIMPLE_DATA)])

        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = [f"{self.indent_type.add_to(repr(item))}," for item in SIMPLE_DATA]
        expected_output.extend(
            [
                self.indent_type.add_to(opening),
                *[f"{self.indent_type.add_to(repr(item), depth=2)}," for item in SIMPLE_DATA],
                self.indent_type.add_to(f"{closing},"),
            ]
        )
        expected_output = "\n".join([opening, *expected_output, closing])

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_nested_unrecognized_iterable(self, sut):
        collection = DummyIterable(nested=True)
        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = [
            f"{self.indent_type.add_to(repr(item))}," for item in SIMPLE_HASHABLE_DATA
        ]
        expected_output.extend(
            [
                self.indent_type.add_to(opening),
                *[
                    f"{self.indent_type.add_to(repr(item), depth=2)},"
                    for item in SIMPLE_HASHABLE_DATA
                ],
                self.indent_type.add_to(f"{closing},"),
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
                self.indent_type.add_to(f"{repr(key)}: {repr(value)},")
            )

        expected_nested_mapping_output = [
            f"{repr(nested_key)}: {{",
            *expected_simple_mapping_output,
            "},",
        ]
        expected_output = "\n".join(
            [
                "{",
                *expected_simple_mapping_output,
                *self.indent_type.add_to_each(expected_nested_mapping_output),
                "}",
            ]
        )

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


class TestPrettyFormatterCompact:
    @pytest.fixture
    def sut(self) -> PrettyFormatter:
        return PrettyFormatter.new(
            compact=True,
            width=None,
        )

    @pytest.mark.parametrize("iterable_type", RECOGNIZABLE_ITERABLE_TYPES)
    def test_format_iterable(self, sut: PrettyFormatter, iterable_type: type):
        collection = iterable_type(SIMPLE_HASHABLE_DATA)

        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = opening + ", ".join(repr(value) for value in collection) + closing

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_unrecognized_iterable(self, sut: PrettyFormatter):
        collection = DummyIterable()
        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = opening + ", ".join(repr(value) for value in collection) + closing

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_mapping(self, sut: PrettyFormatter):
        mapping = gen_mapping(SIMPLE_DATA)
        expected_output = (
            "{" + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in mapping.items()) + "}"
        )

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


class TestPrettyFormatterCompactForNestedIterableTypes:
    @pytest.fixture
    def sut(self) -> PrettyFormatter:
        self.indent_type = FormatOptions.default("indent_type")
        return PrettyFormatter.new(
            compact=True,
            width=60,
        )

    @pytest.mark.parametrize("iterable_type", RECOGNIZABLE_NHASH_ITERABLE_TYPES)
    def test_format_nested_iterable(self, sut: PrettyFormatter, iterable_type: type):
        collection = iterable_type([*SIMPLE_HASHABLE_DATA, iterable_type(SIMPLE_HASHABLE_DATA)])
        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = [f"{self.indent_type.add_to(sut(item))}," for item in collection]
        expected_output = "\n".join([opening, *expected_output, closing])

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output

    def test_format_nested_unrecognized_iterable(self, sut):
        collection = DummyIterable(nested=True)
        opening, closing = IterableFormatter.get_parens(collection)

        expected_output = [f"{self.indent_type.add_to(sut(item))}," for item in collection]
        expected_output = "\n".join([opening, *expected_output, closing])

        assert sut(collection) == expected_output
        assert sut.format(collection) == expected_output


class TestPrettyFormatterCompactForNestedMappingTypes:
    @pytest.fixture
    def sut(self) -> PrettyFormatter:
        self.indent_type = FormatOptions.default("indent_type")
        return PrettyFormatter.new(
            compact=True,
            width=80,
        )

    def test_format_nested_mapping(self, sut):
        mapping = gen_mapping(SIMPLE_HASHABLE_DATA)
        mapping["nested"] = gen_mapping(SIMPLE_HASHABLE_DATA)

        expected_output = list()
        for key, value in mapping.items():
            expected_output.append(self.indent_type.add_to(f"{sut(key)}: {sut(value)},"))
        expected_output = "\n".join(["{", *expected_output, "}"])

        assert sut(mapping) == expected_output
        assert sut.format(mapping) == expected_output


class TestPrettyFormatterStyleEntireText:
    COMPACT_VALS = [True, False]
    STYLE_VALS = [Fore.light_gray, Back.green, Style.bold]
    MODE_VALS = [TextStyle.Mode.normal, TextStyle.Mode.override, TextStyle.Mode.preserve]

    CSM_PARAMS = list(product(COMPACT_VALS, STYLE_VALS, MODE_VALS))
    CSM_IDS = [f"{compact=},{style=},{mode=}" for compact, style, mode in CSM_PARAMS]

    @pytest.fixture(autouse=True, params=CSM_PARAMS, ids=CSM_IDS)
    def sut(self, request: pytest.FixtureRequest) -> TextStyle:
        compact, style, mode = request.param
        self.text_style = TextStyle(style, mode)
        return PrettyFormatter.new(
            compact=compact, text_style=self.text_style, style_entire_text=True
        )

    def _is_str_styled(self, s: str) -> bool:
        return s.startswith(f"{Style.reset}{self.text_style.value}") and s.endswith(Style.reset)

    def test_is_output_styled_simple(self, sut: PrettyFormatter):
        assert all(self._is_str_styled(sut(item)) for item in SIMPLE_DATA)

    @pytest.mark.parametrize("iterable_type", RECOGNIZABLE_NHASH_ITERABLE_TYPES)
    def test_is_output_styled_nested_iterable(self, sut: PrettyFormatter, iterable_type: type):
        collection = iterable_type([*SIMPLE_HASHABLE_DATA, iterable_type(SIMPLE_HASHABLE_DATA)])

        formatted = sut(collection)
        formatted_lines = formatted.split("\n")

        assert all(self._is_str_styled(line) for line in formatted_lines)

    def test_is_output_styled_nested_mapping(self, sut: PrettyFormatter):
        mapping = gen_mapping(SIMPLE_HASHABLE_DATA)
        mapping["nested"] = gen_mapping(SIMPLE_HASHABLE_DATA)

        formatted = sut(mapping)
        formatted_lines = formatted.split("\n")

        assert all(self._is_str_styled(line) for line in formatted_lines)


class TestPrettyFormatterProjections:
    def test_format_projected_elements(self):
        float_proj = lambda f: int(f) + 1
        str_proj = lambda s: [ord(c) for c in s]

        sut = PrettyFormatter.new(
            compact=True,
            width=None,
            projections={
                float: float_proj,
                str: str_proj,
            },
        )

        f = 3.14
        assert float_proj(f) != f
        assert sut(f) != repr(f)
        assert sut(f) == repr(float_proj(f))
        assert sut.format(f) == repr(float_proj(f))

        s = "string"
        assert str_proj(s) != s
        assert sut(s) != repr(s)
        assert sut(s) == repr(str_proj(s))
        assert sut.format(s) == repr(str_proj(s))

    def test_format_projected_elements_with_no_matchin_projection(self):
        sut = PrettyFormatter.new(
            compact=True,
            width=None,
            projections=dict(),
        )

        f = 3.14
        assert sut(f) == repr(f)
        assert sut.format(f) == repr(f)


class TestPrettyFormatterCustomFormatters:
    def test_format_elements_with_overriden_formatters(self):
        base_types = [str, bytes, Iterable, Mapping]
        concrete_types = [str, bytes, list, dict]

        fmt_func = lambda x, depth: str(x)

        sut = PrettyFormatter.new(formatters=[normal_formatter(t, fmt_func) for t in base_types])

        assert all(sut(value) == fmt_func(value, depth=0) for t in concrete_types if (value := t()))

    def test_format_elements_with_custom_formatters(self):
        class DummyType:
            def __str__(self):
                return "DummyType.__str__()"

        custom_types = [int, float, DummyType]
        fmt_func = lambda x, depth: str(x)

        sut = PrettyFormatter.new(formatters=[normal_formatter(t, fmt_func) for t in custom_types])

        assert all(sut(value) == fmt_func(value, depth=0) for t in custom_types if (value := t()))

        default_type_values = ["string", b"bytes", [1, 2, 3], {"k1": 1, "k2": 2}]
        default_formatter = PrettyFormatter()

        assert all(sut(value) == default_formatter(value) for value in default_type_values)


class TestIterableFormatter:
    def test_init_default(self):
        fmt = PrettyFormatter.new()
        sut = IterableFormatter(fmt)

        assert sut.type is Iterable

    def test_init_with_strict_type_matching(self):
        fmt = PrettyFormatter.new(strict_type_matching=True)
        sut = IterableFormatter(fmt)

        assert sut.type is IterableFormatter._TYPES

    def test_get_parnens(self):
        assert IterableFormatter.get_parens(list()) == ("[", "]")
        assert IterableFormatter.get_parens(set()) == ("{", "}")
        assert IterableFormatter.get_parens(frozenset()) == ("frozen{", "}")
        assert IterableFormatter.get_parens(tuple()) == ("(", ")")
        assert IterableFormatter.get_parens(range(3)) == ("(", ")")
        assert IterableFormatter.get_parens(deque()) == ("deque([", "])")
        assert IterableFormatter.get_parens(DummyIterable()) == (f"{DummyIterable.__name__}(", ")")


class TestMappingFormatter:
    def test_init_default(self):
        fmt = PrettyFormatter.new()
        sut = MappingFormatter(fmt)

        assert sut.type is Mapping

    def test_init_with_strict_type_matching(self):
        fmt = PrettyFormatter.new(strict_type_matching=True)
        sut = MappingFormatter(fmt)

        assert sut.type is MappingFormatter._TYPES
