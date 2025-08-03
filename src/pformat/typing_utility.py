import sys
from dataclasses import dataclass
from types import GenericAlias
from typing import Any, Union

if sys.version_info >= (3, 10):
    import types

    _union_type = types.UnionType
else:
    _union_type = None


def is_type(obj: Any) -> bool:
    return isinstance(obj, type) or isinstance(obj, GenericAlias)


def is_union(t: type) -> bool:
    return (
        (_union_type is not None and isinstance(t, _union_type))  # `|` union (Python 3.10+)
        or (hasattr(t, "__origin__") and t.__origin__ is Union)  # typing.Union
    )


BASE_TYPES = (object, Any)


def is_subclass(t1: type, t2: type) -> bool:
    if t2 in BASE_TYPES:
        return True

    if t1 in BASE_TYPES:
        return False

    if is_union(t1):
        return False

    if is_union(t2):
        return any(issubclass(t1, t) for t in t2.__args__)

    try:
        return issubclass(t1, t2)
    except TypeError:
        return False


def has_valid_type(obj: Any, t: type, exact_match: bool = False) -> bool:
    if is_type(obj) and not is_type(t):
        return False

    if t in BASE_TYPES:
        return True

    if is_union(t):
        return any(has_valid_type(obj, arg, exact_match) for arg in t.__args__)

    if exact_match:
        return type(obj) is t

    return is_subclass(type(obj), t)


@dataclass(frozen=True)
class Ordering:
    LT: int = -1
    EQ: int = 0
    GT: int = 1


def type_cmp(t1: type, t2: type) -> int:
    if t1 is t2:
        return Ordering.EQ

    if t1 in BASE_TYPES and t2 in BASE_TYPES:
        return Ordering.EQ

    if is_subclass(t1, t2):
        return Ordering.LT
    if is_subclass(t2, t1):
        return Ordering.GT

    if is_union(t1) and is_union(t2):
        return Ordering.EQ

    if is_union(t1):
        return Ordering.GT if is_subclass(t2, t1) else Ordering.EQ
    if is_union(t2):
        return Ordering.LT if is_subclass(t1, t2) else Ordering.EQ

    return Ordering.EQ
