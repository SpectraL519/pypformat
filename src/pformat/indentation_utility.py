DEFAULT_INDENT_CHARACTER = " "


def indent_size(indent_width: int, depth: int) -> int:
    return depth * indent_width


def indent_str(indent_width: int, depth: int) -> str:
    return DEFAULT_INDENT_CHARACTER * indent_size(indent_width, depth)


def add_indent(s: str, indent_width: int, depth: int) -> str:
    return f"{indent_str(indent_width, depth)}{s}"
