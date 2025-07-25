# PyPformat - Utility

- [Text Styling](#text-styling)
- [Indentation](#indentation)
- [Named Types](#named-types)
- [Type-specific Callable Objects](#type-specific-callable-objects)
- [Type Projection Objects](#type-projection-objects)
- [Type Formatter Objects](#type-formatter-objects)
- [PyPformat Magic Methods](#pypformat-magic-methods)

<br />
<br />

## Text Styling

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

### Additional Utility

#### Type definitions

- `TextStyleValue` - a type alias for `Optional[str]`
- `TextStyleParam` - a type alias for `Union[TextStyle, TextStyleValue]`

#### Utility methods of the `TextStyle` class

- `apply_to(s: str) -> str` - returns the input string with the text style applied based on the `mode` parameter
- `apply_to_each(s_collection: Iterable[str]) -> list[str]` - returns a new list of styled strings constructed by calling the `apply_to` method for each string in the input iterable
- [static] `new(style: TextStyleParam = None, mode: Optional[Mode] = None) -> TextStyle` - creates a new `TextStyle` instance based on the input parameters

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

<br />
<br />

## Named Types

The `PyPformat` package defines a few *named types* to make the formatting of complex types easier (e.g. through projections, see [Type Projection Objects](#type-projection-objects)).

These include `NamedIterable` and `NamedMapping`:

```python
@dataclass
class NamedIterable(Iterable):
    name: str
    iterable: Iterable
    parens: Optional[Tuple[str, str]] = None
```

```python
@dataclass
class NamedMapping(Mapping):
    name: str
    mapping: Mapping
    parens: Optional[Tuple[str, str]] = None
```

These types can be used to specify the name and/or parenthesis used for a given iterable/mapping object without having to create a specifc class derived from `list`/`dict` or other built-in iterable/mapping types:

> [!NOTE]
>
> The `NamedIterable` and `NamedMapping` classes define a `get_parens() -> Tuple[str, str]` method, which will return the `parens` member or `(f"{self.name}({{", "})")` if `parens` is `None`. This method is used by the `PrettyFormatter` class when processing a `NamedIterable`/`NamedMapping` instance.

An example use case for these types is shown in the [PyPformat Magic Methods](#pypformat-magic-methods) section.

<br />
<br />

## Type-specific Callable Objects

The `PyPformat` package defines a `TypeSpecificCallable` abstract class (file: [type_specific_callable.py](/src/pformat/type_specific_callable.py)) which is used as a base class for the type [projection](#type-projection-objects) and [formatter](#type-formatter-objects) objects.

This class has only one member - `type: type`, which is also used as and identifier of the class. Naturally, it is the only parameter of the class's constructor.

The `TypeSpecificCallable` defines the following methods:

- **Abstract** `__call__` magic method, which takes at least one positional argument:

  ```python
  @abstractmethod
  __call__(self, obj: Any, *args, **kwargs) -> Any:
  ```

- Magic methods: `__eq__`, `__repr__`

- `has_valid_type` - used to verify whether an object has a type which can be handled by the callable instance.

  ```python
  has_valid_type(self, obj: Any, exact_match: bool = False) -> bool
  ```

- `covers` - used to verify whether the `other` instance of `TypeSpecificCallable` contains a type which can also be handled by `self`.

  ```python
  covers(self, other: TypeSpecifcCallable, exact_match: bool = False) -> bool
  ```

> [!NOTE]
> If the `exact_match` parameter is set to `True`, the functions will use the `<type-to-check> is self.type` check. Otherwise, the `isinstance` or `issubclass` behaviour is used.

- `cmp` - a classmethod which defines the comparator logic used for ordering of `TypeSpecificCallable` objects.

  ```python
  @classmethod
  cmp(cls, c1: TypeSpecifcCallable, c2: TypeSpecifcCallable) -> int
  ```

  The function will return:

  - a negative number if `c1 < c2`,
  - a positive number if `c1 > c2`,
  - zero otherwise,

  with the assumption that an instance `c1` is considered greater than `c2` if `c2.type` is a subtype of `c1.type`. This includes the `Any` and `Union` types.

<br />
<br />

## Type Projection Objects

The `PrettyFormatter` class supports type projections through the `TypeProjection` class defined in the [type_projection.py](/src/pformat/type_projection.py) file. This is a subclass of [`TypeSpecificCallable`](#type-specific-callable-objects) which implies that instances of `TypeProjection` are identified by their `type` parameter.

However, the `TypeProjection` class requires a `proj_func: TypeProjectionFunc` parameter in its constructor in addition to the `type` parameter, where `TypeProjectionFunc = Callable[[Any], Any]`. The `proj_func` is the functional object which performs the actual projection logic.

When defining the projections for the `PrettyFormatter` class, you can instantiate the instances of `TypeProjection` directly or using the defined builder function:

```python
int_proj = pf.TypeProjection(int, lambda i: str(i))
float_proj = pf.make_projection(float, lambda f: int(f))
```

> [!CAUTION]
> Defining projection functions which project a given type onto itself, a subtype of the given type or a collection of objects of the same or derived types **with `exact_type_matching=False` (default)** will result in an infinite recursion.

<br />
<br />

## Type Formatter Objects

The `PrettyFormatter` class cotnains an ordered collection of type specific formatters. When formatting an item, this collection is traversed and the first matching formatter is applied to the input item.

The type specific formatters are instances of the `TypeFormatter` abstract class (defined in the [type_formatter.py](/src/pformat/type_formatter.py) file), which inherits from [`TypeSpecificCallable`](#type-specific-callable-objects) and therefore the identifier of this class is its `type` member, which is then used for matching the formatted item's type in the `has_valid_type` function.

<br />

The `TypeFormatter` class is the base type used for type specific formatters and defines a common abstract method:

```python
@abstractmethod
__call__(self, obj: Any, depth: int) -> str
```

You can use this class as a base for you custom formatters. Alternatively, you can create custom formatter objects using the helper function:

```python
make_formatter(t: type, fmt_func: TypeFormatterFunc) -> CustomFormatter
```

Where the `fmt_func` parameter is a callable, the signature of which matches the signature of the `__call__` abstract method of the `TypeFormatter` base class.

<br />
<br />

## PyPformat Magic Methods

The type projections and/or formatters can be specified for the `PrettyFormatter` class using the formatting options (as described in [Format Options](/docs/usage.md#format-options)) or using dedicated magic methods.

### Projections: `__pf_project__`

If a type defines the `__pf_project__` magic method, it will be used directly when applying the type projections.

> [!CAUTION]
>
> This magic method will override any type projections specified for the *projectable* type using the [Format Options](/docs/usage.md#format-options).

An example from the [complex_data](/examples/complex_data.py) demo script:

### Formatting: `__pf_format__(options)`

If a type defines the `__pf_format__` magic method, it will be used directly to format the given object.

> [!CAUTION]
>
> This magic method will override any default/custom type formatters specified for the *formattable* type using the [Format Options](/docs/usage.md#format-options). Moreover, it will **not** apply any projections to the type, even if the `__pf_project__` method is defined for the type.

<br/>

### Examples

Below you can see how the `__pf_project__` and `__pf_format__` magic methods can be used in code:

```python
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
```

However, to see how the formatting of such classes would actually behave, check out the [complex_data](/examples/complex_data.py) example/demo script.
