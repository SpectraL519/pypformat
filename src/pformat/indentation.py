from collections.abc import Iterable

DEFAULT_INDENT_CHARACTER = " "


def indent_size(indent_width: int, depth: int) -> int:
    return depth * indent_width


def indent_str(indent_width: int, depth: int) -> str:
    return DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth)


def add_indent(s: str, indent_width: int, depth: int = 1) -> str:
    return f"{indent_str(indent_width, depth)}{s}"


def add_indents(str_list: Iterable[str], indent_width: int, depth: int = 1) -> list[str]:
    if len(str_list) == 0:
        return str_list

    return [add_indent(s, indent_width, depth) for s in str_list]
