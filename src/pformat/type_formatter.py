from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from .type_specific_callable import TypeSpecifcCallable

TypeFormatterFunc = Callable[[Any, int], str]


class TypeFormatter(TypeSpecifcCallable):
    def __init__(self, t: type):
        super().__init__(t)

    @abstractmethod
    def __call__(self, obj: Any, depth: int) -> str:
        return super().__call__(obj, depth)


class CustomFormatter(TypeFormatter):
    def __init__(self, t: type, fmt_func: TypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._validate_type(obj)
        return self.__fmt_func(obj, depth)


def make_formatter(t: type, fmt_func: TypeFormatterFunc) -> CustomFormatter:
    return CustomFormatter(t, fmt_func)
