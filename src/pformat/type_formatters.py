from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Callable

from .type_specific_callable import TypeSpecifcCallable

NormalTypeFormatterFunc = Callable[[Any, int], str]
MultilineTypeFormatterFunc = Callable[[Any, int], Iterable[str]]


class TypeFormatter(TypeSpecifcCallable):
    pass


class NormalFormatter(TypeFormatter):
    pass


class CustomNormalFormatter(NormalFormatter):
    def __init__(self, t: type, fmt_func: NormalTypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._validate_type(obj)
        return self.__fmt_func(obj, depth)


def normal_formatter(t: type, fmt_func: NormalTypeFormatterFunc) -> CustomNormalFormatter:
    return CustomNormalFormatter(t, fmt_func)


class MultilineFormatter(TypeFormatter):
    pass


class CustomMultilineFormatter(MultilineFormatter):
    def __init__(self, t: type, fmt_func: MultilineTypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._validate_type(obj)
        return self.__fmt_func(obj, depth)


def multiline_formatter(t: type, fmt_func: MultilineTypeFormatterFunc) -> CustomMultilineFormatter:
    return CustomMultilineFormatter(t, fmt_func)
