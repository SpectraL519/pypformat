from __future__ import annotations

from collections import ChainMap, OrderedDict, defaultdict, deque
from collections.abc import Iterable, Mapping
from types import MappingProxyType
from typing import Any, Optional, Union

from .format_options import (
    FormatOptions,
    TypeFormatterFuncMutSequence,
    TypeProjectionFuncMapping,
)
from .formatter_types import MultilineFormatter, NormalFormatter, TypeFormatter
from .text_style import TextStyle, TextStyleParam, strlen_no_style


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

        self._default_formatter = DefaultFormatter(text_style=self._options.text_style)

    @staticmethod
    def new(
        width: int = FormatOptions.default("width"),
        compact: int = FormatOptions.default("compact"),
        indent_type: int = FormatOptions.default("indent_type"),
        text_style: TextStyleParam = FormatOptions.default("text_style"),
        style_entire_text: bool = FormatOptions.default("style_entire_text"),
        strict_type_matching: bool = FormatOptions.default("strict_type_matching"),
        projections: Optional[TypeProjectionFuncMapping] = FormatOptions.default("projections"),
        formatters: Optional[TypeFormatterFuncMutSequence] = FormatOptions.default("formatters"),
    ) -> PrettyFormatter:
        return PrettyFormatter(
            options=FormatOptions(
                width=width,
                compact=compact,
                indent_type=indent_type,
                text_style=TextStyle.new(text_style),
                style_entire_text=style_entire_text,
                strict_type_matching=strict_type_matching,
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
            if formatter.has_valid_type(projected_obj, self._options.strict_type_matching):
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
            DefaultFormatter(str, self._options.text_style),
            DefaultFormatter(bytes, self._options.text_style),
            DefaultFormatter(bytearray, self._options.text_style),
            MappingFormatter(self),
            IterableFormatter(self),
        ]


class DefaultFormatter(NormalFormatter):
    def __init__(self, t: type = Any, text_style: TextStyleParam = None):
        super().__init__(t)
        self._text_style = TextStyle.new(text_style)

    def __call__(self, obj: Any, depth: int = 0) -> str:
        if self.type is not Any:
            self._check_type(obj)

        return self._text_style.apply_to(repr(obj))


class IterableFormatter(MultilineFormatter):
    _TYPES = Union[list, set, frozenset, tuple, range, deque, memoryview]

    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

        if self._options.strict_type_matching:
            super().__init__(IterableFormatter._TYPES)
        else:
            super().__init__(Iterable)

    def __call__(self, collection: Iterable, depth: int = 0) -> list[str]:
        self._check_type(collection)

        opening, closing = IterableFormatter.get_parens(collection)

        if self._options.compact:
            collecion_str = (
                opening + ", ".join(self._base_formatter(value) for value in collection) + closing
            )
            collecion_str_len = strlen_no_style(collecion_str) + self._options.indent_type.length(
                depth
            )
            if self._options.width is None or collecion_str_len <= self._options.width:
                if self._options.style_entire_text:
                    return [self._options.text_style.apply_to(collecion_str)]
                return [collecion_str]

        values = list()
        for value in collection:
            v_fmt = self._base_formatter._format_impl(value, depth)
            v_fmt[-1] = f"{v_fmt[-1]},"
            values.extend(v_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
        if self._options.style_entire_text:
            return self._options.text_style.apply_to_each([opening, *values_fmt, closing])
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
    _TYPES = Union[dict, defaultdict, OrderedDict, MappingProxyType, ChainMap]

    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

        if self._options.strict_type_matching:
            super().__init__(MappingFormatter._TYPES)
        else:
            super().__init__(Mapping)

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
            mapping_str_len = strlen_no_style(mapping_str) + self._options.indent_type.length(depth)
            if self._options.width is None or mapping_str_len <= self._options.width:
                if self._options.style_entire_text:
                    return [self._options.text_style.apply_to(mapping_str)]
                return [mapping_str]

        values = list()
        for key, value in mapping.items():
            key_fmt = self._base_formatter(key)
            item_values_fmt = self._base_formatter._format_impl(value, depth)
            item_values_fmt[0] = f"{key_fmt}: {item_values_fmt[0]}"
            item_values_fmt[-1] = f"{item_values_fmt[-1]},"
            values.extend(item_values_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
        if self._options.style_entire_text:
            return self._options.text_style.apply_to_each(["{", *values_fmt, "}"])
        return ["{", *values_fmt, "}"]
