from colored import Fore
from icecream import ic

from pformat import FormatOptions, IndentType, PrettyFormatter, normal_formatter

"""
This is a dummy test file to empirically test and visualize
the behaviour of PrettyFormatter
"""


FMT_OPTIONS = {
    "default": FormatOptions(),
    "compact, dot indent (dark_gray), Fore.green": FormatOptions(
        width=40,
        compact=True,
        indent_type=IndentType.DOTS(width=3, style=Fore.dark_gray),
        text_style=f"{Fore.green}",
    ),
    "compact, bbar indent (grey_37), projections": FormatOptions(
        width=40,
        compact=True,
        indent_type=IndentType.BROKEN_BAR(style=Fore.grey_37),
        projections={
            float: lambda f: int(f),
            bytes: lambda b: bytearray(b),
        },
    ),
    "line indent (green), formatters": FormatOptions(
        indent_type=IndentType.LINE(style=Fore.green),
        formatters=[
            normal_formatter(int, lambda i, _: f"{i:.1f}"),
            normal_formatter(float, lambda f, _: f"{f:.2f}"),
            normal_formatter(str, lambda s, _: f'str"{s}"'),
        ],
    ),
}


def test_dummy_collection():
    print()

    collection = [
        1,
        2.123,
        {"key3": 3, "key4": {"key5": 5, "key6": 6}},
        {8, 7},
        frozenset({9, 10}),
        (11, 12),
        "string",
        b"f\xcd\x11",
    ]

    ic(collection)
    print("\n" + ("-" * 50) + "\n")

    for config_name, fmt_opt in FMT_OPTIONS.items():
        ic(config_name)
        fmt = PrettyFormatter(fmt_opt)
        print(fmt(collection), end="\n" * 3)


def test_dummy_mapping():
    print()

    mapping = {
        "key1": 1,
        "key2": {"key3": 3, "key4": 4},
        "key5": {
            "key6": 6,
            "super_turbo_long_mega_key7": {"key10": [10, 11, 12, 13], "key8": 8, "key9": 9},
        },
    }

    ic(mapping)
    print("\n" + ("-" * 50) + "\n")

    for config_name, fmt_opt in FMT_OPTIONS.items():
        ic(config_name)
        fmt = PrettyFormatter(fmt_opt)
        print(fmt(mapping), end="\n" * 3)
