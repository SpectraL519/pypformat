from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .typing_utility import has_valid_type, is_subclass, type_cmp


class TypeSpecifcCallable(ABC):
    def __init__(self, t: type):
        self.type = t

    def __eq__(self, other: TypeSpecifcCallable) -> bool:
        self._validate_for_comparison(other)
        return self.type is other.type

    def _validate_for_comparison(self, other: Any):
        if not isinstance(other, TypeSpecifcCallable):
            raise TypeError(
                f"Cannot compare a `{self.__class__.__name__}` instance to an instance of `{type(other).__name__}`"
            )

    @abstractmethod
    def __call__(self, obj: Any, *args, **kwargs) -> Any:
        raise NotImplementedError(f"{repr(self)}.__call__ is not implemented")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.__name__})"

    def has_valid_type(self, obj: Any, exact_match: bool = False) -> bool:
        return has_valid_type(obj, self.type, exact_match)

    def _validate_type(self, obj: Any, exact_match: bool = False) -> None:
        if not self.has_valid_type(obj, exact_match):
            raise TypeError(
                f"[{repr(self)}] Cannot process an object of type `{type(obj).__name__}` - `{str(obj)}`"
            )

    def covers(self, other: TypeSpecifcCallable, exact_match: bool = False) -> bool:
        return other.type is self.type if exact_match else is_subclass(other.type, self.type)

    @classmethod
    def cmp(cls, c1: TypeSpecifcCallable, c2: TypeSpecifcCallable) -> int:
        return type_cmp(c1.type, c2.type)
