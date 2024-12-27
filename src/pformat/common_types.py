from collections.abc import Iterable, Mapping
from typing import Any, Callable

TypeProjectionFunc = Callable[[Any], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]

NormalTypeFormatterFunc = Callable[[Any, int], str]
MultilineTypeFormatterFunc = Callable[[Any, int], Iterable[str]]
