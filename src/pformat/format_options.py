from dataclasses import dataclass
from typing import Any, Optional

from .common_types import TypeFormatterFuncSequence, TypeProjectionFuncMapping


@dataclass
class FormatOptions:
    width: Optional[int] = 80
    indent_width: int = 4
    compact: bool = False
    projections: Optional[TypeProjectionFuncMapping] = None
    formatters: Optional[TypeFormatterFuncSequence] = None

    @staticmethod
    def default(opt_name: str) -> Any:
        return FormatOptions.__dataclass_fields__[opt_name].default
