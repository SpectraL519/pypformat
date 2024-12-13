from collections.abc import Mapping, MutableSequence
from typing import Any, Callable, Union

TypeProjectionFunc = Callable[[object], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]

NormalTypeFormatterFunc = Callable[[object, int], str]
MultilineTypeFormatterFunc = Callable[[object, int], str]
TypeFormatterFuncSequence = MutableSequence[
    type, Union[NormalTypeFormatterFunc, MultilineTypeFormatterFunc]
]
