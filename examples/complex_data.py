"""
This example shows how a complex data, like iterables and mappings, is formatted.
"""

from collections import ChainMap, Counter, OrderedDict, UserString, defaultdict
from types import MappingProxyType

from common import FMT_CONFIGS, display

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
        },
    ),
    "key11": Counter("Hello"),
}

if __name__ == "__main__":
    print("-" * 50)
    display(COLLECTION, FMT_CONFIGS)

    print("-" * 50)
    display(MAPPING, FMT_CONFIGS)
