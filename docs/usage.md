# PyPformat - Usage

- [Baisc usage](#basic-usage)
- [Format options](#format-options)
  - [Options overview](#options-overview)
- [Examples](#examples)

<br />

Related pages:

- [PyPformat - Utility](/docs/utility.md)

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
| `indent_type` | [`IndentType`](/docs/utility.md#indentation) | `IndentType.NONE()` | Specifies the type of the indentation markers used for nested elements in collections and mappings. |
| `text_style` | [`TextStyle`](/docs/utility.md#text-styling) | `TextStyle()` | Specifies the style, which will be applied to the text when formatting. |
| `style_entire_text` | `bool` | `False` | If `True`, the pretty formatter will apply the given style to the entire text.<br/>If `False`, the style will only be applied to individual values. |
| `exact_type_matching` | `bool` | `False` | If `True`, the pretty formatter will apply the `projections` and `formatters` to items based on the `isinstance` checks.<br/>If `False`, `type(item) is <specified-type>` checks will be used. |
| `projections` | `TypeProjectionFuncMapping`<br>(Optional) | `None` | A *type to projection function* mapping, where the specified projection functions will be applied to each item **recursively** before formatting - only if the item's type is a valid key in the mapping. |
| `formatters` | `MutableSequence[TypeFormatter]`<br/>(Optional) | `None` | A mutable sequence of [`TypeFormatter`](/docs/utility.md#type-specific-formatters) objects, which is prepended to a list of predefined type formatters and then sorted in an inheritance-wise order (the child types precede their parent types in the ordering). Then, the preprocessed sequence is traveresed in this order to match the type of an input element to a corresponding formatter object. |

> [!WARNING]
>
> In the current version the text style specified in the formatting options may not be applied for types formatted using custom formatters (passed through the `formatters` parameter). Therefore the style must be applied manually within the custom formatter.

<br />
<br />

## Examples

In the [examples](/examples/) directory, you can find short demo programs demonstating the usage of the `PyPformat` package:

- `simpla_data.py` - integers, floats, strings, etc.
- `complex_data.py` - collections, mappings, etc.

The formatting configurations used in the example programs are provided in the [common.py](/examples/common.py) file.
