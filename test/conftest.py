from typing import Callable

import pytest


def pytest_itemcollected(item: pytest.Item):
    if isinstance(item, pytest.Function):
        # Replace the `-` separator in parametric test names with `,`
        item._nodeid = item.nodeid.replace("-", ",")


def assert_does_not_throw(func: Callable, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        pytest.fail(f"Function `{func.__name__}` raised an exception: {e}")


def gen_derived_type(t: type) -> type:
    class Derived(t):
        pass

    return Derived
