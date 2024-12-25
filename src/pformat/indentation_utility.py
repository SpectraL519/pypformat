from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .text_style import TextStyle, TextStyleParam

DEFAULT_INDENT_CHARACTER = " "
DEFAULT_INDENT_WIDTH = 4


@dataclass
class IndentMarker:
    character: str = DEFAULT_INDENT_CHARACTER
    fill: bool = True

    def __post_init__(self):
        if len(self.character) != 1:
            raise ValueError(
                f"The character of an IndentMarker must be a string of length 1 - got `{self.character}`"
            )


@dataclass
class IndentType:
    width: int = DEFAULT_INDENT_WIDTH
    marker: IndentMarker = field(default_factory=IndentMarker)
    style: TextStyle = field(default_factory=TextStyle)

    def __post_init__(self):
        if not isinstance(self.style, TextStyle):
            self.style = TextStyle.new(self.style)

    def length(self, depth: int) -> int:
        return self.width * depth

    def string(self, depth: int) -> str:
        return self.style.apply_to(self.__string(depth))

    def add_to(self, s: str, depth: int = 1) -> str:
        return f"{self.string(depth)}{s}"

    def add_to_each(self, s_collection: Iterable[str], depth: int = 1) -> list[str]:
        return [self.add_to(s, depth) for s in s_collection]

    def __string(self, depth: int) -> str:
        if self.marker.fill:
            return self.marker.character * self.length(depth)

        return f"{self.marker.character}{DEFAULT_INDENT_CHARACTER * (self.width - 1)}" * depth

    @staticmethod
    def new(
        width: int = DEFAULT_INDENT_WIDTH,
        character: str = DEFAULT_INDENT_CHARACTER,
        fill: bool = True,
        style: TextStyleParam = None,
    ) -> IndentType:
        return IndentType(
            width=width,
            marker=IndentMarker(character=character, fill=fill),
            style=style,
        )

    @staticmethod
    def NONE(width: int = DEFAULT_INDENT_WIDTH) -> IndentType:
        return IndentType.new(width=width, style=None)

    @staticmethod
    def DOTS(
        width: int = DEFAULT_INDENT_WIDTH,
        style: TextStyleParam = None,
    ) -> IndentType:
        return IndentType.new(
            width=width,
            character="·",
            style=style,
        )

    @staticmethod
    def THICK_DOTS(
        width: int = DEFAULT_INDENT_WIDTH,
        style: TextStyleParam = None,
    ) -> IndentType:
        return IndentType.new(
            width=width,
            character="•",
            style=style,
        )

    @staticmethod
    def LINE(
        width: int = DEFAULT_INDENT_WIDTH,
        style: TextStyleParam = None,
    ) -> IndentType:
        return IndentType.new(
            width=width,
            character="|",
            fill=False,
            style=style,
        )

    @staticmethod
    def BROKEN_BAR(
        width: int = DEFAULT_INDENT_WIDTH,
        style: TextStyleParam = None,
    ) -> IndentType:
        return IndentType.new(
            width=width,
            character="¦",
            fill=False,
            style=style,
        )
