from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from colored import Style

ANSI_ESCAPE_PATTERN = r"\x1b\[[0-9;]*[mGK]"
ANSI_ESCAPE_RESET_PATTERN = re.escape(Style.reset)


def _clean_style(s: str) -> str:
    return re.sub(ANSI_ESCAPE_PATTERN, "", s)


def _strlen_clean(s: str) -> int:
    return len(_clean_style(s))


def _apply_style_normal(s: str, style: str) -> str:
    return f"{style}{s}{Style.reset}"


def _apply_style_override(s: str, style: str) -> str:
    return f"{style}{_clean_style(s)}{Style.reset}"


def _apply_style_preserve(s: str, style: str) -> str:
    s_aligned = re.sub(ANSI_ESCAPE_RESET_PATTERN, style, s)
    return f"{style}{s_aligned}{Style.reset}"


TextStyleValue = Optional[str]
TextStyleParam = Union["TextStyle", TextStyleValue]


@dataclass
class TextStyle:
    class Mode(Enum):
        normal = _apply_style_normal
        override = _apply_style_override
        preserve = _apply_style_preserve

    value: TextStyleValue = None
    mode: Mode = Mode.preserve

    def apply_to(self, s: str) -> str:
        if self.value is None:
            return s

        return self.mode(s, self.value)

    def apply_to_each(self, s_collection: Iterable[str]) -> list[str]:
        return [self.apply_to(s) for s in s_collection]

    @staticmethod
    def new(style: TextStyleParam) -> TextStyle:
        if style is None:
            return TextStyle()

        return TextStyle(style) if isinstance(style, str) else style
