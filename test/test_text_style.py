# import pytest
# from colored import Back, Fore, Style

# from pformat.text_style import apply_style

# STR = "string"
# STYLE_VALS = [Fore.light_gray, Back.green, Style.bold]


# def test_apply_style_with_none_style():
#     assert apply_style(STR, style=None) == STR


# @pytest.mark.parametrize("style", STYLE_VALS)
# def test_apply_style(style: str):
#     assert apply_style(STR, style) == f"{style}{STR}{Style.reset}"
