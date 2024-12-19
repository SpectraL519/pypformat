# pypformat

Python pretty formatting package

[![tests](https://github.com/SpectraL519/pypformat/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/tests)
[![ruff - linter & formatter](https://github.com/SpectraL519/pypformat/actions/workflows/ruff.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/ruff)

<br />

## TODO

- Remove `test_dummy.py` before release
- Add notes:
  - (important/caution) using projections:
    - don't project a type onto a list of the same type - infinite recursion
    - `text_style` may/will not be applied for custom-formatted types with `style_entire_text=False`
- Remove the `PrettyFormatter.new` and `FormatOptions.default` methods ?
