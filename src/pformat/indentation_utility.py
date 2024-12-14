from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

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

    def size(self, depth: int) -> int:
        return self.width * depth

    def string(self, depth: int) -> str:
        if self.marker.fill:
            return self.marker.character * self.size(depth)

        return f"{self.marker.character}{DEFAULT_INDENT_CHARACTER * (self.width - 1)}" * depth

    def add_to(self, s: str, depth: int = 1) -> str:
        return f"{self.string(depth)}{s}"

    def add_to_each(self, s_collection: Iterable[str], depth: int = 1) -> list[str]:
        return [self.add_to(s, depth) for s in s_collection]

    @staticmethod
    def new(
        width: int = DEFAULT_INDENT_WIDTH,
        character: str = DEFAULT_INDENT_CHARACTER,
        fill: bool = True,
    ) -> IndentType:
        return IndentType(
            width=width,
            marker=IndentMarker(character=character, fill=fill),
        )

    @staticmethod
    def NONE(width: int = DEFAULT_INDENT_WIDTH) -> IndentType:
        return IndentType.new(width=width)

    @staticmethod
    def DOTS(width: int = DEFAULT_INDENT_WIDTH) -> IndentType:
        return IndentType.new(
            width=width,
            character="·",
        )

    @staticmethod
    def THICK_DOTS(width: int = DEFAULT_INDENT_WIDTH) -> "IndentType":
        return IndentType.new(
            width=width,
            character="•",
        )

    @staticmethod
    def LINE(width: int = DEFAULT_INDENT_WIDTH) -> "IndentType":
        return IndentType.new(
            width=width,
            character="|",
            fill=False,
        )

    @staticmethod
    def BROKEN_BAR(width: int = DEFAULT_INDENT_WIDTH) -> "IndentType":
        return IndentType.new(
            width=width,
            character="¦",
            fill=False,
        )
