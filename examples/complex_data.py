"""
This example shows how a complex data, like iterables and mappings, is formatted.
"""

from collections import ChainMap, Counter, OrderedDict, UserDict, UserList, UserString, defaultdict
from dataclasses import dataclass
from types import MappingProxyType

from common import FMT_CONFIGS, display

import pformat as pf


@dataclass
class ProjecablePoint:
    x: int = 0
    y: int = 0
    asdict: bool = False

    def __pf_project__(self):
        if self.asdict:
            return pf.NamedMapping(
                name="ProjecablePoint",
                mapping={"x": self.x, "y": self.y},
                parens=("ProjectablePoint(", ")"),
            )
        else:
            return pf.NamedIterable(name="ProjecablePoint", iterable=(self.x, self.y))


@dataclass
class FormattablePoint:
    x: int
    y: int

    def __pf_format__(self, options: pf.FormatOptions) -> str:
        return options.text_style.apply_to(f"p[{self.x}, {self.y}]")


COLLECTION = [
    1,
    2.123,
    {"key3": 3, "key4": MappingProxyType({"key5": 5, "key6": 6})},
    {8, 7},
    frozenset({9, 10}),
    (11, 12),
    "string",
    UserString("user_string"),
    b"f\xcd\x11",
    bytearray([10, 15, 20]),
    range(5),
    UserList([1, 2, 3]),
    [ProjecablePoint(3, 14), ProjecablePoint(3, 14, asdict=True), FormattablePoint(3, 14)],
]

MAPPING = {
    "key1": 1,
    "key2": OrderedDict({"key3": 3, "key4": 4}),
    "key5": defaultdict(
        str,
        {
            "key6": 6,
            "a_very_long_dictionary_key7": ChainMap(
                {"key10": [10, 11, 12, 13], "key8": 8, "key9": 9}
            ),
            "key11": Counter("Hello"),
        },
    ),
    "key12": UserDict({0: "a", 1: "b", 2: "c"}),
}

if __name__ == "__main__":
    print("-" * 50)
    display(COLLECTION, FMT_CONFIGS)

    print("-" * 50)
    display(MAPPING, FMT_CONFIGS)
