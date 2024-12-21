# pypformat

Python pretty formatting package

[![tests](https://github.com/SpectraL519/pypformat/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/tests)
[![examples](https://github.com/SpectraL519/pypformat/actions/workflows/examples.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/examples)
[![ruff - linter & formatter](https://github.com/SpectraL519/pypformat/actions/workflows/ruff.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/ruff)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/60ba7283e412ea91cd2db2b3b649003d/raw/pypf_covbadge.json)]()

<br />

## TODO

- Remove `test_dummy.py` before release
- Add notes:
  - (important/caution) using projections:
    - don't project a type onto a list of the same type - infinite recursion
    - `text_style` may/will not be applied for custom-formatted types with `style_entire_text=False`
- Remove the `PrettyFormatter.new` and `FormatOptions.default` methods ?
