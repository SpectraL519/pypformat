from __future__ import annotations

from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    UserString,
    defaultdict,
    deque,
)
from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from functools import cmp_to_key
from types import MappingProxyType
from typing import Any, MutableSequence, Optional, Union

from .format_options import FormatOptions
from .named_types import NamedIterable, NamedMapping
from .text_style import TextStyle, TextStyleParam, strlen_no_style
from .type_formatter import TypeFormatter
from .type_projection import TypeProjection


@dataclass(frozen=True)
class PFMagicMethod:
    PROJECT: str = "__pf_project__"
    FORMAT: str = "__pf_format__"


class PrettyFormatter:
    def __init__(
        self,
        options: FormatOptions = FormatOptions(),
    ):
        self._options: FormatOptions = options
        self.__setup_formatters()

    @staticmethod
    def new(
        compact: bool = FormatOptions.default("compact"),
        width: int = FormatOptions.default("width"),
        indent_type: int = FormatOptions.default("indent_type"),
        text_style: TextStyleParam = FormatOptions.default("text_style"),
        style_entire_text: bool = FormatOptions.default("style_entire_text"),
        exact_type_matching: bool = FormatOptions.default("exact_type_matching"),
        projections: Optional[Iterable[TypeProjection]] = FormatOptions.default("projections"),
        formatters: Optional[MutableSequence[TypeFormatter]] = FormatOptions.default("formatters"),
    ) -> PrettyFormatter:
        return PrettyFormatter(
            options=FormatOptions(
                width=width,
                compact=compact,
                indent_type=indent_type,
                text_style=TextStyle.new(text_style),
                style_entire_text=style_entire_text,
                exact_type_matching=exact_type_matching,
                projections=projections,
                formatters=formatters,
            )
        )

    def __call__(self, obj: Any, depth: int = 0) -> str:
        return self._format_impl(obj, depth)

    def format(self, obj: Any, depth: int = 0) -> str:
        return self(obj, depth)

    def _format_impl(self, obj: Any, depth: int = 0) -> list[str]:
        if hasattr(obj, PFMagicMethod.FORMAT):
            formatted_obj = getattr(obj, PFMagicMethod.FORMAT)(self._options)
            if not isinstance(formatted_obj, str):
                raise ValueError(
                    f"The `{PFMagicMethod.FORMAT}` method of an object `{repr(obj)}` of type `{type(obj)}` returned "
                    f"an object of type `{type(formatted_obj)}` - expected `str`"
                )
            return formatted_obj

        projected_obj = self._project(obj)

        for formatter in self._formatters:
            if formatter.has_valid_type(projected_obj, self._options.exact_type_matching):
                return formatter(projected_obj, depth)

        return self._default_formatter(projected_obj, depth)

    def _project(self, obj: Any) -> Any:
        if hasattr(obj, PFMagicMethod.PROJECT):
            return getattr(obj, PFMagicMethod.PROJECT)()

        if self._options.projections is None:
            return obj

        for projection in self._options.projections:
            if projection.has_valid_type(obj, exact_match=self._options.exact_type_matching):
                return projection(obj)

        return obj

    def __setup_formatters(self):
        if self._options.formatters is None:
            self._formatters = self.__predefined_formatters()
        else:
            self._formatters = deepcopy(self._options.formatters)
            not_covered_predefined_formatters = [
                pre_fmt
                for pre_fmt in self.__predefined_formatters()
                if not any(
                    fmt.covers(pre_fmt, exact_match=self._options.exact_type_matching)
                    for fmt in self._formatters
                )
            ]
            self._formatters.extend(not_covered_predefined_formatters)

        self._formatters = sorted(self._formatters, key=cmp_to_key(TypeFormatter.cmp))
        self._default_formatter = DefaultFormatter(Any, self._options)

    def __predefined_formatters(self) -> list[TypeFormatter]:
        return [
            DefaultFormatter(Union[str, UserString], self._options),
            DefaultFormatter(bytes, self._options),
            DefaultFormatter(bytearray, self._options),
            MappingFormatter(self),
            IterableFormatter(self),
        ]


class DefaultFormatter(TypeFormatter):
    def __init__(self, t: type, options: FormatOptions):
        super().__init__(t)

        self._exact_type_matching = options.exact_type_matching
        self._text_style = deepcopy(options.text_style)

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._validate_type(obj, self._exact_type_matching)
        return self._text_style.apply_to(repr(obj))


class IterableFormatter(TypeFormatter):
    _TYPES = Union[list, UserList, set, frozenset, tuple, range, deque, memoryview, NamedIterable]

    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

        if self._options.exact_type_matching:
            super().__init__(IterableFormatter._TYPES)
        else:
            super().__init__(Iterable)

    def __call__(self, collection: Iterable, depth: int = 0) -> str:
        self._validate_type(collection, self._options.exact_type_matching)

        opening, closing = IterableFormatter.get_parens(collection)

        if self._options.compact:
            collecion_str = (
                opening + ", ".join(self._base_formatter(value) for value in collection) + closing
            )
            collecion_str_len = strlen_no_style(collecion_str) + self._options.indent_type.length(
                depth
            )
            if collecion_str_len <= self._options.width:
                if self._options.style_entire_text:
                    return self._options.text_style.apply_to(collecion_str)
                return collecion_str

        values = list()
        for value in collection:
            v_fmt = self._base_formatter._format_impl(value, depth).split("\n")
            v_fmt[-1] = f"{v_fmt[-1]},"
            values.extend(v_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
        lines_fmt = [opening, *values_fmt, closing]

        if self._options.style_entire_text:
            lines_fmt = self._options.text_style.apply_to_each(lines_fmt)
        return "\n".join(lines_fmt)

    @staticmethod
    def get_parens(collection: Iterable) -> tuple[str, str]:
        if type(collection) in (list, UserList):
            return "[", "]"
        if type(collection) is set:
            return "{", "}"
        if type(collection) is frozenset:
            return "frozenset({", "})"
        if type(collection) in (tuple, range):
            return "(", ")"
        if type(collection) is NamedIterable:
            return collection.get_parens()

        return f"{type(collection).__name__}([", "])"


class MappingFormatter(TypeFormatter):
    _TYPES = Union[
        dict, defaultdict, UserDict, OrderedDict, ChainMap, MappingProxyType, Counter, NamedMapping
    ]

    def __init__(self, base_formatter: PrettyFormatter):
        self._base_formatter = base_formatter
        self._options = self._base_formatter._options

        if self._options.exact_type_matching:
            super().__init__(MappingFormatter._TYPES)
        else:
            super().__init__(Mapping)

    def __call__(self, mapping: Mapping, depth: int = 0) -> str:
        self._validate_type(mapping, self._options.exact_type_matching)

        opening, closing = MappingFormatter.get_parens(mapping)

        if self._options.compact:
            mapping_str = (
                opening
                + ", ".join(
                    f"{self._base_formatter(key)}: {self._base_formatter(value)}"
                    for key, value in mapping.items()
                )
                + closing
            )
            mapping_str_len = strlen_no_style(mapping_str) + self._options.indent_type.length(depth)
            if mapping_str_len <= self._options.width:
                if self._options.style_entire_text:
                    return self._options.text_style.apply_to(mapping_str)
                return mapping_str

        values = list()
        for key, value in mapping.items():
            key_fmt = self._base_formatter(key)
            item_values_fmt = self._base_formatter._format_impl(value, depth).split("\n")
            item_values_fmt[0] = f"{key_fmt}: {item_values_fmt[0]}"
            item_values_fmt[-1] = f"{item_values_fmt[-1]},"
            values.extend(item_values_fmt)

        values_fmt = self._options.indent_type.add_to_each(values)
        lines_fmt = [opening, *values_fmt, closing]

        if self._options.style_entire_text:
            lines_fmt = self._options.text_style.apply_to_each(lines_fmt)
        return "\n".join(lines_fmt)

    @staticmethod
    def get_parens(mapping: Mapping) -> tuple[str, str]:
        if type(mapping) in (dict, UserDict):
            return "{", "}"

        if isinstance(mapping, defaultdict):
            return f"defaultdict({mapping.default_factory}, {{", "})"
        if isinstance(mapping, MappingProxyType):
            return "mappingproxy({", "})"
        if type(mapping) is NamedMapping:
            return mapping.get_parens()

        return f"{type(mapping).__name__}({{", "})"
