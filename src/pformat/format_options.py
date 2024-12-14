from dataclasses import MISSING, asdict, dataclass, field, fields
from typing import Any, Optional

from .common_types import TypeFormatterFuncSequence, TypeProjectionFuncMapping
from .indentation_utility import IndentType


@dataclass
class FormatOptions:
    width: Optional[int] = 80
    compact: bool = False
    indent_type: IndentType = field(default_factory=lambda: IndentType.NONE())
    projections: Optional[TypeProjectionFuncMapping] = None
    formatters: Optional[TypeFormatterFuncSequence] = None

    def asdict(self, shallow: bool = True) -> dict:
        if shallow:
            return {field.name: getattr(self, field.name) for field in fields(self)}

        return asdict(self)

    @staticmethod
    def default(opt_name: str) -> Any:
        field = FormatOptions.__dataclass_fields__[opt_name]
        if field.default_factory is not MISSING:
            return field.default_factory()
        return field.default
