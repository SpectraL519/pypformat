"""
This example shows how a complex data, like iterables and mappings, is formatted.
"""

from common import FMT_CONFIGS, display

COLLECTION = [
    1,
    2.123,
    {"key3": 3, "key4": {"key5": 5, "key6": 6}},
    {8, 7},
    frozenset({9, 10}),
    (11, 12),
    "string",
    b"f\xcd\x11",
    bytearray([10, 15, 20]),
    range(5),
]

MAPPING = {
    "key1": 1,
    "key2": {"key3": 3, "key4": 4},
    "key5": {
        "key6": 6,
        "a_very_long_dictionary_key7": {"key10": [10, 11, 12, 13], "key8": 8, "key9": 9},
    },
}

if __name__ == "__main__":
    print("-" * 50)
    display(COLLECTION, FMT_CONFIGS)

    print("-" * 50)
    display(MAPPING, FMT_CONFIGS)
