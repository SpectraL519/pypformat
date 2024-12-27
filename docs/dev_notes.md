# PyPformat - Dev notes

- [Dev environment](#dev-environment)
- [Formatting and linting](#formatting-and-linting)
- [Testing](#testing)

<br />
<br />

## Dev environment

To create a complete development environment for the `PyPformat` project create a virtual environment and install the required dependencies:

```shell
pip install -r requirements-dev.txt
```

To run the project examples, you must install the project itself into the environment with:

```shell
cd <pypformat-root>
pip install .
```

<br />
<br />

## Formatting and linting

The project uses the [Ruff](https://docs.astral.sh/ruff/) formatter and linter, the configuration of which is defined in the [ruff.toml](/ruff.toml) file.

You can use the formatter and linter with:

```shell
ruff check # linter
ruff format # (--check) - formatter
```

<br />
<br />

## Testing

You can run the tests in the active environment using the `pytest` command.

Alternatively, you can run the `tox` command to run tests for all supported python versions. This will also generate coverage reports in `.coverage` files and/or directories.

> [!TIP]
> The `tox.ini` configuration file is prepared with CI testing in mind, therefore it will fail if any of the supported python versions is not available. To fix that, you can set the `skip_missing_interpreters` option to `True` **locally**.