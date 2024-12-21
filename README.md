# pypformat

Python pretty formatting package

[![tests](https://github.com/SpectraL519/pypformat/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/tests)
[![examples](https://github.com/SpectraL519/pypformat/actions/workflows/examples.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/examples)
[![ruff - linter & formatter](https://github.com/SpectraL519/pypformat/actions/workflows/ruff.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/ruff)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/f6cec4c4c8e1733cfe45f807918a128a/raw/pypf_covbadge.svg)]()

<br />

## TODO

- Remove `test_dummy.py` before release
- Add notes:
  - (important/caution) using projections:
    - don't project a type onto a list of the same type - infinite recursion
    - `text_style` may/will not be applied for custom-formatted types with `style_entire_text=False`
- Remove the `PrettyFormatter.new` and `FormatOptions.default` methods ?
