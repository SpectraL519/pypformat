from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

DEFAULT_INDENT_CHARACTER = " "
DEFAULT_INDENT_WIDTH = 4


@dataclass
class IndentMarker:
    character: str
    fill: bool = True

    def __post_init__(self):
        if len(self.character) != 1:
            self.character = None
            raise ValueError(
                f"The character of an IndentMarker must be a string of length 1 - got `{self.character}`"
            )


@dataclass
class IndentType:
    marker: IndentMarker
    width: int

    def size(self, depth: int) -> int:
        return self.width * depth

    def string(self, depth: int) -> str:
        if self.marker.fill:
            return self.marker.character * self.size(depth)

        return f"{self.marker.character}{DEFAULT_INDENT_CHARACTER * (self.width - 1)}" * depth

    @staticmethod
    def new(
        character: str = DEFAULT_INDENT_CHARACTER,
        fill: bool = True,
        width: int = DEFAULT_INDENT_CHARACTER,
    ) -> IndentType:
        return IndentType(
            marker=IndentMarker(character=character, fill=fill),
            width=width,
        )

    @staticmethod
    def NONE(width: int = DEFAULT_INDENT_WIDTH) -> IndentType:
        return IndentType.new(width=width)

    @staticmethod
    def DOTS(width: int = DEFAULT_INDENT_WIDTH) -> IndentType:
        return IndentType.new(
            character="·",
            width=width,
        )

    @staticmethod
    def THICK_DOTS(width: int = DEFAULT_INDENT_WIDTH) -> "IndentType":
        return IndentType.new(
            character="•",
            width=width,
        )

    @staticmethod
    def LINE(width: int = DEFAULT_INDENT_WIDTH) -> "IndentType":
        return IndentType.new(
            character="¦",
            fill=False,
            width=width,
        )


def indent_size(indent_width: int, depth: int) -> int:
    return depth * indent_width


def indent_str(indent_width: int, depth: int) -> str:
    return DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth)


def add_indent(s: str, indent_width: int, depth: int = 1) -> str:
    return f"{indent_str(indent_width, depth)}{s}"


def add_indents(str_list: Iterable[str], indent_width: int, depth: int = 1) -> list[str]:
    if len(str_list) == 0:
        return str_list

    return [add_indent(s, indent_width, depth) for s in str_list]
