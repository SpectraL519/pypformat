from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from .typing_utility import has_valid_type, type_cmp


class TypeSpecifcCallable(ABC):
    def __init__(self, t: type):
        self.type = t

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeSpecifcCallable):
            raise TypeError(
                f"Cannot compare a `{self.__class__.__name__}` instance to an instance of `{type(other).__name__}`"
            )

        return self.type == other.type

    @abstractmethod
    def __call__(self, obj: Any, *args, **kwargs) -> str | Iterable[str]:
        raise NotImplementedError(f"{repr(self)}.__call__ is not implemented")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.__name__})"

    def has_valid_type(self, obj: Any, exact_match: bool = False) -> bool:
        return has_valid_type(obj, self.type, exact_match)

    def _check_type(self, obj: Any) -> None:
        if not isinstance(obj, self.type):
            raise TypeError(
                f"[{repr(self)}] Cannot process an object of type `{type(obj).__name__}` - `{str(obj)}`"
            )

    @classmethod
    def cmp(cls, c1: TypeSpecifcCallable, c2: TypeSpecifcCallable) -> int:
        return type_cmp(c1.type, c2.type)
