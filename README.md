# PyPformat

[![tests](https://github.com/SpectraL519/pypformat/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/tests)
[![examples](https://github.com/SpectraL519/pypformat/actions/workflows/examples.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/examples)
[![ruff - linter & formatter](https://github.com/SpectraL519/pypformat/actions/workflows/ruff.yaml/badge.svg)](https://github.com/SpectraL519/pypformat/actions/workflows/ruff)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/60ba7283e412ea91cd2db2b3b649003d/raw/pypf_covbadge.json)]()

<br />

## Overview

`PyPformat` is a simple and highly customizable python pretty-formatting package designed as an alternative to the built-in [pprint library](https://docs.python.org/3/library/pprint.html) - `PyPformat` uses a different, more natural formatting style and provides extensive personalization capabilities, including text colorizing or customized indentation marking, on top of the basic options like compact printing.

<br />

The example below demostrates the difference in the **default** outputs produced by the `pprint` and `PyPformat` libraries.

```txt
>>> from pprint import pprint
>>> import pformat as pf
>>>
>>> from collections import ChainMap, OrderedDict, defaultdict
>>>
>>> mapping = {
...     "key1": 1,
...     "key2": OrderedDict({"key3": 3, "key4": 4}),
...     "key5": defaultdict(
...         str,
...         {
...             "key6": 6,
...             "a_very_long_dictionary_key7": ChainMap(
...                 {"key10": [10, 11, 12, 13], "key8": 8, "key9": 9}
...             ),
...         },
...     ),
... }
>>>
>>> pprint(mapping)
{'key1': 1,
 'key2': OrderedDict({'key3': 3, 'key4': 4}),
 'key5': defaultdict(<class 'str'>,
                     {'a_very_long_dictionary_key7': ChainMap({'key10': [10,
                                                                         11,
                                                                         12,
                                                                         13],
                                                               'key8': 8,
                                                               'key9': 9}),
                      'key6': 6})}
>>>
>>> formatter = pf.PrettyFormatter()
>>> print(formatter(mapping))
{
    'key1': 1,
    'key2': OrderedDict({
        'key3': 3,
        'key4': 4,
    }),
    'key5': defaultdict(<class 'str'>, {
        'key6': 6,
        'a_very_long_dictionary_key7': ChainMap({
            'key10': [
                10,
                11,
                12,
                13,
            ],
            'key8': 8,
            'key9': 9,
        }),
    }),
}
```

> [!IMPORTANT]
>
> - The minimum (tested) python version required to use the `PyPformat` package is **3.9**.
> - The complete functionality of the `PyPformat` package (including all format configuration options) is described in the [PyPformat - Usage](/docs/usage.md) document.
> - While the `PyPformat` package is already quite versatile and customizable, its development is ongoing. A detailed list of the planned features/improvements can be found in the [PyPformat - TODO](/docs/todo.md) document.

<br />
<br />

## Installation

The `PyPformat` package can be installed via pip:

```shell
pip install pypformat
```

<br />
<br />

## For developers

The [PyPformat - Dev notes](/docs/dev_notes.md) document contains the information about project development, testing and formatting.

<br />
<br />

## Licence

The `PyPformat` project is licenced under the [MIT Licence](https://opensource.org/license/mit/), which can be inspected in the [LICENCE](/LICENSE) file in the project's root directory.
