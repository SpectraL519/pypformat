from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Union

from colored import Style

ANSI_ESCAPE_PATTERN = r"\x1b\[[0-9;]*[mGK]"
ANSI_ESCAPE_RESET_PATTERN = re.escape(Style.reset)


def rm_style_modifiers(s: str) -> str:
    return re.sub(ANSI_ESCAPE_PATTERN, "", s)


def strlen_no_style(s: str) -> int:
    return len(rm_style_modifiers(s))


def _apply_style_normal(s: str, style: str) -> str:
    return f"{Style.reset}{style}{s}{Style.reset}"


def _apply_style_override(s: str, style: str) -> str:
    return _apply_style_normal(rm_style_modifiers(s), style)


def _apply_style_preserve(s: str, style: str) -> str:
    s_aligned = re.sub(ANSI_ESCAPE_RESET_PATTERN, f"{Style.reset}{style}", s)
    return _apply_style_normal(s_aligned, style)


TextStyleValue = Optional[str]
TextStyleParam = Union["TextStyle", TextStyleValue]


@dataclass
class TextStyle:
    class Mode(Enum):
        normal = ("normal", _apply_style_normal)
        override = ("override", _apply_style_override)
        preserve = ("preserve", _apply_style_preserve)

        def __new__(cls, name: str, callback: Callable[[str, str], str]):
            obj = object.__new__(cls)
            obj._value_ = name
            obj.callback = callback
            return obj

    value: TextStyleValue = None
    mode: Mode = Mode.preserve

    def apply_to(self, s: str) -> str:
        if self.value is None:
            return s

        return self.mode.callback(s, self.value)

    def apply_to_each(self, s_collection: Iterable[str]) -> list[str]:
        return [self.apply_to(s) for s in s_collection]

    @staticmethod
    def new(style: TextStyleParam = None, mode: Optional[Mode] = None) -> TextStyle:
        def _mode(
            _in: Optional[TextStyle.Mode], _default: TextStyle.Mode = TextStyle.Mode.preserve
        ) -> TextStyle.Mode:
            return _in or _default

        if style is None:
            return TextStyle(mode=_mode(mode))

        return (
            TextStyle(style, mode=_mode(mode))
            if isinstance(style, str)
            else TextStyle(style.value, mode=_mode(mode, style.mode))
        )
