from __future__ import annotations

from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any

from .formatter_types import MultilineFormatter, NormalFormatter, TypeSpecificFormatter
from .indentation_utility import add_indent

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
        return self._format_impl(obj, depth)

    def format(self, obj: Any, depth: int = 0) -> str:
        return self._format_impl(obj, depth)

    def _format_impl(self, obj: Any, depth: int = 0) -> str:
        for t, formatter in self._formatters.items():
            if isinstance(obj, t):
                return formatter(obj, depth)

        return self._default_formatter(obj, depth)

    # def _run_formatter(self, obj: Any, formatter: TypeSpecificFormatter, depth: int) -> str:
    #     if isinstance(formatter, MultilineFormatter):
    #         return "\n".join([add_indent(fmt, INDENT_WIDTH, depth) for fmt in formatter(obj)])

    #     return add_indent(formatter(obj), INDENT_WIDTH, depth)


class DefaultFormatter(NormalFormatter):
    def __call__(self, obj: Any, depth: int = 0) -> str:
        return str(obj)


class IterableFormatter(NormalFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter

    def __call__(self, collection: Iterable, depth: int = 0) -> list[str]:
        opening, closing = self._get_parens(collection)
        nested_depth = depth + 1

        values_fmt = [
            f"{add_indent(self._base_formatter(value, nested_depth), INDENT_WIDTH, nested_depth)},"
            for value in collection
        ]

        return "\n".join(
            [
                # add_indent(opening, INDENT_WIDTH, depth),
                opening,
                *values_fmt,
                add_indent(closing, INDENT_WIDTH, depth),
            ]
        )

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
        nested_depth = depth + 1

        values_fmt = [
            add_indent(
                f"{key}: {self._base_formatter(value, nested_depth)},", INDENT_WIDTH, nested_depth
            )
            for key, value in mapping.items()
        ]

        # ic(values_fmt, depth, nested_depth)
        return "\n".join(
            [
                # add_indent("{", INDENT_WIDTH, depth),
                "{",
                *values_fmt,
                add_indent("}", INDENT_WIDTH, depth),
            ]
        )


if __name__ == "__main__":
    from icecream import ic

    def separate():
        print("\n" + ("-" * 50))

    fmt = PrettyFormatter()

    separate()

    # data = load_data(Path.cwd().parent / "data/simple_list.pkl")
    simple_list = [
        1,
        2,
        {"key3": 3, "key4": {"key5": 5, "key6": 6}},
        {8, 7},
        frozenset({9, 10}),
        (11, 12),
        "string",
        b"f\xcd\x11",
    ]

    ic(simple_list)
    print(fmt(simple_list))

    separate()

    simple_dict = {"key3": 3, "key4": {"key5": 5, "key6": 6}}
    ic(simple_dict)
    print(fmt(simple_dict))
