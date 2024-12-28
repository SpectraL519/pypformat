import sys
from typing import Any, Callable, Union

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


def _has_valid_type(obj: Any, t: type, exact_match: bool = False) -> bool:
    if t is Any:
        return True

    if _is_union(t):
        return any(_has_valid_type(obj, _t, exact_match) for _t in t.__args__)

    return type(obj) is t if exact_match else isinstance(obj, t)


BinaryTypeCmparator = Callable[[type, type], int]
BinaryTypePredicate = Callable[[type, type], bool]


class TypeCmp:
    LT = -1
    EQ = 0
    GT = 1

    @staticmethod
    def __impl(t1: type, t2: type) -> int:
        if t1 is Any:
            return TypeCmp.GT
        if t2 is Any:
            return TypeCmp.LT

        if _is_union(t1) and _is_union(t2):
            return TypeCmp.EQ

        if _is_union(t1):
            return TypeCmp.GT if issubclass(t2, t1) else TypeCmp.LT
        if _is_union(t2):
            return TypeCmp.LT if issubclass(t1, t2) else TypeCmp.GT

        if issubclass(t1, t2):
            return TypeCmp.LT
        if issubclass(t2, t1):
            return TypeCmp.GT

        return TypeCmp.EQ

    @staticmethod
    def eq_cmp() -> BinaryTypeCmparator:
        # def _cmp(t1: type, t2: type) -> int:
        #     return TypeCmp.EQ if TypeCmp.__impl(t1, t2) == TypeCmp.EQ else TypeCmp.LT
        return lambda t1, t2: -abs(TypeCmp.__impl(t1, t2))

    @staticmethod
    def lt_cmp() -> BinaryTypeCmparator:
        return TypeCmp.__impl

    @staticmethod
    def gt_cmp() -> BinaryTypeCmparator:
        return lambda t1, t2: -TypeCmp.__impl(t1, t2)
