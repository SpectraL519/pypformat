from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from colored import Fore

import pformat as pf


@dataclass
class Config:
    name: str
    fmt_opts: pf.FormatOptions


def display(item: Any, configs: Iterable[Config]):
    print(f"{item = }\n")

    for config in configs:
        formatter = pf.PrettyFormatter(config.fmt_opts)
        print(f"--- {config.name} ---")
        print(formatter(item), "\n")


FMT_CONFIGS = [
    Config(
        name="default",
        fmt_opts=pf.FormatOptions(),
    ),
    Config(
        name="compact | simple",
        fmt_opts=pf.FormatOptions(
            width=40,
            compact=True,
            indent_type=pf.IndentType.DOTS(),
        ),
    ),
    Config(
        name="compact | styled",
        fmt_opts=pf.FormatOptions(
            width=40,
            compact=True,
            indent_type=pf.IndentType.THICK_DOTS(width=3, style=Fore.dark_gray),
            text_style=Fore.green,
            style_entire_text=True,
        ),
    ),
    Config(
        name="compact | projections | styled",
        fmt_opts=pf.FormatOptions(
            width=40,
            compact=True,
            indent_type=pf.IndentType.BROKEN_BAR(style=Fore.grey_37),
            text_style=Fore.magenta,
            projections=(
                pf.make_projection(float, lambda f: int(f)),
                pf.make_projection(bytes, lambda b: bytearray(b)),
            ),
        ),
    ),
    Config(
        name="formatters | styled",
        fmt_opts=pf.FormatOptions(
            indent_type=pf.IndentType.LINE(style=Fore.green),
            text_style=Fore.cyan,
            style_entire_text=True,
            formatters=[
                pf.make_formatter(int, lambda i, _: f"{i:.1f}"),
                pf.make_formatter(float, lambda f, _: f"{f:.2f}"),
                pf.make_formatter(str, lambda s, _: f's"{s}"'),
            ],
        ),
    ),
]
