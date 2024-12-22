from collections.abc import Iterable, Mapping
from typing import Any, Callable

TypeProjectionFunc = Callable[[object], Any]
TypeProjectionFuncMapping = Mapping[type, TypeProjectionFunc]

NormalTypeFormatterFunc = Callable[[object, int], str]
MultilineTypeFormatterFunc = Callable[[object, int], Iterable[str]]
