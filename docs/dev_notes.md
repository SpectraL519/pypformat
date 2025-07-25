# PyPformat - Dev notes

- [Dev environment](#dev-environment)
- [Formatting and linting](#formatting-and-linting)
- [Testing](#testing)
- [Other]()

<br />
<br />

## Dev environment

To create a complete development environment for the `PyPformat` project create a virtual environment and install the required dependencies. You can do it by running:

```shell
make prepare-venv
source venv/bin/activate
```

To run the project examples, you must install the project itself into the environment with:

```shell
make install
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

or

```shell
make ruff
# equivalent to: ruff format && ruff check --fix
```

<br />
<br />

## Testing

You can run the tests in the active environment using the `pytest` command.

Alternatively, you can run the `tox` command to run tests for all supported python versions. This will also generate coverage reports in `.coverage` files and/or directories.

> [!TIP]
> The `tox.ini` configuration file is prepared with CI testing in mind, therefore it will fail if any of the supported python versions is not available. To fix that, you can set the `skip_missing_interpreters` option to `True` **locally**.

<br />
<br />

## Other

The [Makefile](/Makefile) defines a few utility targets which can be used to parform actions like running tests, building the project, cleaning temorary files, etc.

These targets include:

```shell
prepare-venv    # prepare the virtual environment
clean-venv      # remove the virtual environment
tests-simple    # run tests directly using pytest
tests-tox       # run test using tox and generate the coverage report
clean-tests     # clean the test-related temporary files
clean-cov       # clean the coverage-related temporary files
build           # build the project/package
clean-build     # clean the build files
ruff            # run the ruff formatter and linter
clean-ruff      # clean ruff temporary files
clean-all       # clean all temporary files
install         # install the project to the current envinronment
upload          # upload the distribution files to pypi (requires access to the pypi project)
```

> [!NOTE]
>
> Apart from `prepare-venv` and `clean-*` all targets require to be sourced to a valid project environment within the current shell session (e.g. by using `source venv/bin/activate` if you've used the `prepare-venv`).
