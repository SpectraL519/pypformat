from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .format_options import FormatOptions, TypeFormatterFuncSequence, TypeProjectionFuncMapping
from .formatter_types import MultilineFormatter, NormalFormatter, TypeFormatter


class PrettyFormatter:
    def __init__(
        self,
        options: FormatOptions = FormatOptions(),
    ):
        self._options: FormatOptions = options

        self._formatters = self._options.formatters or list()
        for formatter in self.__predefined_formatters():
            if formatter not in self._formatters:
                self._formatters.append(formatter)

        self._default_formatter = DefaultFormatter()

    @staticmethod
    def new(
        width: int = FormatOptions.default("width"),
        compact: int = FormatOptions.default("compact"),
        indent_type: int = FormatOptions.default("indent_type"),
        projections: Optional[TypeProjectionFuncMapping] = FormatOptions.default("projections"),
        formatters: Optional[TypeFormatterFuncSequence] = FormatOptions.default("formatters"),
    ) -> PrettyFormatter:
        return PrettyFormatter(
            options=FormatOptions(
                width=width,
                compact=compact,
                indent_type=indent_type,
                projections=projections,
                formatters=formatters,
            )
        )

    def __call__(self, obj: Any, depth: int = 0) -> str:
        return "\n".join(self._format_impl(obj, depth))

    def format(self, obj: Any, depth: int = 0) -> str:
        return "\n".join(self._format_impl(obj, depth))

    def _format_impl(self, obj: Any, depth: int = 0) -> list[str]:
        projected_obj = self._project(obj)

        for formatter in self._formatters:
            if formatter.is_valid(projected_obj):
                return self._format_with(projected_obj, formatter, depth)

        return self._format_with(projected_obj, self._default_formatter, depth)

    def _format_with(self, obj: Any, formatter: TypeFormatter, depth: int = 0) -> list[str]:
        if isinstance(formatter, MultilineFormatter):
            return formatter(obj, depth)

        return formatter(obj, depth).split("\n")

    def _project(self, obj: Any) -> Any:
        if self._options.projections is None:
            return obj

        for t, projection in self._options.projections.items():
            if isinstance(obj, t):
                return projection(obj)

        return obj

    def __predefined_formatters(self) -> list[TypeFormatter]:
        return [
            DefaultFormatter(str),
            DefaultFormatter(bytes),
            DefaultFormatter(bytearray),
            MappingFormatter(self),
            IterableFormatter(self),
        ]


class DefaultFormatter(NormalFormatter):
    def __init__(self, t: type = Any):
        super().__init__(t)

    def __call__(self, obj: Any, depth: int = 0) -> str:
        if self.type is not Any:
            self._check_type(obj)

        return repr(obj)


class IterableFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        super().__init__(Iterable)
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

    def __call__(self, collection: Iterable, depth: int = 0) -> list[str]:
        self._check_type(collection)

        opening, closing = IterableFormatter.get_parens(collection)

        if self._options.compact:
            collecion_str = (
                opening + ", ".join(self._base_formatter(value) for value in collection) + closing
            )
            collecion_str_len = len(collecion_str) + self._options.indent_type.size(depth)
            if self._options.width is None or collecion_str_len <= self._options.width:
                return [collecion_str]

        values = list()
        for value in collection:
            v_fmt = self._base_formatter._format_impl(value, depth)
            v_fmt[-1] = f"{v_fmt[-1]},"
            values.extend(v_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
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
        return f"{type(collection).__name__}(", ")"


class MappingFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        super().__init__(Mapping)
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

    def __call__(self, mapping: Mapping, depth: int = 0) -> list[str]:
        self._check_type(mapping)

        if self._options.compact:
            mapping_str = (
                "{"
                + ", ".join(
                    f"{self._base_formatter(key)}: {self._base_formatter(value)}"
                    for key, value in mapping.items()
                )
                + "}"
            )
            collecion_str_len = len(mapping_str) + self._options.indent_type.size(depth)
            if self._options.width is None or collecion_str_len <= self._options.width:
                return [mapping_str]

        values = list()
        for key, value in mapping.items():
            key_fmt = self._base_formatter(key)
            item_values_fmt = self._base_formatter._format_impl(value, depth)
            item_values_fmt[0] = f"{key_fmt}: {item_values_fmt[0]}"
            item_values_fmt[-1] = f"{item_values_fmt[-1]},"
            values.extend(item_values_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
        return ["{", *values_fmt, "}"]
