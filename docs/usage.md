# PyPformat - Usage

- [Baisc usage](#basic-usage)
- [Format options](#format-options)
  - [Options overview](#options-overview)
- [Utility](#utility)

<br />
<br />

## Basic usage

The core element of the `PyPformat` package is the `PrettyFormatter` class which can be used to format/serialize data to a string representation.

```python
import pformat as pf

formatter = pf.PrettyFormater()
data = ...
formatted_str = formatter(data) # or formatter.format(data)
print(formatted_str)
```

Optionally, you can set the `depth: int` parameter for the call of `formatter` (or `formatter.format`), which will set the nesting level of the input data.

<br />
<br />

## Format options

The `PrettyFormatter` class can be customized using formatting options, which alter the behaviour of the `PrettyFormatter`.

> [!NOTE]
> The options are stored in a `FormatOptions` dataclass, which is defined in the [format_options.py](/src/pformat/format_options.py) file.

This can be done in two ways:

- Using the `FormatOptions` class directly:

  ```python
  fmt_opts = pf.FormatOptions(<options>)
  formatter = pf.PrettyFormatter(fmt_opts)
  ```

- Using the `new` method:

  ```python
  formatter = pf.PrettyFormatter.new(<options>)
  ```

Both of these allow for specifying the same options, which are described in the [Options overview](#options-overview) section.

<br />

### Options overview

The table below contains a brief overview of all available formatting options.

| **Name** | **Type** | **Default value** | **Description** |
| :- | :- | :- | :- |
| `compact` | `bool` | `False` | If `True`, the pretty formatter will *try to* fit the elements in a single line within the constaints of the `width` parameter. |
| `width` | `int` | `50` | Specifies the limit of the `compact` packing of the formatted elements.<br/>If the length of the formatted string is greater than the parameter's value, the pretty formatter will *try to* split the string into multiple lines.  |
| [`indent_type`](#option-indent_type) | `IndentType` | `IndentType.NONE()` | Specifies the type of the indentation markers used for nested elements in collections and mappings. |
| [`text_style`](#option-text_style) | `TextStyle` | `TextStyle()` | Specifies the style, which will be applied to the text when formatting. |
| [`style_entire_text`](#option-style_entire_text) | `bool` | `False` | If `True`, the pretty formatter will apply the given style to the entire text.<br/>If `False`, the style will only be applied to individual values. |
| [`exact_type_matching`](#option-exact_type_matching) | `bool` | `False` | If `True`, the pretty formatter will apply the `projections` and `formatters` to items based on the `isinstance` checks.<br/>If `False`, `type(item) is <specified-type>` checks will be used. |
| [`projections`](#option-projections) | `TypeProjectionFuncMapping`<br>(Optional) | `None` | A *type to projection function* mapping, where the specified projection functions will be applied to each item **recursively** before formatting - only if the item's type is a valid key in the mapping. |
| [`formatters`](#option-formatters) | `MutableSequence[TypeFormatter]`<br/>(Optional) | `None` | A mutable sequence of `TypeFormatter` objects, which is prepended to a list of predefined type formatters, which is iterated in order during the process of type matching while formatting data. |

<br />

<details>
  <summary><h4 id="option-indent_type">Option: <code>indent_type</code></h4></summary>

  Description
</details>

<details>
  <summary><h4 id="option-text_style">Option: <code>text_style</code></h4></summary>

  Description
</details>

<details>
  <summary><h4 id="option-style_entire_text">Option: <code>style_entire_text</code></h4></summary>

  Description
</details>

<details>
  <summary><h4 id="option-exact_type_matching">Option: <code>exact_type_matching</code></h4></summary>

  Description
</details>

<details>
  <summary><h4 id="option-projections">Option: <code>projections</code></h4></summary>

  Description
</details>

<details>
  <summary><h4 id="option-formatters">Option: <code>formatters</code></h4></summary>

  Description
</details>

<br />
<br />

## Utility

<details>
  <summary><h3 id="utility-type-specific-formatters">Type specific formatters</h3></summary>

The `PrettyFormatter` class cotnains an ordered collection of type specific formatters. When formatting an item, this collection is traversed and the first matching formatter is applied to the input item.

The type specific formatters are instances of the `TypeFormatter` abstract class (defined in the [formatter_types.py](/src/pformat/formatter_types.py) file). The identifier of this class is its `type` member, which is then used in matching the formatted item's type in the function:

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

</details>

<br />
<br />

<details>
  <summary><h3 id="utility-text-styling">Text styling</h3></summary>

> [!IMPORTANT]
> `PyPformat` utilizes the [colored](https://dslackw.gitlab.io/colored/) package for text styling.

Text styling in the `PyPformat` package is done via the `TextStyle` dataclass defined in the [text_style.py](/src/pformat/text_style.py) file.

The members of this class are:

| **Name** | **Type** | **Default value** | **Description** |
| :- | :- | :- | :- |
| `value` | `TextStyleValue` | `None` | Represents the actual text style string, e.g.:<br/>- `colored.Fore.green`<br/>- `colored.Back.red`<br/>- `colored.Style.underline` |
| `mode` | `TextStyle.Mode` | `Mode.preserve` | Specifies how the text style should be applied to a string when using the `apply_to` method. |

> [!INFO]
> 
> The table below presents all available text style modes.
> 
> | **Name** | **Description** |
> | :- | :- |
> | normal | Returns `f"{Style.reset}{style}{s}{Style.reset}"` for an input string `s`. |
> | preserve | Replaces all `Style.reset` occurances with `f"{Style.reset}{<style>}"` in the input string and then applies the style like the *normal* mode to the aligned string. |
> | override | Removes all style modifiers from the input string and then applies the style like the *normal* mode to the aligned string. |

<br />

#### Additional utility

##### Type definitions

- `TextStyleValue` - a type alias for `Optional[str]`
- `TextStyleParam` - a type alias for `Union[TextStyle, TextStyleValue]`

<br />

##### Utility methods of the `TextStyle` class

- `apply_to(s: str) -> str` - returns the input string with the text style applied based on the `mode` parameter
- `apply_to_each(s_collection: Iterable[str]) -> list[str]` - returns a new list of styled strings constructed by calling the `apply_to` method for each string in the input iterable
- [static] `new(style: TextStyleParam = None, mode: Optional[Mode] = None) -> TextStyle` - creates a new `TextStyle` instance based on the input parameters
</details>

<br />

##### Utility functions

- `rm_style_modifiers(s: str) -> str` - removes all ANSI escape sequences from a string
- `strlen_no_style(s: str) -> int` - returns the length of the string after removing its style modifiers

<!-- indentation -->

<!--
<details>
  <summary><h3 id="utility-...">...</h3></summary>
</details>
 -->
