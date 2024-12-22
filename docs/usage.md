# PyPformat - Usage

- [Baisc usage](#basic-usage)
- [Format options](#format-options)
  - [Options overview](#options-overview)

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

The `PrettyFormatter` class can be customized using formatting options, which alter the behaviour of the `PrettyFormatter`. This can be done in two ways:

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

| **Option** | **Type** | **Default value** | **Description** |
| :- | :- | :- | :- |
| `compact` | `bool` | `False` | ... |
| `width` | `Optional[int]` | `50` | ... |
| `indent_type` | `IndentType` | `IndentType.NONE()` | ... |
| `text_style` | `TextStyle` | `TextStyle()` | ... |
| `style_entire_text` | `bool` | `False` | ... |
| `strict_type_matching` | `bool` | `False` | ... |
| `projections` | <pre>Optional[<br>&nbsp;TypeProjectionFuncMapping<br>]</pre> | `None` | ... |
| `formatters` | <pre>Optional[<br>&nbsp;TypeFormatterFuncMutSequence<br>]</pre> | `None` | ... |
