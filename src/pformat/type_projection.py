from typing import Any, Callable

from .type_specific_callable import TypeSpecifcCallable

TypeProjectionFunc = Callable[[Any], Any]


def identity_projection_func(obj: Any) -> Any:
    return obj


class TypeProjection(TypeSpecifcCallable):
    def __init__(self, t: type, projection_func: TypeProjectionFunc = identity_projection_func):
        super().__init__(t)
        self.__proj_func = projection_func

    def __call__(self, obj: Any) -> Any:
        self._check_type(obj)
        return self.__proj_func(obj)


def projection(t: type, projection_func: TypeProjectionFunc) -> TypeProjection:
    return TypeProjection(t, projection_func)
