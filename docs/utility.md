# PyPformat - Utility

- [Type-specific formatters](#type-specific-formatters)
- [Text styling](#text-styling)
- [Indentation](#indentation)

<br />
<br />

## Type-specific formatters

The `PrettyFormatter` class cotnains an ordered collection of type specific formatters. When formatting an item, this collection is traversed and the first matching formatter is applied to the input item.

The type specific formatters are instances of the `TypeFormatter` abstract class (defined in the [type_specific_formatters.py](/src/pformat/type_specific_formatters.py) file). The identifier of this class is its `type` member, which is then used in matching the formatted item's type in the function:

```python
has_valid_type(obj: Any, exact_match: bool = False) -> bool
```

<br />

The `TypeFormatter` class is the base type used for type specific formatters and defines a common, abstract method:

```python
@abstractmethod
__call__(self, obj: Any, depth: int = 0) -> str | Iterable[str]
```

However, the abstract classes actually used as base types for concrete formatters are:

- `NormalFormatter(TypeFormatter)` - the `__call__` abstract method should return an instance of `str`,
- `MultilineFormatter(TypeFormatter)` - the `__call__` abstract method should return an instance of `Iterable[str]`, where each element in the returned collection should be a sepparate line.

With that in mind, you can use these classes to create custom formatters.

Alternatively, you can create custom formatter objects using the predefined functions:

```python
normal_formatter(t: type, fmt_func: NormalTypeFormatterFunc) -> CustomNormalFormatter
multiline_formatter(t: type, fmt_func: MultilineTypeFormatterFunc) -> CustomMultilineFormatter
```

Where the `fmt_func` parameters are callables, the signatures of which match the signatures of the `__call__` abstract methods of their corresponding base classes.

<br />
<br />

## Text styling

> [!IMPORTANT]
> `PyPformat` utilizes the [colored](https://dslackw.gitlab.io/colored/) package for text styling.

Text styling in the `PyPformat` package is done via the `TextStyle` dataclass defined in the [text_style.py](/src/pformat/text_style.py) file.

The members of this class are:

| **Name** | **Type** | **Default value** | **Description** |
| :- | :- | :- | :- |
| `value` | `TextStyleValue` | `None` | Represents the actual text style string, e.g.:<br/>- `colored.Fore.green`<br/>- `colored.Back.red`<br/>- `colored.Style.underline` |
| `mode` | `TextStyle.Mode` | `Mode.preserve` | Specifies how the text style should be applied to a string when using the `apply_to` method. |

> [!NOTE]
>
> The table below presents all available text style modes.
>
> | **Name** | **Description** |
> | :- | :- |
> | normal | Returns `f"{Style.reset}{style}{s}{Style.reset}"` for an input string `s`. |
> | preserve | Replaces all `Style.reset` occurances with `f"{Style.reset}{<style>}"` in the input string and then applies the style like the *normal* mode to the aligned string. |
> | override | Removes all style modifiers from the input string and then applies the style like the *normal* mode to the aligned string. |

<br />

### Additional utility

#### Type definitions

- `TextStyleValue` - a type alias for `Optional[str]`
- `TextStyleParam` - a type alias for `Union[TextStyle, TextStyleValue]`

<br />

#### Utility methods of the `TextStyle` class

- `apply_to(s: str) -> str` - returns the input string with the text style applied based on the `mode` parameter
- `apply_to_each(s_collection: Iterable[str]) -> list[str]` - returns a new list of styled strings constructed by calling the `apply_to` method for each string in the input iterable
- [static] `new(style: TextStyleParam = None, mode: Optional[Mode] = None) -> TextStyle` - creates a new `TextStyle` instance based on the input parameters

<br />

#### Utility functions

- `rm_style_modifiers(s: str) -> str` - removes all ANSI escape sequences from a string
- `strlen_no_style(s: str) -> int` - returns the length of the string after removing its style modifiers

<br />
<br />

## Indentation

The indentation types/options for the `PrettyFormatter` are specified via the `IndentType` dataclass, the members of which are defined in the table below.

| **Name** | **Type** | **Default value** | **Description** |
| :- | :- | :- | :- |
| `width` | `int` | `4` | Specifies the width of a single indentation level. |
| `marker` | `IndentMarker` | `IndentMarker()` | Defines the character to use for indentation marking. |
| `style` | [`TextStyle`](#text-styling) | `TextStyle()` | Defines the style to be applied to the indentation markers in the formatted output. |

> [!NOTE]
> The `IndentMarker` dataclass is defines the following members.
>
> | **Name** | **Type** | **Default value** | **Description** |
> | :- | :- | :- | :- |
> | `character` | `str` | `" "` | The character which will be used to mark the indentation. |
> | `fill` | `bool` | `True` | Specifies whether the `character` should fill the entire indendation marker (if `True`) or just the first character at each level/depth (if `False`) |

<br />

The `IndentType` class defines the following utility methods:

- `length(depth: int) -> int` - returns the length of the unstyled indentation string at the given depth
- `string(depth: int) -> str` - return the styled indentation string using for the given depth
- `add_to(s: str, depth: int = 1) -> str` - returns the input string with a prepended, styled indentation string
- `add_to_each(s_collection: Iterable[str], depth: int = 1) -> list[str]` - returns a new list of strings with prepended, styled indendation strings constructed by calling the `add_to` method for each string in the input iterable

<br />

You can create new instances of the `IndentType` class using the `new` static method:

```python
@staticmethod
def new(
    width: int = 4,
    character: str = " ",
    fill: bool = True,
    style: TextStyleParam = None,
) -> IndentType:
    return IndentType(
        width=width,
        marker=IndentMarker(character=character, fill=fill),
        style=style,
    )
```

Alternatively, you can use the predefined type builder methods presented below.

> [!NOTE]
> All builder methods are *static* and their parameters have the same types and default values as the `new` method.

```python
def NONE(width):
    return IndentType.new(width=width, style=None)

def DOTS(width, style):
    return IndentType.new(width=width, character="·", style=style)

def THICK_DOTS(width, style):
    return IndentType.new(width=width, character="•", style=style)

def LINE(width, style):
    return IndentType.new(width=width, character="|", fill=False, style=style)

def BROKEN_BAR(width, style):
    return IndentType.new(width=width, character="¦", fill=False, style=style)
```

```python
>>> import pformat as pf
>>> pf.IndentType.NONE().string(depth=2)
'        '
>>> pf.IndentType.DOTS().string(depth=2)
'········'
>>> pf.IndentType.THICK_DOTS().string(depth=2)
'••••••••'
>>> pf.IndentType.LINE().string(depth=2)
'|   |   '
>>> pf.IndentType.BROKEN_BAR().string(depth=2)
'¦   ¦   '
```
