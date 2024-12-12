from __future__ import annotations

from collections import OrderedDict, deque
from collections.abc import Iterable, Mapping
from typing import Any

from .formatter_types import MultilineFormatter, NormalFormatter, TypeSpecificFormatter
from .indentation import add_indents

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

    def __call__(self, obj: Any) -> str:
        return "\n".join(self._format_impl(obj))

    def format(self, obj: Any) -> str:
        return "\n".join(self._format_impl(obj))

    def _format_impl(self, obj: Any) -> list[str]:
        for t, formatter in self._formatters.items():
            if isinstance(obj, t):
                return self._format_with(obj, formatter)

        return self._format_with(obj, self._default_formatter)

    def _format_with(self, obj: Any, formatter: TypeSpecificFormatter) -> list[str]:
        if isinstance(formatter, MultilineFormatter):
            return formatter(obj)

        return formatter(obj).split("\n")


class DefaultFormatter(NormalFormatter):
    def __call__(self, obj: Any, depth: int = 0) -> str:
        return repr(obj)


class IterableFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter

    def __call__(self, collection: Iterable) -> list[str]:
        opening, closing = IterableFormatter.get_parens(collection)

        values = list()
        for value in collection:
            v_fmt = self._base_formatter._format_impl(value)
            v_fmt[-1] = f"{v_fmt[-1]},"
            values.extend(v_fmt)

        values_fmt = add_indents(values, INDENT_WIDTH, 1)
        return [opening, *values_fmt, closing]

    @staticmethod
    def get_parens(collection: Iterable) -> tuple[str, str]:
        if isinstance(collection, list):
            return "[", "]"
        if isinstance(collection, set):
            return "{", "}"
        if isinstance(collection, frozenset):
            return "frozen{", "}"
        if isinstance(collection, tuple) or isinstance(collection, range):
            return "(", ")"
        if isinstance(collection, deque):
            return "deque([", "])"
        return "![", "]!"


class MappingFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter

    def __call__(self, mapping: Mapping) -> list[str]:
        values = list()
        for key, value in mapping.items():
            key_fmt = self._base_formatter(key)
            item_values_fmt = self._base_formatter._format_impl(value)
            item_values_fmt[0] = f"{key_fmt}: {item_values_fmt[0]}"
            item_values_fmt[-1] = f"{item_values_fmt[-1]},"
            values.extend(item_values_fmt)

        values_fmt = add_indents(values, INDENT_WIDTH, 1)
        return ["{", *values_fmt, "}"]
