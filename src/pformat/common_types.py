from collections.abc import Mapping
from typing import Any, Callable, Union

TypeProjectionFunc = Callable[[object], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]

NormalTypeFormatterFunc = Callable[[object, int], str]
MultilineTypeFormatterFunc = Callable[[object, int], str]
TypeFormatterFuncMapping = Mapping[type, Union[NormalTypeFormatterFunc, MultilineTypeFormatterFunc]]
