from __future__ import annotations

from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any

from .formatter_types import MultilineFormatter, NormalFormatter, TypeSpecificFormatter
from .indentation import add_indent, add_indents

TypeSpecificFormatterMapping = Mapping[type, TypeSpecificFormatter]

INDENT_WIDTH = 4


class PrettyFormatter:
    def __init__(self):
        self._default_formatter = DefaultFormatter()

        self._formatters = OrderedDict(
            [
                (str, self._default_formatter),
                (bytes, self._default_formatter),
                (Mapping, MappingFormatter(self)),
                (Iterable, IterableFormatter(self)),
            ]
        )

    def __call__(self, obj: Any, depth: int = 0) -> str:
        return "\n".join(self._format_impl(obj, depth))

    def format(self, obj: Any, depth: int = 0) -> str:
        return "\n".join(self._format_impl(obj, depth))

    def _format_impl(self, obj: Any, depth: int = 0) -> list[str]:
        for t, formatter in self._formatters.items():
            if isinstance(obj, t):
                return self._run_formatter(obj, formatter, depth)

        return self._run_formatter(obj, self._default_formatter, depth)

    def _run_formatter(
        self, obj: Any, formatter: TypeSpecificFormatter, depth: int = 0
    ) -> list[str]:
        if isinstance(formatter, MultilineFormatter):
            return formatter(obj)

        return [formatter(obj)]


class DefaultFormatter(NormalFormatter):
    def __call__(self, obj: Any, depth: int = 0) -> str:
        return add_indent(str(obj), INDENT_WIDTH, depth)


class IterableFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter

    def __call__(self, collection: Iterable, depth: int = 0) -> list[str]:
        opening, closing = self._get_parens(collection)

        values = list()
        for value in collection:
            values.extend(self._base_formatter._format_impl(value))

        values_fmt = add_indents(values, INDENT_WIDTH, 1)
        return add_indents([opening, *values_fmt, closing], INDENT_WIDTH, depth)

    def _get_parens(self, collection: Iterable) -> tuple[str, str]:
        if isinstance(collection, list):
            return "[", "]"
        if isinstance(collection, set):
            return "{", "}"
        if isinstance(collection, frozenset):
            return "frozen{", "}"
        if isinstance(collection, tuple) or isinstance(collection, range):
            return "(", ")"
        return "![", "]!"


class MappingFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter

    def __call__(self, mapping: Mapping, depth: int = 0) -> list[str]:
        values = list()
        for key, value in mapping.items():
            item_values_fmt = self._base_formatter._format_impl(value)
            item_values_fmt[0] = f"{key}: {item_values_fmt[0]}"
            values.extend(item_values_fmt)

        values_fmt = add_indents(values, INDENT_WIDTH, 1)
        return add_indents(["{", *values_fmt, "}"], INDENT_WIDTH, depth)


if __name__ == "__main__":
    from icecream import ic
    # data = load_data(Path.cwd().parent / "data/simple_list.pkl")

    def separate():
        print("\n" + ("-" * 50))

    fmt = PrettyFormatter()

    separate()

    simple_list = [1, 2, "string", b"bytes", [3, 4, "string2", b"bytes2"]]
    ic(simple_list)
    print(fmt(simple_list))

    separate()

    simple_dict = {"key1": 1, "key2": 2, "key3": 3, "key4": {"key5": 5, "key6": 6}}
    ic(simple_dict)
    print(fmt(simple_dict))

    separate()

    complex_list = [
        1,
        2,
        {"key3": 3, "key4": {"key5": 5, "key6": 6}},
        {8, 7},
        frozenset({9, 10}),
        (11, 12),
        "string",
        b"f\xcd\x11",
    ]

    ic(complex_list)
    print(fmt(complex_list))
