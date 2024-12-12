from dataclasses import MISSING, dataclass
from typing import Any


@dataclass
class FormatOptions:
    width: int = 80
    indent_width: int = 4
    compact: bool = False

    @staticmethod
    def default(opt_name: str) -> Any:
        field = FormatOptions.__dataclass_fields__[opt_name]
        if field.default_factory is not MISSING:
            return field.default_factory()
        return field.default
