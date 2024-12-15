from typing import Optional

from colored import Style


def apply_style(s: str, style: Optional[str]) -> str:
    if style is None:
        return s

    return f"{style}{s}{Style.reset}"
