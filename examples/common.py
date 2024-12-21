from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from colored import Fore

import pformat as pf


def _process_description(description: str) -> str:
    lines = description.split("\n")
    lines = [f"> {line}" for line in lines]
    return "\n".join(lines)


@dataclass
class Config:
    name: str
    fmt_opts: pf.FormatOptions

    def params_description(self) -> str:
        pass


def display(item: Any, configs: Iterable[Config], with_description: bool = False):
    print(f"{item = }\n")

    for config in configs:
        formatter = pf.PrettyFormatter(config.fmt_opts)
        print(f"--- {config.name} ---")
        # if (with_description):
        #     print(f"{config.description}")
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
            projections={
                float: lambda f: int(f),
                bytes: lambda b: bytearray(b),
            },
        ),
    ),
    Config(
        name="formatters | styled",
        fmt_opts=pf.FormatOptions(
            indent_type=pf.IndentType.LINE(style=Fore.green),
            text_style=Fore.cyan,
            style_entire_text=True,
            formatters=[
                pf.normal_formatter(int, lambda i, _: f"{i:.1f}"),
                pf.normal_formatter(float, lambda f, _: f"{f:.2f}"),
                pf.normal_formatter(str, lambda s, _: f's"{s}"'),
            ],
        ),
    ),
]
