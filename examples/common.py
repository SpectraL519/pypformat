import pformat as pf

from dataclasses import dataclass
from typing import Any
from collections.abc import Iterable
from colored import Fore, Back, Style


def _process_description(description: str) -> str:
    lines = description.split("\n")
    lines = [f"> {line}" for line in lines]
    return "\n".join(lines)


@dataclass
class Config:
    name: str
    fmt_opts: pf.FormatOptions
    description: str

    def __post_init__(self):
        self.description = _process_description(self.description)


def display(item: Any, configs: Iterable[Config], with_description: bool = False):
    print(f"{item = }\n")

    for config in configs:
        formatter = pf.PrettyFormatter(config.fmt_opts)
        print(f"--- {config.name} ---")
        if (with_description):
            print(f"{config.description}")
        print(formatter(item), "\n")


default_config = Config(
    name="default",
    fmt_opts=pf.FormatOptions(),
    description="The default formatting options configuration",
)

simple_compact_config = Config(
    name="compact, thick dot indent",
    fmt_opts=pf.FormatOptions(
        width=40,
        compact=True,
        indent_type=pf.IndentType.THICK_DOTS(width=3, style=Fore.dark_gray),
    ),
    description=(
        "A simple compact formatting configuration with:\n"
        "  - width = 40\n"
        "  - indent_type = THICK_DOTS, width=3, style=Fore.dark_gray"
    ),
)

FMT_CONFIGS = [default_config, simple_compact_config]
