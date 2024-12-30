from dataclasses import MISSING, asdict, dataclass, field, fields
from functools import cmp_to_key
from typing import Any, Iterable, MutableSequence, Optional

from .indentation_utility import IndentType
from .text_style import TextStyle
from .type_formatters import TypeFormatter
from .type_projection import TypeProjection


@dataclass
class FormatOptions:
    compact: bool = False
    width: int = 50
    indent_type: IndentType = field(default_factory=lambda: IndentType.NONE())
    text_style: TextStyle = field(default_factory=TextStyle)
    style_entire_text: bool = False
    exact_type_matching: bool = False
    projections: Optional[Iterable[TypeProjection]] = None
    formatters: Optional[MutableSequence[TypeFormatter]] = None

    def __post_init__(self):
        if not isinstance(self.text_style, TextStyle):
            self.text_style = TextStyle.new(self.text_style)

        if self.projections is not None:
            self.projections = sorted(self.projections, key=cmp_to_key(TypeProjection.cmp))

        if self.formatters is not None:
            self.formatters = sorted(self.formatters, key=cmp_to_key(TypeFormatter.cmp))

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
