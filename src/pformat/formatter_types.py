from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Union

from .common_types import MultilineTypeFormatterFunc, NormalTypeFormatterFunc

if sys.version_info >= (3, 10):
    import types

    union_type = types.UnionType
else:
    union_type = None


def _is_union(t: type) -> bool:
    return (
        (union_type is not None and isinstance(t, union_type))  # `|` union (Python 3.10+)
        or (hasattr(t, "__origin__") and t.__origin__ is Union)  # typing.Union
    )


def _has_valid_type(obj: Any, t: type, exact_match: bool) -> bool:
    if t is Any:
        return True

    if _is_union(t):
        return any(_has_valid_type(obj, _t, exact_match) for _t in t.__args__)

    return type(obj) is t if exact_match else isinstance(obj, t)


class TypeFormatter(ABC):
    def __init__(self, t: type):
        self.type = t

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeFormatter):
            raise TypeError(
                f"Cannot compare a `{self.__class__.__name__}` instance to an instance of `{type(other).__name__}`"
            )

        return self.type == other.type

    @abstractmethod
    def __call__(self, obj: Any, depth: int = 0) -> str | Iterable[str]:
        raise NotImplementedError(f"{repr(self)}.__call__ is not implemented")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.__name__})"

    def has_valid_type(self, obj: Any, exact_match: bool = False) -> bool:
        return _has_valid_type(obj, self.type, exact_match)

    def _check_type(self, obj: Any) -> None:
        if not isinstance(obj, self.type):
            raise TypeError(
                f"[{repr(self)}] Cannot format an object of type `{type(obj).__name__}` - `{str(obj)}`"
            )


class NormalFormatter(TypeFormatter):
    def __init__(self, t: type):
        super().__init__(t)

    @abstractmethod
    def __call__(self, obj: Any, depth: int = 0) -> str:
        super().__call__(obj, depth)


class CustomNormalFormatter(NormalFormatter):
    def __init__(self, t: type, fmt_func: NormalTypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._check_type(obj)
        return self.__fmt_func(obj, depth)


def normal_formatter(t: type, fmt_func: NormalTypeFormatterFunc) -> CustomNormalFormatter:
    return CustomNormalFormatter(t, fmt_func)


class MultilineFormatter(TypeFormatter):
    def __init__(self, t: type):
        super().__init__(t)

    @abstractmethod
    def __call__(self, obj: Any, depth: int = 0) -> Iterable[str]:
        super().__call__(obj, depth)


class CustomMultilineFormatter(MultilineFormatter):
    def __init__(self, t: type, fmt_func: MultilineTypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._check_type(obj)
        return self.__fmt_func(obj, depth)


def multiline_formatter(t: type, fmt_func: MultilineTypeFormatterFunc) -> CustomMultilineFormatter:
    return CustomMultilineFormatter(t, fmt_func)
