"""
This example shows how the simpla data types are formatted.
For these types the default (repr) formatter is used.
"""

from common import FMT_CONFIGS, display


class MyClass:
    pass


SIMPLE_DATA = (
    123,
    3.14,
    "string",
    b"bytes",
    bytearray([1, 2, 3]),
)


if __name__ == "__main__":
    for item in SIMPLE_DATA:
        print("-" * 50)
        display(item, FMT_CONFIGS)
