import re

import pytest
from colored import Back, Fore, Style

from pformat.text_style import (
    ANSI_ESCAPE_RESET_PATTERN,
    TextStyle,
    rm_style_modifiers,
    strlen_no_style,
)

STYLE_VALS = [Fore.light_gray, Back.green, Style.bold]
SIMPLE_STR = "string"
STYLED_STR = SIMPLE_STR.join((STYLE_VALS + [Style.reset]) * 2)


def test_rm_style_modifiers():
    s = SIMPLE_STR.join(STYLE_VALS)
    assert rm_style_modifiers(s) == SIMPLE_STR * (len(STYLE_VALS) - 1)


def test_strlen_no_style():
    s = SIMPLE_STR.join(STYLE_VALS)
    assert strlen_no_style(s) == len(SIMPLE_STR) * (len(STYLE_VALS) - 1)


class TestTextStyle:
    MODE_VALS = [TextStyle.Mode.normal, TextStyle.Mode.override, TextStyle.Mode.preserve]

    @pytest.fixture(params=STYLE_VALS, ids=[f"{style=}" for style in STYLE_VALS])
    def sut(self, request: pytest.FixtureRequest) -> TextStyle:
        self.style = request.param
        return TextStyle(self.style)

    def test_apply_to_normal_mode(self, sut: TextStyle):
        sut.mode = TextStyle.Mode.normal
        assert sut.apply_to(SIMPLE_STR) == f"{Style.reset}{self.style}{SIMPLE_STR}{Style.reset}"

    def test_apply_to_override_mode(self, sut: TextStyle):
        sut.mode = TextStyle.Mode.override
        styled_str = SIMPLE_STR.join(STYLE_VALS)

        assert (
            sut.apply_to(styled_str)
            == f"{Style.reset}{self.style}{rm_style_modifiers(styled_str)}{Style.reset}"
        )

    def test_apply_to_preserve_mode(self, sut: TextStyle):
        sut.mode = TextStyle.Mode.preserve

        expected_styled_str = re.sub(
            ANSI_ESCAPE_RESET_PATTERN, f"{Style.reset}{self.style}", STYLED_STR
        )
        expected_styled_str = f"{Style.reset}{self.style}{expected_styled_str}{Style.reset}"

        assert sut.apply_to(STYLED_STR) == expected_styled_str

    @pytest.mark.parametrize("mode", MODE_VALS, ids=[f"{mode=}" for mode in MODE_VALS])
    def test_apply_to_each(self, sut: TextStyle, mode: TextStyle.Mode):
        empty_collection = list()
        assert len(sut.apply_to_each(empty_collection)) == 0

        s_collection = [STYLED_STR for _ in range(5)]
        expected_styled_str = sut.apply_to(STYLED_STR)
        assert all(s_out == expected_styled_str for s_out in sut.apply_to_each(s_collection))

    def test_new_with_none_style(self):
        assert TextStyle.new(None) == TextStyle()

    @pytest.mark.parametrize("style", STYLE_VALS, ids=[f"{style=}" for style in STYLE_VALS])
    def test_new_with_style_str(self, style: str):
        assert TextStyle.new(style) == TextStyle(style)

    @pytest.mark.parametrize("mode", MODE_VALS, ids=[f"{mode=}" for mode in MODE_VALS])
    def test_new_with_text_style(self, mode: TextStyle.Mode):
        style_value = "".join(STYLE_VALS)
        style = TextStyle(style_value, mode)

        assert TextStyle.new(style) == style
