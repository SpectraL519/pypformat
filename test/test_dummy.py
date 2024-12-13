from icecream import ic

from pformat import FormatOptions, PrettyFormatter

"""
This is a dummy test file to empirically test and visualize
the behaviour of PrettyFormatter
"""


FMT_OPTIONS = {
    "default": FormatOptions(),
    "compact": FormatOptions(
        width=40,
        indent_width=3,
        compact=True,
    ),
    "custom - projections": FormatOptions(
        width=40,
        compact=True,
        projections={
            float: lambda f: int(f),
            bytes: lambda b: bytearray(b),
        },
    ),
}


def test_dummy_collection():
    print()

    collection = [
        1,
        2,
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
        ic(config_name, fmt_opt)
        fmt = PrettyFormatter(fmt_opt)
        print(fmt(mapping), end="\n" * 3)
