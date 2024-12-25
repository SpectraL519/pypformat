# PyPformat

[![tests](https://github.com/SpectraL519/pypformat/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/tests)
[![examples](https://github.com/SpectraL519/pypformat/actions/workflows/examples.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/examples)
[![ruff - linter & formatter](https://github.com/SpectraL519/pypformat/actions/workflows/ruff.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/ruff)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/60ba7283e412ea91cd2db2b3b649003d/raw/pypf_covbadge.json)]()

<br />

## Overview

`PyPformat` is a simple and customizable python pretty formatting package and an alternative to the [pprint library](https://docs.python.org/3/library/pprint.html).

> [!IMPORTANT]
> The minimum (tested) python version required to use the `PyPformat` package is **3.9**.

> [!NOTE]
> While the `PyPformat` package is already quite versatile and customizable, its development is ongoing. A detailed list of the planned features/improvements can be found in the [PyPformat - TODO](/docs/todo.md) document.

<br />
<br />

## Installation

The `PyPformat` package can be installed via pip:

```shell
pip install pypformat
```

<br />
<br />

## Quick start

After installing the package, you have to import it in your python program with:

```python
import pformat as pf
```

The core element of the package is the `PrettyFormatter` class which can be used to format/serialize data to a string representation.

```python
formatter = pf.PrettyFormater()
data = ...
print(formatter(data))
```

The configuration of the `PrettyFormatter` class can be customized to allow different output styling. The available options and other utility is described in detail in the [PyPformat - Usage](/docs/usage.md) document.

<br />

### For developers

The [PyPformat - Dev notes](/docs/dev_notes.md) document contains the information about project development, testing and formatting.

<br />
<br />

## Licence

The `PyPformat` project is licenced under the [MIT Licence](https://opensource.org/license/mit/), which can be inspected in the [LICENCE](/LICENSE) file in the project's root directory.