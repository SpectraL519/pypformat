import pytest


def pytest_itemcollected(item: pytest.Item):
    if isinstance(item, pytest.Function):
        # Replace the `-` separator in parametric test names with `,`
        item._nodeid = item.nodeid.replace("-", ",")
