from collections.abc import Mapping
from typing import Any, Callable

from .type_specific_callable import TypeSpecifcCallable

TypeProjectionFunc = Callable[[Any], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]


class TypeProjection(TypeSpecifcCallable):
    def __init__(self, t: type, projection_func: TypeProjectionFunc):
        super().__init__(t)
        self.__func = projection_func

    def __call__(self, value: Any) -> Any:
        return self.__func(value)
