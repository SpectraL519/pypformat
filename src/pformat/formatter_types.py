from __future__ import annotations

from typing import Any

from .common_types import MultilineTypeFormatterFunc, NormalTypeFormatterFunc


class TypeFormatter:
    def __init__(self, t: type):
        self.type = t

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeFormatter):
            raise TypeError(
                f"Cannot compare a `{self.__class__.__name__}` instance to an instance of `{type(other).__name__}`"
            )

        return self.type == other.type

    def __call__(self, obj: Any, depth: int = 0) -> str:
        raise NotImplementedError(f"{repr(self)}.__call__ is not implemented")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.__name__})"

    def is_valid(self, obj: Any) -> None:
        if self.type is Any:
            return True
        return isinstance(obj, self.type)

    def _check_type(self, obj: Any) -> None:
        if not isinstance(obj, self.type):
            raise TypeError(
                f"[{repr(self)}] Cannot format an object of type `{type(obj).__name__}` - `{str(obj)}`"
            )


class NormalFormatter(TypeFormatter):
    def __init__(self, t: type):
        super().__init__(t)


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


class CustomMultilineFormatter(MultilineFormatter):
    def __init__(self, t: type, fmt_func: MultilineTypeFormatterFunc):
        super().__init__(t)
        self.__fmt_func = fmt_func

    def __call__(self, obj: Any, depth: int = 0) -> str:
        self._check_type(obj)
        return self.__fmt_func(obj, depth)


def multiline_formatter(t: type, fmt_func: MultilineTypeFormatterFunc) -> CustomMultilineFormatter:
    return CustomMultilineFormatter(t, fmt_func)
