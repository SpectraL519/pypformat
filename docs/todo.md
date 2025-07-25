# PyPformat - TODO

## Planned features

- Introduction of the `print` and `format` free functions

- Item packing - if enabled, the formatter should pack as many item of iterables and mappings into a single line, as possible within the limit defined by the `width` option

- Max depth - if set the formatter should insert a placeholder (e.g. `...`) in place of the nested elements at the *max depth* level instead of formatting them indefinitely

- Default `__pf_*__` method implementation injection using decorators - might look something like:
  ```python
  @pf.with(pf.impl.format.inline)
  class MyClass:
      def __init__(self, number: int, string: str):
          self.number = number
          self.string = string

  fmt = pf.PrettyFormatter()
  print(fmt(MyClass(3, "abc")))
  # should print: MyClass(number=3, string="abc")
  ```

  Possible implmenetations:

  - `project` - returns `self.__dict__`
  - `project_public` - like `project` but filters items with the `_` prefix
  - `project_slots` - projects only the items that are present the `__slots__` attribute
  - `project_attrs` - projects only the attributes present int `__annotations__`
  - `format` - basic formatting implementation
  - `format_inline` - as shown in the example
  - `format_multiline` - similar to `format_inline` but each field is in a new line
