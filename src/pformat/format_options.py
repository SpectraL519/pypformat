from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable, Optional

TypeProjection = Callable[[object], Any]
TypeProjectionMapping = Mapping[type, TypeProjection]


@dataclass
class FormatOptions:
    width: Optional[int] = 80
    indent_width: int = 4
    compact: bool = False
    projections: Optional[TypeProjectionMapping] = None

    @staticmethod
    def default(opt_name: str) -> Any:
        return FormatOptions.__dataclass_fields__[opt_name].default
