from __future__ import annotations

from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any

from .formatter_types import MultilineFormatter, NormalFormatter, TypeSpecificFormatter
from .indentation_utility import add_indent

TypeSpecificFormatterMapping = Mapping[type, TypeSpecificFormatter]

INDENT_WIDTH = 4


class PrettyFormatter:
    def __init__(self):
        self._default_formatter = DefaultFormatter()

        self._formatters = OrderedDict(
            [
                (str, self._default_formatter),
                (bytes, self._default_formatter),
                (Iterable, IterableFormatter(self)),
            ]
        )

    def __call__(self, obj: Any, depth: int = 0) -> str:
        for t, formatter in self._formatters.items():
            if isinstance(obj, t):
                return self._run_formatter(obj, formatter, depth)

        return self._run_formatter(obj, self._default_formatter, depth)

    def format(self, obj: Any, depth: int = 0) -> str:
        return self(obj, depth)

    def _run_formatter(self, obj: Any, formatter: TypeSpecificFormatter, depth: int) -> str:
        if isinstance(formatter, MultilineFormatter):
            return "\n".join([add_indent(fmt, INDENT_WIDTH, depth) for fmt in formatter(obj)])

        return add_indent(formatter(obj), INDENT_WIDTH, depth)


class DefaultFormatter(NormalFormatter):
    def __call__(self, obj: Any, depth: int = 0) -> str:
        return add_indent(str(obj), INDENT_WIDTH, depth)


class IterableFormatter(MultilineFormatter):
    def __init__(self, base_formatter: PrettyFormatter):
        self._simple_types = (str, bytes)
        self._base_formatter = base_formatter

    def __call__(self, collection: Iterable, depth: int = 0) -> list[str]:
        opening, closing = self._get_parens(collection)
        nested_depth = depth + 1

        for value in collection:
            ic(value, self._base_formatter(value, nested_depth))

        values_fmt = [f"{self._base_formatter(value, nested_depth)}," for value in collection]

        ic(collection, depth, values_fmt)

        return [opening, *values_fmt, closing]

    def _get_parens(self, collection: Iterable) -> tuple[str, str]:
        if isinstance(collection, list):
            return "[", "]"
        if isinstance(collection, set):
            return "{", "}"
        if isinstance(collection, frozenset):
            return "frozen{", "}"
        if isinstance(collection, tuple) or isinstance(collection, range):
            return "(", ")"
        return "![", "]!"


if __name__ == "__main__":
    import pickle
    from pathlib import Path

    from icecream import ic

    def load_data(path: Path) -> dict:
        with open(path, "rb") as pickle_file:  # Open the file in binary read mode
            return pickle.load(pickle_file)  # Load the data

    def separate():
        print("\n" + ("-" * 50))

    ic(Path.cwd())

    separate()

    # data = load_data(Path.cwd().parent / "data/simple_list.pkl")
    data = [
        1,
        2,
        # {"key3": 3, "key4": {"key5": 5, "key6": 6}},
        {8, 7},
        frozenset({9, 10}),
        (11, 12),
        "string",
        b"f\xcd\x11",
    ]
    ic(data)

    separate()

    fmt = PrettyFormatter()
    print(fmt(data))
