from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Iterator, Optional, Tuple


@dataclass
class NamedIterable(Iterable):
    name: str
    iterable: Iterable
    parens: Optional[Tuple[str, str]] = None

    def __iter__(self):
        return iter(self.iterable)

    def get_parens(self) -> Tuple[str, str]:
        return self.parens or (f"{self.name}([", "])")


@dataclass
class NamedMapping(Mapping):
    name: str
    mapping: Mapping
    parens: Optional[Tuple[str, str]] = None

    def __getitem__(self, key: Any) -> Any:
        return self.mapping[key]

    def __iter__(self) -> Iterator[Any]:
        return iter(self.mapping)

    def __len__(self) -> int:
        return len(self.mapping)

    def get_parens(self) -> Tuple[str, str]:
        return self.parens or (f"{self.name}({{", "})")
