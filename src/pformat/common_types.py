from collections.abc import Iterable, Mapping, MutableSequence
from typing import Any, Callable, Union

TypeProjectionFunc = Callable[[object], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]

NormalTypeFormatterFunc = Callable[[object, int], str]
MultilineTypeFormatterFunc = Callable[[object, int], Iterable[str]]
TypeFormatterFuncMutSequence = MutableSequence[
    type, Union[NormalTypeFormatterFunc, MultilineTypeFormatterFunc]
]
